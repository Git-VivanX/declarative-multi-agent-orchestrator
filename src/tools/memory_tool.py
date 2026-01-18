import json
import os

FILE = "src/memory/store.json"

def memory_tool(action, key=None, value=None):
    if not os.path.exists(FILE):
        with open(FILE, "w") as f:
            json.dump({}, f)

    with open(FILE, "r+") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = {}

        if action == "write":
            data[key] = value
            f.seek(0)
            json.dump(data, f, indent=2)
            f.truncate()
        elif action == "read":
            return data.get(key)