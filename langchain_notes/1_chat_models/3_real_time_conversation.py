from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

# Create the model
model = ChatOpenAI(model="gpt-4o-mini")

chat_history = []

system_mesage = SystemMessage(content="You are a helpful AI assistant that answers questions in 2-3 sentences.")
chat_history.append(system_mesage)

while True:
    # Read user input
    query = input("You: ")
    if query.lower() == "exit":
        break
    chat_history.append(HumanMessage(content=query))

    # Get AI response using history
    result = model.invoke(chat_history)
    response = result.content
    chat_history.append(AIMessage(content=response))
    print(f"ChatGPT-4o-mini: {response}")

print("----- Message History -----")
for message in chat_history:
    print(message)