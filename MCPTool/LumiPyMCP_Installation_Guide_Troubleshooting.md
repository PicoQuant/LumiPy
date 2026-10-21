# LumiPyMCP – Installation Guide (Windows)

> \*\*Warning:\*\* LumiPyMCP is experimental. It lets an AI agent run Python code against your Luminosa system, including lasers and scanners. Read `MCPTool/Disclaimer.md` before use and review any generated code before letting it run on real samples.

## How it works

```
Claude Desktop  ──(starts)──>  lumipy\_mcp\_server.py  ──(TCP 127.0.0.1:65432)──>  lumipy\_rce\_server.py (running in Luminosa PyEdit)
```

You need two parts:

1. **The MCP server.** Claude Desktop starts it through `uv`.
2. **The RCE server.** You start it yourself inside Luminosa.

**Requirement:** Claude Desktop must run **on the microscope PC**, because the MCP server connects to `127.0.0.1`. For a remote setup, see [Remote setup](#remote-setup-optional).

\---

## Step 1 – Install uv

Open **CMD** or **PowerShell** and run:

```bash
winget install --id=astral-sh.uv -e
```

Then **close and reopen** the terminal and check that it worked:

```bash
uv --version
where uv
```

Note the path that `where uv` prints. You may need it in Step 3B. Typical locations:

* `C:\\Users\\<user>\\AppData\\Local\\Microsoft\\WinGet\\Packages\\astral-sh.uv\_Microsoft.Winget.Source\_8wekyb3d8bbwe\\uv.exe`
* `C:\\Users\\<user>\\AppData\\Local\\Microsoft\\WinGet\\Links\\uv.exe`
* `C:\\Users\\<user>\\.local\\bin\\uv.exe` (if installed with the PowerShell script)

If `uv` isn't found, add its folder to your user **Path** under *Environment Variables*, then open a new terminal.

\---

## Step 2 – Pre-load dependencies (important)

On first start, uv downloads Python and `fastmcp` (about 70 packages). This can take longer than Claude Desktop waits, and Claude then shows **"Unable to connect to extension server"**.

To avoid that, run the server **once by hand** first:

```bash
uv run --with fastmcp https://raw.githubusercontent.com/PicoQuant/LumiPy/v1.1.0-rc3/MCPTool/lumipy\_mcp\_server.py
```

or, using a local copy:

```bash
uv run --with fastmcp "C:\\path\\to\\LumiPy\\MCPTool\\lumipy\_mcp\_server.py"
```

It worked when you see:

```
Hostname: <PC-NAME> (127.0.0.1:65432)
... FastMCP banner ...
INFO  Starting MCP server 'LumiPyMCPTool' with transport 'stdio'
```

Then stop it with **Ctrl+C**. The packages are now cached, so later starts are fast.

\---

## Step 3 – Connect Claude Desktop

Choose **one** option, either A or B. Don't use both at once.

### Option A – One-click extension (recommended)

1. Download `LumiPyMCP-<version>.mcpb` from the [Releases page](https://github.com/PicoQuant/LumiPy/releases).
2. Double-click it, or go to **Settings → Extensions → Install Extension**.
3. Quit Claude completely and restart it (see the tip below).
4. Check **Settings → Connectors → LumiPyMCP**: it should be *Enabled* with no red error.

Notes:

* The extension downloads `lumipy\_mcp\_server.py` from GitHub on every start, so the PC needs access to `raw.githubusercontent.com`.
* The extension calls `uv` by name, so `uv` must be on the PATH that Claude Desktop sees.

### Option B – Manual config (offline, editable, or if Option A fails)

1. In Claude Desktop, go to **Settings → Developer → Edit config**. This opens the config file the app actually uses.

   * Don't look for the file by hand. On Store/MSIX installs it is **not** in `%APPDATA%\\Claude` but in
`%LOCALAPPDATA%\\Packages\\Claude\_<id>\\LocalCache\\Roaming\\Claude\\`.
2. **Quit Claude completely first** (see the tip below). Otherwise Claude overwrites your changes when it closes.
3. Add an `mcpServers` entry **as a top-level key** in the existing JSON object. Use the **full path to `uv.exe`** and **double backslashes**:

```json
{
  "mcpServers": {
    "LumiPyMCPTool": {
      "command": "C:\\\\Users\\\\<user>\\\\AppData\\\\Local\\\\Microsoft\\\\WinGet\\\\Packages\\\\astral-sh.uv\_Microsoft.Winget.Source\_8wekyb3d8bbwe\\\\uv.exe",
      "args": \[
        "run", "--with", "fastmcp",
        "C:\\\\path\\\\to\\\\LumiPy\\\\MCPTool\\\\lumipy\_mcp\_server.py"
      ]
    }
  },
  "preferences": { "...existing content stays unchanged...": true }
}
```

4. Save in Notepad with **Save as type: All files** and **Encoding: UTF-8**, so the file stays `.json` and doesn't become `.json.txt`.
5. Start Claude and check **Settings → Developer**. **LumiPyMCPTool** should be listed as running.

> \*\*Tip – quitting Claude completely:\*\* close the window, then right-click the tray icon → \*\*Quit\*\*. If in doubt, open Task Manager (Ctrl+Shift+Esc) and end every \*Claude\* process.

\---

## Step 4 – Start the RCE server in Luminosa (required every session)

1. Start the Luminosa software and open **PyEdit**.
2. Pick a Python environment, ideally one with **only numpy** installed, to limit what generated code can do.
3. Open and run `MCPTool\\lumipy\_rce\_server.py`. Leave it running for the whole session.
4. To disconnect the agent, stop the script.

\---

## Step 5 – Test

In a new Claude chat:

> \*Use LumiPyMCPTool to get the context and print the Luminosa version.\*

If you get **"Connection refused — is the executor running on 127.0.0.1:65432?"**, the RCE server from Step 4 is not running.

\---

## Troubleshooting

|Symptom|Cause|Fix|
|-|-|-|
|Connector shows *"Unable to connect to extension server"*|First start too slow (uv downloading packages)|Run Step 2 once, then restart Claude|
|Same error after Step 2|Claude can't find `uv` on its PATH (e.g. uv was installed while Claude was running)|Quit Claude completely and restart it; sign out of Windows and back in; or use Option B with the full `uv.exe` path|
|*Settings → Developer* shows *"No servers added"*|Config not saved, or invalid JSON|See the rows below|
|Changes to the config file disappear|Claude was still running and overwrote the file|End all Claude processes in Task Manager **before** editing|
|Config file not found under `%APPDATA%\\Claude`|Store/MSIX install of Claude Desktop|Use **Settings → Developer → Edit config**|
|Config edited but ignored|Common JSON mistakes: single `\\` in paths; `mcpServers` pasted as a **second `{ }` block** instead of a key; missing or extra comma; `{your path}` placeholder left in; file saved as `.json.txt`|Fix the JSON and check it in a JSON validator|
|Two LumiPy entries / odd behaviour|Extension (A) and manual config (B) both active|Keep only one|
|Agent says *Connection refused*|RCE server not running in Luminosa|Run `lumipy\_rce\_server.py` in PyEdit (Step 4)|

**Logs:** **Settings → Developer → Open Logs Folder** → `mcp-server-LumiPyMCP\*.log`. The last lines show the exact error.

\---

## Remote setup (optional)

To run Claude on a different PC than the microscope:

1. Use **Option B** with a local copy of `lumipy\_mcp\_server.py`.
2. In that file, change `HOST = "127.0.0.1"` to the microscope PC's IP address.
3. Allow TCP port **65432** through the firewall on the microscope PC.
4. Check that `lumipy\_rce\_server.py` listens on the network interface and not only on localhost.

## Other clients

* **Browser chatbots (ChatGPT, Gemini, …):** use the *MCP SuperAssistant* browser extension with `fastmcp\_config.json`. Run it with `npx @srbhptl39/mcp-superassistant-proxy@latest --config .\\fastmcp\_config.json`.
* **LM Studio (local models):** Developer tab → `mcp.json`. Add the same `mcpServers` block as in Option B.

