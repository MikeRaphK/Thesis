# ChatGPT has very restricted capabilities. For example, it cannot access the web
# For that reason, we give it 'tools'. These tools are custom functions that help
# the LLM to interact with external systems
# The model never actually executes functions itself, it simply generates parameters

from openai import OpenAI
from datetime import datetime
import json

client = OpenAI()

# This is the function that we want the model to be able to call
def get_password(username: str) -> str:
    if username == "Mike":
        return "SuperDuperDifficultPassword"
    elif username == "John":
        return "SimplePassword"
    else:
        return "UnknownUser"

llm_get_password = {
    "name": "get_password",
    "description": "Get the password of a given user. Call this whenever you need to know the password, for example when a user asks 'What is my password?'",
    "parameters": {
        "type": "object",
        "properties": {
            "username": {
                "type": "string",
                "description": "The user's username.",
            },
        },
        "required": ["username"],
        "additionalProperties": False,
    },
}
llm_functions = []
llm_functions.append(llm_get_password)

messages=[]
messages.append({"role": "system", "content": "You are a helpful assistant! Use the supplied functions to assist the user."})
messages.append({"role": "user", "content": "Hello, can you tell me what my password is?"})
messages.append({"role": "assistant", "content": "Hello! Certainly! Can you tell me what your username is?"})
messages.append({"role": "assistant", "content": "My username is Mike"})

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
    functions=llm_functions,
    function_call="auto",
)

response_message = response.choices[0].message

# If a function call was made,
if dict(response_message).get("function_call"):
    # Extract the arguments
    json_response = json.loads(response_message.function_call.arguments)
    username = json_response["username"]
    # Call the function
    print(f"The function output is: {get_password(username=username)}")
# Else, print the message
else:
    print(response_message.content)