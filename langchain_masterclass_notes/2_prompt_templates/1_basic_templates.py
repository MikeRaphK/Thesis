from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage

# # Template using a template string
# template = "Tell me a joke about {topic}."
# prompt_template = ChatPromptTemplate.from_template(template)

# print("-----Prompt from Template-----")
# prompt = prompt_template.invoke({"topic": "cats"})
# print(prompt)



# # Template using multiple placeholders
# template = """You are a helpful assistant.
# Human: Tell me a {adjective} story about a {animal}.
# Assistant:"""
# prompt_template = ChatPromptTemplate.from_template(template)
# prompt = prompt_template.invoke({"adjective": "funny", "animal": "panda"})
# print("-----Prompt from Template-----")
# print(prompt)



# System and human messages
messages = [
    ("system", "You are a comedian who tells jokes about {topic}."),
    ("human", "Tell me {joke_count} jokes"),
]

prompt_template = ChatPromptTemplate.from_messages(messages)
prompt = prompt_template.invoke({"topic": "lawyers", "joke_count": 3})
print("-----Prompt from Template-----")
print(prompt)



# #! THIS DOES NOT WORK!
# messages = [
#     ("system", "You are a comedian who tells jokes about {topic}."),
#     HumanMessage(content="Tell me {joke_count} jokes"),
# ]

# prompt_template = ChatPromptTemplate.from_messages(messages)
# prompt = prompt_template.invoke({"topic": "lawyers", "joke_count": 3})
# print("-----Prompt from Template-----")
# print(prompt)