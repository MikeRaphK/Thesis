from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent

# Initialize model
import os
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(model="gpt-4o-mini", openai_api_key=OPENAI_API_KEY)

# File writing tool
@tool
def write_to_file_tool(content : str) -> str:
    """
    Writes content to a file.
    """
    with open("./foo.txt", "w") as f:
        f.write(content)
    return f"File 'foo.txt' has been successfully created and written to."


# Initialize agent that will call the tool
tools = []
tools.append(write_to_file_tool)
agent = initialize_agent(
    tools=tools,
    llm=llm,
    verbose=True  # Enables logs
)

prompt = """ Please write the following to foo.txt program:\n
The quick brown fox jumps over the lazy dog
"""

response = agent.run(prompt)
print(response)