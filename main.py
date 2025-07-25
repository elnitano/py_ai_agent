import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file
from functions.call_function import call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file,
    ]
)

MAX_LOOPS = 20

def main():
    argvlen = len(sys.argv)
    user_prompt = ""
    if argvlen < 2:
        exit("No argument given!")
    if argvlen >= 2:
        user_prompt = sys.argv[1]
        
    if user_prompt:
        messages = [
            types.Content(role="user", parts=[types.Part(text=user_prompt)])
            ]
        
        for i in range(MAX_LOOPS):
            try:
                aitest = client.models.generate_content(
                    model="gemini-2.0-flash-001", 
                    contents=messages,
                    config=types.GenerateContentConfig(
                        tools=[available_functions],
                        system_instruction=system_prompt, ),
                )
                useverbose = False
                if argvlen >= 3:
                    if sys.argv[2] == "--verbose":
                        useverbose = True
                        print(f"User prompt: {user_prompt}")
                        print(f"Prompt tokens: {aitest.usage_metadata.prompt_token_count}")
                        print(f"Response tokens: {aitest.usage_metadata.candidates_token_count}")

                has_function_calls = False
                for candidate in aitest.candidates:
                    messages.append(candidate.content)
                    for part in candidate.content.parts:
                        if part.function_call:
                            has_function_calls = True
                            break

                if not has_function_calls and aitest.text:
                    print(f"Final response:")
                    print(aitest.text)
                    break

                for candidates in aitest.candidates:
                    for parts in candidates.content.parts:
                        if parts.function_call:
                            function_call_result = call_function(parts.function_call, useverbose)
                            if (function_call_result and
                                function_call_result.parts and
                                function_call_result.parts[0] and
                                function_call_result.parts[0].function_response):

                                messages.append(types.Content(role="tool", parts=function_call_result.parts))

                                if useverbose:                    
                                    print(f"-> {function_call_result.parts[0].function_response.response}")
                            else:
                                raise Exception("Function Call failed: Missing function response!")
                        elif parts.text:
                            print(parts.text)
            
            except Exception as e:
                print(f"Critical error during AI Calling, error {e}")
                break



if __name__ == "__main__":
    main()
