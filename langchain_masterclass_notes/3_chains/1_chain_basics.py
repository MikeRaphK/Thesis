from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain_openai import ChatOpenAI

# Create the model
model = ChatOpenAI(model="gpt-4o-mini")

# Define prompt templates
messages = [
    ("system", "You are a comedian who tells jokes about {topic}."),
    ("human", "Tell me {joke_count} jokes"),
]
prompt_template = ChatPromptTemplate.from_messages(messages)

# Create a chain and make output readable
chain = prompt_template | model | StrOutputParser()

# Run the chain
result = chain.invoke({"topic": "dogs", "joke_count": 3})
print(result)