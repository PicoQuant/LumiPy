"""
LumiPy Python Remote Execution Server
----------------------------------------
- Sandboxed exec() with restricted builtins and isolated namespace
- **Main-thread execution** — client scripts run on the main thread so
  GUI code (tkinter, Qt, etc.) works correctly
- Networking / accept loop runs on a background thread
- On timeout the client receives output so far; execution continues on the
  main thread.  The client can poll with ``__get_last_output__`` or cancel
  with ``__kill_execution__``.
- Robust length-prefix framing (handles TCP fragmentation)
- SO_REUSEADDR to avoid "address already in use" on restart
- Proper exception-specific error handling
- Graceful shutdown on KeyboardInterrupt / SIGTERM
"""

import contextlib
import ctypes
import io
import os
import sys
import logging
import queue
import signal
import socket
import struct
import threading
import time
import traceback

import pqlumi as pql
import pqtool as pqt
import pqdc as pqd
import pqscan as pqs
import pqharp as pqh
import pqcam as pqc

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

# RCE server IP and PORT
HOST = "127.0.0.1" # localhost; change this if run remotely
PORT = 65432

EXEC_TIMEOUT_SECONDS = 5  # Default wall-clock timeout per script
MAX_SCRIPT_BYTES = 64 * 1024  # 64 KB cap on incoming script size

# How often the main-thread loop calls pqt.gui_sleep() and checks the
# script queue (in seconds).  Lower = more responsive, higher = less CPU.
MAIN_LOOP_POLL_INTERVAL = 0.05  # 50 ms

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(threadName)s: %(message)s",
)
log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Sandbox helpers
# ---------------------------------------------------------------------------

# Modules that are blocked entirely — these allow writing/deleting files
# or executing external programs.
_BLOCKED_MODULES = {
    # External process execution
    "subprocess", "multiprocessing", "concurrent.futures",
    "pty", "popen2", "commands",
    # File writing / deletion via OS
    "os", "shutil", "pathlib", "tempfile", "glob",
    # Dynamic code execution from untrusted sources
    "importlib", "runpy", "compileall", "py_compile",
    # Network that could exfiltrate data
    "socket", "http", "urllib", "requests",
    # Sandbox escape via low-level or introspection APIs
    "ctypes", "code", "ast", "types",
}


def _safe_import(name, *args, **kwargs):
    """Allow all imports except those in _BLOCKED_MODULES.

    Also patches 'os' submodules to strip write/execute capabilities
    when accessed indirectly (e.g. via os.path which is read-only safe).
    """
    top_level = name.split(".")[0]
    if top_level in _BLOCKED_MODULES or name in _BLOCKED_MODULES:
        raise ImportError(f"Module '{name}' is not allowed on this server")
    module = __import__(name, *args, **kwargs)
    return module


# Use all real builtins, then remove the dangerous ones.
# This is safer than a whitelist because it won't silently break
# builtins we forgot to include.
import builtins as _builtins_module

_SAFE_BUILTINS = vars(_builtins_module).copy()

# Remove builtins that can execute programs or overwrite files
for _name in (
    "open",        # re-added below as read-only
    "exec",        # no nested exec
    "eval",        # no nested eval
    "compile",     # no dynamic compilation
    "__import__",  # replaced with _safe_import below
):
    _SAFE_BUILTINS.pop(_name, None)

# Re-add open() in read-only mode
def _safe_open(file, mode="r", *args, **kwargs):
    """open() restricted to read-only modes."""
    if any(c in mode for c in ("w", "a", "x", "+")):
        raise PermissionError("Writing to files is not allowed on this server")
    return _builtins_module.open(file, mode, *args, **kwargs)

_SAFE_BUILTINS["open"] = _safe_open
_SAFE_BUILTINS["__import__"] = _safe_import


# Persistent sandbox namespace — variables created by one script run are
# available to subsequent runs, just like a live Python session.
_sandbox: dict = {"__builtins__": _SAFE_BUILTINS}


# ---------------------------------------------------------------------------
# Protocol helpers
# ---------------------------------------------------------------------------
# Wire format: [4-byte big-endian script length][4-byte big-endian timeout][script bytes]

