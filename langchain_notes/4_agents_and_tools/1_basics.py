from langchain import hub
from langchain.agents import (
    AgentExecutor,
    create_react_agent,
)
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI

# This function will be used as a tool that returns the current time
def get_current_time(*args, **kwargs):
    """Returns the current military time in HH:MM:SS format."""
    from datetime import datetime
    return datetime.now().strftime("%H:%M:%S")

# List of tools available to the agent
tools = []
current_time_tool = Tool(
    name="Time",
    func=get_current_time,
    description="Useful for when you need to know the current time"
)
tools.append(current_time_tool)

# Pull the prompt template from the hub. This prompt follows ReAct = Reason and Action
# https://smith.langchain.com/hub/hwchase17/react
prompt = hub.pull("hwchase17/react")

# Create the model
model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Create a ReAct agent
agent = create_react_agent(llm=model, tools=tools, prompt=prompt, stop_sequence=True)

# Create the agent executor
agent_executor = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=True)

# Run the agent
response = agent_executor.invoke({"input" : "What time is it?"})
print(f"ChatGPT-4o-mini: {response['output']}")
