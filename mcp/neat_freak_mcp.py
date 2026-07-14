import sys
import json
import os
import shutil

def log(msg):
    # Print to stderr for logging/debugging (does not interfere with stdout JSON-RPC)
    sys.stderr.write(f"LOG: {msg}\n")
    sys.stderr.flush()

def handle_initialize(req_id, params):
    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "result": {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {}
            },
            "serverInfo": {
                "name": "neat-freak-mcp",
                "version": "1.0.0"
            }
        }
    }

def handle_tools_list(req_id):
    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "result": {
            "tools": [
                {
                    "name": "flatten_directory",
                    "description": "Moves all files in a single-child nested directory up and deletes the empty parent folder.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "directory_path": {
                                "type": "string",
                                "description": "Absolute path to the parent directory to flatten."
                            }
                        },
                        "required": ["directory_path"]
                    }
                },
                {
                    "name": "prune_empty_folders",
                    "description": "Recursively deletes all empty directories in the workspace (skipping .git folders).",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "workspace_path": {
                                "type": "string",
                                "description": "Absolute path to the workspace root to prune."
                            }
                        },
                        "required": ["workspace_path"]
                    }
                },
                {
                    "name": "clear_scratch_directory",
                    "description": "Deletes all files and folders inside the scratch/ directory to clean up experimental code.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "workspace_path": {
                                "type": "string",
                                "description": "Absolute path to the workspace root containing the scratch/ folder."
                            }
                        },
                        "required": ["workspace_path"]
                    }
                },
                {
                    "name": "clear_agent_sandbox",
                    "description": "Deletes a specific agent's isolated subfolder inside the scratch/ directory.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "workspace_path": {
                                "type": "string",
                                "description": "Absolute path to the workspace root containing the scratch/ folder."
                            },
                            "sandbox_name": {
                                "type": "string",
                                "description": "The name of the agent subfolder to delete (e.g. 'researcher' or 'coder')."
                            }
                        },
                        "required": ["workspace_path", "sandbox_name"]
                    }
                }
            ]
        }
    }

def call_tool(name, arguments):
    if name == "flatten_directory":
        dir_path = arguments.get("directory_path")
        if not dir_path or not os.path.exists(dir_path):
            return "Error: Directory path does not exist."
        try:
            children = os.listdir(dir_path)
            children = [c for c in children if c != '.DS_Store']
            if len(children) != 1:
                return "Error: Directory does not contain exactly one child folder."
            child_name = children[0]
            child_path = os.path.join(dir_path, child_name)
            if not os.path.isdir(child_path):
                return "Error: Child item is a file, not a directory."
            for item in os.listdir(child_path):
                shutil.move(os.path.join(child_path, item), os.path.join(dir_path, item))
            os.rmdir(child_path)
            return f"Successfully flattened {child_name} into {dir_path}"
        except Exception as e:
            return f"Error flattening directory: {str(e)}"
    elif name == "prune_empty_folders":
        ws_path = arguments.get("workspace_path")
        if not ws_path or not os.path.exists(ws_path):
            return "Error: Workspace path does not exist."
        try:
            pruned = []
            for root, dirs, files in os.walk(ws_path, topdown=False):
                # Skip .git paths
                parts = root.split(os.sep)
                if '.git' in parts:
                    continue
                items = os.listdir(root)
                items = [i for i in items if i != '.DS_Store']
                if len(items) == 0:
                    ds_store = os.path.join(root, '.DS_Store')
                    if os.path.exists(ds_store):
                        os.remove(ds_store)
                    os.rmdir(root)
                    pruned.append(root)
            if len(pruned) == 0:
                return "No empty directories found."
            return "Successfully deleted the following empty folders:\n" + "\n".join(pruned)
        except Exception as e:
            return f"Error pruning empty folders: {str(e)}"
    elif name == "clear_scratch_directory":
        ws_path = arguments.get("workspace_path")
        if not ws_path or not os.path.exists(ws_path):
            return "Error: Workspace path does not exist."
        scratch_path = os.path.join(ws_path, "scratch")
        if not os.path.exists(scratch_path):
            return "Error: scratch/ folder does not exist in this workspace."
        try:
            cleared_items = []
            for item in os.listdir(scratch_path):
                item_path = os.path.join(scratch_path, item)
                if os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                else:
                    os.remove(item_path)
                cleared_items.append(item)
            if len(cleared_items) == 0:
                return "scratch/ directory was already empty."
            return f"Successfully cleared the following files/folders from scratch/:\n" + "\n".join(cleared_items)
        except Exception as e:
            return f"Error clearing scratch directory: {str(e)}"
    elif name == "clear_agent_sandbox":
        ws_path = arguments.get("workspace_path")
        sandbox_name = arguments.get("sandbox_name")
        if not ws_path or not os.path.exists(ws_path):
            return "Error: Workspace path does not exist."
        if not sandbox_name:
            return "Error: Sandbox name is required."
        target_path = os.path.join(ws_path, "scratch", sandbox_name)
        # Prevent directory traversal
        resolved_target = os.path.abspath(target_path)
        resolved_scratch = os.path.abspath(os.path.join(ws_path, "scratch"))
        if not resolved_target.startswith(resolved_scratch) or resolved_target == resolved_scratch:
            return "Error: Invalid sandbox name. Cannot delete directories outside of scratch/."
        if not os.path.exists(target_path):
            return f"Error: Sandbox folder '{sandbox_name}' does not exist inside scratch/."
        try:
            if os.path.isdir(target_path):
                shutil.rmtree(target_path)
            else:
                os.remove(target_path)
            return f"Successfully deleted agent sandbox folder: {sandbox_name}"
        except Exception as e:
            return f"Error clearing agent sandbox: {str(e)}"
    else:
        return f"Error: Tool {name} not found."

def handle_tools_call(req_id, params):
    name = params.get("name")
    arguments = params.get("arguments", {})
    text_result = call_tool(name, arguments)
    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "result": {
            "content": [
                {
                    "type": "text",
                    "text": text_result
                }
            ]
        }
    }

def main():
    log("neat-freak-mcp server started")
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        try:
            req = json.loads(line)
            method = req.get("method")
            req_id = req.get("id")
            params = req.get("params", {})
            
            resp = None
            if method == "initialize":
                resp = handle_initialize(req_id, params)
            elif method == "tools/list":
                resp = handle_tools_list(req_id)
            elif method == "tools/call":
                resp = handle_tools_call(req_id, params)
            
            if resp:
                sys.stdout.write(json.dumps(resp) + "\n")
                sys.stdout.flush()
        except Exception as e:
            log(f"Error handling request: {str(e)}")

if __name__ == "__main__":
    main()