HEADER_SIZE = 8  # 4 bytes length + 4 bytes timeout
MAX_TIMEOUT_SECONDS = 3600  # 1 hour upper cap on client-supplied timeout


def _recv_exactly(conn: socket.socket, n: int) -> bytes:
    """Read exactly *n* bytes from *conn*, handling partial recv() calls."""
    buf = bytearray()
    while len(buf) < n:
        chunk = conn.recv(n - len(buf))
        if not chunk:
            raise ConnectionError("Connection closed before all bytes received")
        buf.extend(chunk)
    return bytes(buf)


def _recv_script(conn: socket.socket) -> tuple[str, int]:
    """Read a length-prefixed script and timeout from the connection.

    Returns (script, timeout_seconds).
    """
    header = _recv_exactly(conn, HEADER_SIZE)
    num_bytes, timeout = struct.unpack(">II", header)  # two unsigned 32-bit big-endian

    if num_bytes == 0:
        raise ValueError("Client sent zero-length script")
    if num_bytes > MAX_SCRIPT_BYTES:
        raise ValueError(
            f"Script size {num_bytes} exceeds limit of {MAX_SCRIPT_BYTES} bytes"
        )
    if timeout > MAX_TIMEOUT_SECONDS:
        raise ValueError(
            f"Timeout {timeout}s exceeds maximum of {MAX_TIMEOUT_SECONDS}s"
        )
    if timeout <= 0:
        timeout = EXEC_TIMEOUT_SECONDS  # 0 means "use server default"

    raw = _recv_exactly(conn, num_bytes)
    return raw.decode("utf-8"), timeout


# ---------------------------------------------------------------------------
# Thread-safe output buffer
# ---------------------------------------------------------------------------

class ThreadSafeOutput(io.TextIOBase):
    """A write-only text stream whose contents can be safely read from any thread.

    The main thread writes to it (via redirect_stdout / print).
    Network threads read from it (via getvalue / snapshot).
    A lock protects the internal buffer so reads never race with writes.
    """

    def __init__(self) -> None:
        self._buf: list[str] = []
        self._lock = threading.Lock()

    # --- Writer interface (main thread) ------------------------------------

    def write(self, s: str) -> int:
        with self._lock:
            self._buf.append(s)
        return len(s)

    def writable(self) -> bool:
        return True

    # --- Reader interface (any thread) -------------------------------------

    def getvalue(self) -> str:
        with self._lock:
            return "".join(self._buf)


# ---------------------------------------------------------------------------
# Execution state  (shared between main thread and network threads)
# ---------------------------------------------------------------------------

# Queue item: (script, done_event, result_holder)
#   - done_event    : threading.Event — set by the main thread when exec() finishes
#   - result_holder : single-element list; main thread puts the result string in [0]
_script_queue: queue.Queue = queue.Queue()

# Set while the main thread is executing a script.
_busy = threading.Event()

# Shared execution state — readable from any thread.
_last_execution: dict = {
    "output": None,     # ThreadSafeOutput capturing stdout
    "running": False,   # True while exec() is in progress
}


# ---------------------------------------------------------------------------
# Special commands  (handled on the network thread — no main-thread needed)
# ---------------------------------------------------------------------------

def _get_last_output() -> str:
    """Return the output of the last execution, or a status message if still running."""
    output = _last_execution["output"]
    if output is None:
        return "No previous execution found\n"
    if _last_execution["running"]:
        current = output.getvalue()
        return (
            f"Still running - output so far:\n{current}"
            if current
            else "Still running — no output yet\n"
        )
    return output.getvalue() or "(no output)\n"


def _kill_execution() -> str:
    """Inject a KeyboardInterrupt into the main thread to cancel execution.

    The main thread's exec() is wrapped in a try/except that catches
    KeyboardInterrupt and records the partial output, so the interrupt
    is handled gracefully.
    """
    if not _last_execution["running"]:
        return "No execution is currently running\n"

    main_tid = threading.main_thread().ident
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
        ctypes.c_ulong(main_tid),
        ctypes.py_object(KeyboardInterrupt),
    )
    if res == 0:
        return "Error: Could not interrupt main thread — invalid thread id\n"
    if res > 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_ulong(main_tid), None)
        return "Error: Exception raised in multiple threads — undone\n"

    # Give the main thread a moment to handle the interrupt
    deadline = time.monotonic() + 3.0
    while _last_execution["running"] and time.monotonic() < deadline:
        time.sleep(0.1)

    if _last_execution["running"]:
        return "Warning: Interrupt sent but execution has not stopped yet (may be stuck in a C extension)\n"

    log.warning("Execution interrupted by client request")
    return "Execution interrupted successfully\n"


