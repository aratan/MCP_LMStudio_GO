# mcp_time_stdio.py
import json
import sys
from datetime import datetime

try:
    from zoneinfo import ZoneInfo
except ImportError:
    from backports.zoneinfo import ZoneInfo

def read_message():
    length = int.from_bytes(sys.stdin.buffer.read(4), 'big')
    msg = sys.stdin.buffer.read(length)
    return json.loads(msg.decode('utf-8'))

def write_message(msg):
    data = json.dumps(msg).encode('utf-8')
    sys.stdout.buffer.write(len(data).to_bytes(4, 'big'))
    sys.stdout.buffer.write(data)
    sys.stdout.flush()

while True:
    try:
        req = read_message()
        method = req.get("method")
        rid = req.get("id")

        if method == "get_tool_list":
            write_message({
                "jsonrpc": "2.0",
                "id": rid,
                "result": {
                    "tools": [{
                        "name": "get_current_time",
                        "description": "Hora actual en España",
                        "inputSchema": {"type": "object", "properties": {}, "required": []}
                    }]
                }
            })

        elif method == "call_tool":
            write_message({
                "jsonrpc": "2.0",
                "id": rid,
                "result": {
                    "content": [{
                        "type": "text",
                        "text": f"Hora en España: {datetime.now(ZoneInfo('Europe/Madrid')).strftime('%Y-%m-%d %H:%M:%S %Z')}"
                    }]
                }
            })

    except Exception:
        break