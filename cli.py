import argparse
import importlib.util
from pathlib import Path
from dotenv import load_dotenv

# 📁 Dynamically load tools from the 'tools' directory
def load_tools():
    tools = {}
    tools_directory = Path("tools")
    if tools_directory.exists() and tools_directory.is_dir():
        for tool_file in tools_directory.glob("*.py"):
            module_name = tool_file.stem
            spec = importlib.util.spec_from_file_location(module_name, tool_file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            tools[module_name] = module
    return tools

load_dotenv()

# 🖥️ CLI Setup
parser = argparse.ArgumentParser(description="🧠 Consulting Assistant CLI")

# Dynamically add all tools in the 'tools' directory as subcommands
tools = load_tools()
for tool_name in tools:
    # Add a default option for each tool, but for --run_chain, allow it to take a filename
    if tool_name == "run_chain":
        parser.add_argument(f'--{tool_name}', type=str, help=f"Run {tool_name} tool with a YAML file path")  # Erwartet einen Pfad
    else:
        parser.add_argument(f'--{tool_name}', action='store_true', help=f"Run {tool_name} tool")

args = parser.parse_args()

# Execute the corresponding tool based on CLI argument
for tool_name, tool in tools.items():
    if getattr(args, tool_name):
        print(f"Running tool: {tool_name}")
        if tool_name == "run_chain" and args.run_chain:
            # Wenn das Tool 'run_chain' ist, übergebe den Pfad der YAML-Datei
            tool.run(args.run_chain)
        else:
            tool.run()  # Für alle anderen Tools ohne zusätzliche Argumente