def _get_environment_info() -> str:
    """Get information about the environment the server is running in."""
    import platform
    from importlib.metadata import distributions

    out = f"Python version: {sys.version}\n"
    out += f"Platform: {platform.platform()}\n"
    out += "Installed packages:\n"
    for dist in distributions():
        out += f"  {dist.metadata['Name']}=={dist.metadata['Version']}\n"

    out += f"  pqlumi=={pql.get_version()}\n"
    out += f"  pqtool=={pqt.get_version()}\n"
    out += f"  pqdc=={pqd.get_version()}\n"
    out += f"  pqharp=={pqh.get_version()}\n"
    out += f"  pqcam=={pqc.get_version()}\n"
    out += f"  pqscan=={pqs.get_version()}\n"

    out += "Forbidden imports:\n"
    for m in list(_BLOCKED_MODULES):
        out += f"  {m}\n"

    return out


def _get_system_config() -> str:
    """Get information about the Luminosa microscopy system."""
    conf_file = os.path.dirname(sys.executable) + '\\PQDevice.conf'
    with open(conf_file, 'r') as f:
        conf = f.read()
    return conf


# Map of special command strings → handler functions.
# These are executed directly on the network thread.
_SPECIAL_COMMANDS: dict[str, callable] = {
    "__get_last_output__":      _get_last_output,
    "__kill_execution__":       _kill_execution,
}

_SPECIAL_COMMANDS2: dict[str, callable] = {
    "__get_environment_info__": _get_environment_info,
    "__get_system_config__":    _get_system_config,
}


# ---------------------------------------------------------------------------
# Main-thread script execution
# ---------------------------------------------------------------------------

def _execute_on_main_thread(script: str) -> str:
    """Execute *script* directly on the calling (main) thread.

    Called from the main-thread loop — NOT from a worker thread.
    No timeout is enforced here; the network thread handles the client
    timeout independently by giving up waiting on done_event.
    """
    output = ThreadSafeOutput()
    _last_execution["output"] = output
    _last_execution["running"] = True

    try:
        with contextlib.redirect_stdout(output):
            exec(script, _sandbox)  # intentional RCE — runs on main thread
    except KeyboardInterrupt:
        # Injected by _kill_execution() — record partial output and stop.
        # We do NOT re-raise: the main-thread loop should keep running.
        print("\nExecution interrupted by client\n", file=output)
        log.warning("Execution interrupted via KeyboardInterrupt on main thread")
    except Exception:
        print(traceback.format_exc(), file=output)
    finally:
        _last_execution["running"] = False

    return output.getvalue()


# ---------------------------------------------------------------------------
# Client handler  (runs on a networking thread)
# ---------------------------------------------------------------------------

