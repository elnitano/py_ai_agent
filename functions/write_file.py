import os
from google.genai import types

def write_file(working_directory, file_path, content):
    workpath = os.path.abspath(working_directory)
    path = os.path.join(working_directory, file_path)
    abspath = os.path.abspath(path)
    if not abspath.startswith(workpath):
        return f'Error: Cannot write to "{abspath}" as it is outside the permitted working directory'
    try:
        os.makedirs(os.path.dirname(abspath), exist_ok=True)
    except OSError as e:
        return f"Error: {e.errno} - {e.strerror}"
    except Exception as e:
        return f'Error: An unexpected error occured: {e}'

    
    try:
        with open(abspath, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except OSError as e:
        return f"Error: {e.errno} - {e.strerror}"
    except Exception as e:
        return f'Error: An unexpected error occured: {e}'
    
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write or overwrite files.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The text content to write to the file.",
            ),
        },
    ),
)