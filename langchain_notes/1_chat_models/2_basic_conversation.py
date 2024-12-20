from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

# Create the model
model = ChatOpenAI(model="gpt-4o-mini")

# SystemMessage: Message to manage AI behavior
# HumanMessage: Message from a human to the AI model
messages = [
    SystemMessage(content="Solve the following math problems"),
    HumanMessage(content="What is 81 divided by 9?"),
]

# Invoke the model with a message
result = model.invoke(messages)
print(f"ChatGPT-4o-mini: {result.content}")

# # AIMessage: Response from an AI
# messages = [
#     SystemMessage(content="Solve the following math problems"),
#     HumanMessage(content="What is 81 divided by 9?"),
#     AIMessage(content="81 divided by 9 is 9."),
#     HumanMessage(content="What is 10 times 5?"),
# ]
# # Invoke the model with a message
# result = model.invoke(messages)
# print(f"ChatGPT-4o-mini: {result.content}")