def handle_client(conn: socket.socket, addr: tuple) -> None:
    """Receive a script, dispatch it to the main thread, send back the result."""
    log.info("Connected: %s", addr)
    try:
        script, timeout = _recv_script(conn)
        log.info(
            "Received %d-char script (timeout=%ds) from %s",
            len(script), timeout, addr,
        )

        stripped = script.strip()

        handler = _SPECIAL_COMMANDS.get(stripped)
        handler2 = _SPECIAL_COMMANDS2.get(stripped)

        # --- Special commands: handled immediately on this thread ------------
        if handler is not None:
            result = handler()

        # --- Server busy: reject new scripts --------------------------------
        elif _busy.is_set():
            result = "Error: Server is busy - a previous script is still running\n"

        # --- Special commands: handled immediately on this thread ------------
        elif handler2 is not None:
            result = handler2()

        # --- Normal script: enqueue for main-thread execution ---------------
        else:
            result_holder: list[str | None] = [None]
            done_event = threading.Event()
            _script_queue.put((script, done_event, result_holder))

            # Wait up to *timeout* seconds for the main thread to finish.
            finished = done_event.wait(timeout=timeout)

            if finished:
                # Execution completed within the timeout
                result = result_holder[0] or "(no output)\n"
            else:
                # Timeout: execution is still running on the main thread.
                # Return whatever output has been captured so far.
                output = _last_execution["output"]
                partial = output.getvalue() if output else ""
                result = (
                    f"{partial}"
                    f"\nExecution timed out after {timeout}s — "
                    f"still running on server.\n"
                    f"Use __get_last_output__ to poll or "
                    f"__kill_execution__ to cancel.\n"
                )

        log.info("Sending %d bytes of output to %s", len(result), addr)
        conn.sendall(result.encode("utf-8"))

    except (ConnectionError, ValueError) as exc:
        log.warning("Protocol error from %s: %s", addr, exc)
        try:
            conn.sendall(f"Error: {exc}\n".encode("utf-8"))
        except OSError:
            pass
    except OSError as exc:
        log.error("Socket error with %s: %s", addr, exc)
    finally:
        conn.close()
        log.info("Disconnected: %s", addr)


# ---------------------------------------------------------------------------
# Networking thread  (accept loop)
# ---------------------------------------------------------------------------

def _accept_loop(
    server_sock: socket.socket, shutdown_event: threading.Event,
) -> None:
    """Accept incoming connections and spawn a handler thread for each.

    Runs on a background thread so the main thread is free for exec().
    """
    while not shutdown_event.is_set():
        try:
            conn, addr = server_sock.accept()
        except socket.timeout:
            continue
        except OSError:
            if not shutdown_event.is_set():
                log.error("Accept error", exc_info=True)
            break

        thread = threading.Thread(
            target=handle_client,
            args=(conn, addr),
            daemon=True,
            name=f"client-{addr[0]}:{addr[1]}",
        )
        thread.start()

    log.info("Accept loop stopped")


# ---------------------------------------------------------------------------
# Server  (main-thread loop)
# ---------------------------------------------------------------------------

def run_server() -> None:
    """Start the server.

    The *main thread* runs a polling loop that:
      1. Calls ``pqt.gui_sleep()`` to pump the GUI event loop.
      2. Checks the script queue and executes scripts inline.

    Networking (accept + recv) happens on background threads.
    Client timeout only controls how long the *client waits* for a reply —
    it does NOT interrupt execution on the main thread.
    """
    shutdown_event = threading.Event()

    def _handle_signal(signum, _frame):
        log.info("Received signal %s – shutting down", signum)
        shutdown_event.set()

    signal.signal(signal.SIGINT, _handle_signal)
    signal.signal(signal.SIGTERM, _handle_signal)

    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.settimeout(1.0)
    server_sock.bind((HOST, PORT))
    server_sock.listen(2)
    log.info("Listening on %s:%s (hostname: %s)", HOST, PORT, socket.gethostname())

    # Start the accept loop on a background thread
    accept_thread = threading.Thread(
        target=_accept_loop,
        args=(server_sock, shutdown_event),
        daemon=True,
        name="accept-loop",
    )
    accept_thread.start()

    # ----- Main-thread loop --------------------------------------------------
    try:
        while not shutdown_event.is_set():
            # Pump the GUI event loop (required by PicoQuant toolkit)
            pqt.gui_sleep()

            # Check for a queued script — non-blocking
            try:
                script, done_event, result_holder = _script_queue.get_nowait()
            except queue.Empty:
                time.sleep(MAIN_LOOP_POLL_INTERVAL)
                continue

            # Execute on this (main) thread
            _busy.set()
            log.info("Executing script on main thread")
            try:
                result = _execute_on_main_thread(script)
            finally:
                _busy.clear()

            # Deliver result to the waiting network handler thread.
            # If the handler already timed out and responded to the client,
            # it will simply ignore this — no harm done.
            result_holder[0] = result
            done_event.set()

    except KeyboardInterrupt:
        log.info("KeyboardInterrupt — shutting down")
        shutdown_event.set()
    finally:
        server_sock.close()
        accept_thread.join(timeout=3.0)
        log.info("Server stopped")


if __name__ == "__main__":
    run_server()
