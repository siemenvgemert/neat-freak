import sys
import json
import os
import shutil

# Ensure scripts directory is in sys.path for direct module reuse
SCRIPTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts"))
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

try:
    import audit_workspace
    import harvest_debt
    import inspect_deps
    import pre_commit_check
except ImportError:
    audit_workspace = None
    harvest_debt = None
    inspect_deps = None
    pre_commit_check = None

def log(msg):
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
                "version": "1.1.0"
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
                    "name": "audit_workspace",
                    "description": "Performs an instantaneous cleanliness audit of the workspace using fast os.scandir traversal, returning a 0-100 Cleanliness Scorecard and cleanup plan in 1 turn.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "workspace_path": {
                                "type": "string",
                                "description": "Absolute path to the workspace root to audit."
                            },
                            "mode": {
                                "type": "string",
                                "description": "Intensity mode ('on', 'ocd', or 'off'). Defaults to configured project mode.",
                                "enum": ["on", "ocd", "off"]
                            }
                        },
                        "required": ["workspace_path"]
                    }
                },
                {
                    "name": "harvest_debt",
                    "description": "Harvests all ponytail and neat-freak simplification comments across all workspace source files in milliseconds, compiling a structured Layout Debt Ledger.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "workspace_path": {
                                "type": "string",
                                "description": "Absolute path to the workspace root to scan."
                            },
                            "write_file": {
                                "type": "boolean",
                                "description": "Whether to write the ledger directly to layout_debt.md in the workspace root. Default is false."
                            }
                        },
                        "required": ["workspace_path"]
                    }
                },
                {
                    "name": "inspect_dependencies",
                    "description": "Analyzes import statements via Python AST and multi-language parsers to detect circular dependencies and layer boundary violations in milliseconds.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "workspace_path": {
                                "type": "string",
                                "description": "Absolute path to the workspace root to analyze."
                            }
                        },
                        "required": ["workspace_path"]
                    }
                },
                {
                    "name": "review_layout",
                    "description": "Reviews new, modified, or staged files against neat-freak placement guidelines (no root source files, nesting limits) returning a PASS/FAIL table.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "workspace_path": {
                                "type": "string",
                                "description": "Absolute path to the workspace root."
                            },
                            "files": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Optional list of specific relative file paths to evaluate. If omitted, evaluates working tree changes."
                            }
                        },
                        "required": ["workspace_path"]
                    }
                },
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
                    "description": "Recursively deletes all empty directories in the workspace using high-speed traversal (skipping .git folders).",
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
    if name == "audit_workspace":
        ws_path = arguments.get("workspace_path")
        if not ws_path or not os.path.exists(ws_path):
            return "Error: Workspace path does not exist."
        mode = arguments.get("mode") or (audit_workspace.resolve_mode(ws_path) if audit_workspace else "on")
        if audit_workspace:
            res = audit_workspace.scan_workspace(ws_path, mode)
            return audit_workspace.format_markdown(res)
        return "Error: audit_workspace module not available."

    elif name == "harvest_debt":
        ws_path = arguments.get("workspace_path")
        if not ws_path or not os.path.exists(ws_path):
            return "Error: Workspace path does not exist."
        write_file = arguments.get("write_file", False)
        if harvest_debt:
            records = harvest_debt.harvest_debt(ws_path)
            content = harvest_debt.format_markdown(records)
            if write_file:
                out_path = os.path.join(ws_path, "layout_debt.md")
                with open(out_path, "w", encoding="utf-8") as f:
                    f.write(content + "\n")
                return f"Successfully updated {out_path} ({len(records)} entries found):\n\n" + content
            return content
        return "Error: harvest_debt module not available."

    elif name == "inspect_dependencies":
        ws_path = arguments.get("workspace_path")
        if not ws_path or not os.path.exists(ws_path):
            return "Error: Workspace path does not exist."
        if inspect_deps:
            res = inspect_deps.inspect_dependencies(ws_path)
            return inspect_deps.format_markdown(res)
        return "Error: inspect_deps module not available."

    elif name == "review_layout":
        ws_path = arguments.get("workspace_path")
        if not ws_path or not os.path.exists(ws_path):
            return "Error: Workspace path does not exist."
        files = arguments.get("files")
        if pre_commit_check:
            mode = pre_commit_check.resolve_mode(ws_path)
            if not files:
                files = pre_commit_check.get_git_files(working_tree=True)
            results = pre_commit_check.check_files(files, mode)
            lines = [f"### Neat Freak Placement Review (Mode: {mode.upper()})\n"]
            if not results:
                lines.append("No modified files detected to review.")
            else:
                lines.append("| File Path | Status | Finding / Recommendation |")
                lines.append("|---|---|---|")
                for r in results:
                    lines.append(f"| `{r['file']}` | **{r['status']}** | {r['reason']} |")
            return "\n".join(lines)
        return "Error: pre_commit_check module not available."

    elif name == "flatten_directory":
        dir_path = arguments.get("directory_path")
        if not dir_path or not os.path.exists(dir_path):
            return "Error: Directory path does not exist."
        try:
            children = [c for c in os.listdir(dir_path) if c != '.DS_Store']
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
            # Fast post-order traversal using os.scandir
            def clean_empty_dirs(path):
                try:
                    entries = list(os.scandir(path))
                except (PermissionError, FileNotFoundError):
                    return
                for e in entries:
                    if e.is_dir(follow_symlinks=False) and e.name != ".git":
                        clean_empty_dirs(e.path)
                try:
                    remaining = [e.name for e in os.scandir(path) if e.name != ".DS_Store"]
                    if not remaining and path != ws_path:
                        ds_store = os.path.join(path, ".DS_Store")
                        if os.path.exists(ds_store):
                            os.remove(ds_store)
                        os.rmdir(path)
                        pruned.append(path.replace("\\", "/"))
                except Exception:
                    pass

            clean_empty_dirs(ws_path)
            if not pruned:
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
            if not cleared_items:
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
    log("neat-freak-mcp server started (v1.1.0)")
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
            elif method == "ping":
                resp = {"jsonrpc": "2.0", "id": req_id, "result": {}}
            
            if resp and req_id is not None:
                sys.stdout.write(json.dumps(resp) + "\n")
                sys.stdout.flush()
        except Exception as e:
            log(f"Error handling request: {str(e)}")

if __name__ == "__main__":
    main()
