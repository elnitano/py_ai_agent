import os
import subprocess
import sys
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    workpath = os.path.abspath(working_directory)
    path = os.path.join(working_directory, file_path)
    abspath = os.path.abspath(path)
    if not abspath.startswith(workpath):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(abspath):
        return f'Error: File "{file_path}" not found.'
    file_name, file_ext = os.path.splitext(file_path)
    if file_ext != ".py":
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        result = subprocess.run([sys.executable, abspath, *args], timeout=30, capture_output=True, cwd=working_directory)
    except Exception as e:
        return f"Error: executing Python file: {e}"

    outputs = []
    if result.stdout:
        outputs.append("STDOUT: " + result.stdout.decode(encoding='utf-8'))
    if result.stderr:
        outputs.append("STDERR: " + result.stderr.decode(encoding='utf-8'))
    if not outputs:
        return "No output produced."
    if result.returncode:
        outputs.append(f"Process exited with code {result.returncode}")
    return '\n'.join(outputs)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run tests.py",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Execute Python files with optional arguments.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional command-line arguments to pass to the Python file.",
                items=types.Schema(type=types.Type.STRING),
            ),
        },
    ),
)