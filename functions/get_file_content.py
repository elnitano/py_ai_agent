import os
from . import func_config
from google.genai import types

def get_file_content(working_directory, file_path):
    workpath = os.path.abspath(working_directory)
    path = os.path.join(working_directory, file_path)
    abspath = os.path.abspath(path)
    if not abspath.startswith(workpath):
        return f'Error: Cannot read "{abspath}" as it is outside the permitted working directory'
    if not os.path.isfile(abspath):
        return f'Error: File not found or is not a regular file: "{abspath}"'
    
    file = ""
    try:
        with open(abspath, "r") as f:
            file = f.read(func_config.MAX_CHARS)
    except IOError as e:
        return f"Error: {e.errno} - {e.strerror}"
    except FileNotFoundError:
        return f'Error: File not found or is not a regular file: "{abspath}"'
    except Exception as e:
        return f'Error: An unexpected error occured: {e}'
    
    if len(file) >= 10000:
        file = file + f'[...File "{abspath}" truncated at 10000 characters]'

    return file

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read file contents.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to read.",
            ),
        },
    ),
)
    