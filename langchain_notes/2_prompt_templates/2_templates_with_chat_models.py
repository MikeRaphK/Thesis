from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

# Create the model
model = ChatOpenAI(model="gpt-4o-mini")

# Template using a template string
print("-----Prompt from template-----")
template = "Tell me a joke about {topic}."
prompt_template = ChatPromptTemplate.from_template(template)
prompt = prompt_template.invoke({"topic": "cats"})
result = model.invoke(prompt)
response = result.content
print(f"ChatGPT-4o-mini: {response}")


# Template using multiple placeholders
print("-----Prompt from template with multiple placeholders-----")
template = """You are a helpful assistant.
Human: Tell me a {adjective} story about a {animal}.
Assistant:"""
prompt_template = ChatPromptTemplate.from_template(template)
prompt = prompt_template.invoke({"adjective": "funny", "animal": "panda"})
result = model.invoke(prompt)
response = result.content
print(f"ChatGPT-4o-mini: {response}")

# Template with system and human messages
print("-----Prompt from template with system and human messages-----")
messages = [
    ("system", "You are a comedian who tells jokes about {topic}."),
    ("human", "Tell me {joke_count} jokes"),
]
prompt_template = ChatPromptTemplate.from_messages(messages)
prompt = prompt_template.invoke({"topic": "lawyers", "joke_count": 3})
result = model.invoke(prompt)
response = result.content
print(f"ChatGPT-4o-mini: {response}")
