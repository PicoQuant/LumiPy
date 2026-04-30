from fastmcp import FastMCP
import os
import socket
import time
import struct
import logging

# RCE server IP and PORT
HOST = "127.0.0.1" # localhost; change this if run remotely
PORT = 65432

LOG_FILE = os.path.join(
    os.path.dirname(__file__),
    "LumiPyMCP_" + time.strftime("%Y_%m_%d", time.localtime()) + ".log",
)

LOG_FILE2 = os.path.join(
    os.path.dirname(__file__),
    "LumiPyMCP_" + time.strftime("%Y_%m_%d", time.localtime()) + ".log.py",
)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

print(f"Hostname: {socket.gethostname()} ({HOST}:{PORT})")

mcp = FastMCP("LumiPyMCPTool")


def log_to_file(log: str):
    """
    Write a log to a file.

    Parameters
    ----------
    log : str
        The log to write to the file.

    Notes
    -----
    If the file does not exist, it will be created.
    If the file already exists, the log will be appended to the end of the file.
    """

    if not os.path.exists(LOG_FILE2):
        with open(LOG_FILE2, 'w') as f:
            f.write('')

    with open(LOG_FILE2, 'a') as f:
        f.write(log)

def send_code(code: str = "", timeout: int = 10) -> str:
    """
    Send code to the local executor over TCP and return the output.

    Parameters
    ----------
    code : str
        The Python code (or special command) to send.
    timeout : int
        Execution timeout in seconds.

    Returns
    -------
    str
        The output returned by the executor, or an error message.
    """
    if not code:
        return ""

    try:
        encoded = code.encode("utf-8")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout + 5)  # network timeout slightly above exec timeout
            sock.connect((HOST, PORT))
            sock.sendall(struct.pack(">II", len(encoded), timeout) + encoded)
            sock.shutdown(socket.SHUT_WR)

            response = b""
            while chunk := sock.recv(4096):
                response += chunk

        return response.decode("utf-8")

    except ConnectionRefusedError:
        msg = f"Connection refused — is the executor running on {HOST}:{PORT}?"
        logger.error(msg)
        return f"Error: {msg}"
    except socket.timeout:
        msg = f"Socket timed out waiting for a response (timeout={timeout}s)"
        logger.error(msg)
        return f"Error: {msg}"
    except OSError as e:
        logger.error("Socket error: %s", e)
        return f"Error: {e}"

def _run_tool(tool_name: str, code: str, timeout: int = 10) -> str:
    """Log a tool call, execute it, log the response, and return the result."""
    logger.info("Tool called: %s", tool_name)
    logger.info("Code:\n%s", code)

    t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    text = f"\n#========== LLM Call ({t}): {tool_name}({str(timeout)}) ==========\n{code}"
    log_to_file(text)

    out = send_code(code, timeout)

    logger.info("Response:\n%s", out)

    text = f"\n#========== Python Response: ==========\n'''\n{out}'''"
    log_to_file(text)

    return out


def get_environment_info() -> str:
    """
    Retrieve information about the local Python execution environment.

    Returns details such as the Python version, installed packages,
    and other runtime properties of the executor process.

    Returns
    -------
    str
        A description of the current execution environment.
    """
    return _run_tool("get_environment_info", "__get_environment_info__")

def get_system_config() -> str:
    """
    Retrieve the Luminosa microscope system configuration.

    Returns
    -------
    str
        The current system configuration as a xml string.
    """
    return _run_tool("get_system_config", "__get_system_config__")


@mcp.tool()
def get_context() -> str:
    """
    Retrieve LumiPy library documentation as context for the current request.

    Call this before writing any LumiPy code so that the correct API,
    conventions, and examples are available.

    Returns
    -------
    str
        The full contents of LumiPy.md wrapped with instructional preamble,
        or an error message if the context file cannot be found.
    """
    logger.info("Tool called: get_context")

    context_file = os.path.join(os.path.dirname(__file__), "LumiPy.md")
    if not os.path.exists(context_file):
        msg = f"Context file not found: {CONTEXT_FILE}"
        logger.warning(msg)
        return f"Warning: {msg}"

    out = '''
# YOUR ROLE

Your are a help assistant for PicoQuant's Luminosa microscope system with access to a local python environment via MCP tools.
You answer user questions, provide system information and help to develop measurement scripts for workflow automation.
You can run or test generated code directly in the local python environment by calling the "execute_python_code" tool and check for its response.
To access the microscope hardware you use **LumiPy**, a Python interface for controlling and acquiring data from Luminosa.

'''
    with open(context_file, "r") as f:
        content = f.read()

    out += content
    out += "\n\n# Luminosa system configuration:\n\n"
    out += get_system_config()
    out += "\n\n# Information about the local python environment:\n\n"
    out += get_environment_info()
    out += "\n\nNow continue with the user request"
    return out

@mcp.tool()
def execute_python_code(code: str, timeout: int) -> str:
    """
    Execute Python code and return the captured output as a string.

    Every print statement in the code will be captured and returned.
    If an error occurs during execution, it is captured as part of the output.

    A resonable timeout appropriate for the code to be executed must be provided.
    If this timeout is exceeded, the function will return with a status message but the code is still running on the executor.
    To get the status of the running code (and all of its printed output to far) use the `get_last_response` tool.
    To abort the running code, use the `abort_code_execution` tool.

    Parameters
    ----------
    code : str
        The Python code to execute.
    timeout : int
        Maximum number of seconds to allow the code to run (default: 10).

    Returns
    -------
    str
        Captured stdout and any error messages from the execution.
    """
    return _run_tool("execute_python_code", code, timeout)

@mcp.tool()
def get_last_response() -> str:
    """
    Retrieve the output from the most recent code execution including partial output for a still-running code block.

    Useful when a previous execution has timed out or needs to be re-examined
    without re-running the code.

    Returns
    -------
    str
        The output produced by the last executed code block.
    """
    return _run_tool("get_last_response", "__get_last_output__")

@mcp.tool()
def abort_code_execution() -> str:
    """
    Abort the currently running code execution.

    Sends a signal to the executor to terminate the active execution thread.
    Use this if a code block is taking too long or has entered an infinite loop.

    Returns
    -------
    str
        A confirmation message indicating whether the abort succeeded.
    """
    return _run_tool("abort_code_execution", "__kill_execution__")

if __name__ == "__main__":
    mcp.run()
