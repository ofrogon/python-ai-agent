import os
import argparse
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from functions.call_function import available_functions, call_function

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if api_key == None:
        raise RuntimeError("Missing api_key value")

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    client = genai.Client(api_key=api_key)

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    for _ in range(20):
        response = agent_loop(args, client, messages)

        if response.function_calls == None:
            print(response.text)
            sys.exit(0)

    print("Error: the maximum loop that the agent can do have been done without result, stopping the process now!")
    sys.exit(1)


def agent_loop(args, client, messages):
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt
        )
    )
    if response.usage_metadata == None:
        raise RuntimeError("Fail to communicate with Gemini API")

    if response.candidates != None:
        for response_candidate in presponse.candidates:
            messages.append(response_candidate.content)

    if (args.verbose):
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


    function_results = []
    if response.function_calls != None:
        for function_call in response.function_calls:
            function_call_result = call_function(function_call)
            if function_call_result.parts == None:
                raise Exception("Missing parts section from function_call_result")

            if function_call_result.parts[0].function_response == None:
                raise Exception("Missing .function_response from function_call_result.parts[0]")

            if function_call_result.parts[0].function_response.response == None:
                raise Exception("Missing .function_response.response from function_call_result.parts[0]")

            function_results.append(function_call_result.parts[0])

            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")

    messages.append(types.Content(role="user", parts=function_results))

    return response

if __name__ == "__main__":
    main()
