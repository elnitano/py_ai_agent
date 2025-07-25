import os
from google.genai import types

def get_files_info(working_directory, directory="."):
	workpath = os.path.abspath(working_directory)
	path = os.path.join(working_directory, directory)
	abspath = os.path.abspath(path)
	if not abspath.startswith(workpath):
		return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
	if not os.path.isdir(abspath):
		return f'Error: "{directory}" is not a directory'
	curpath = os.listdir(abspath)
	buildlist = []
	for objects in curpath:
		object_path = os.path.join(abspath, objects)
		buildlist.append(f"- {objects}: file_size={os.path.getsize(object_path)} bytes, is_dir={os.path.isdir(object_path)}")
	return "\n".join(buildlist)

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
