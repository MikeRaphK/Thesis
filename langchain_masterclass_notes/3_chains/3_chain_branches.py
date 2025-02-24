from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnableBranch
from langchain_openai import ChatOpenAI

# Create the model
model = ChatOpenAI(model="gpt-4o-mini")

# Define prompt templates
positive_messages = [
    ("system", "You are a helpful assistant."),
    ("human", "Generate a thank you note for this positive feedback: {feedback}"),
]
positive_feedback_template = ChatPromptTemplate.from_messages(positive_messages)

negative_messages = [
    ("system", "You are a helpful assistant."),
    ("human", "Generate a response addressing this negative feedback: {feedback}"),
]
negative_feedback_template = ChatPromptTemplate.from_messages(negative_messages)

neutral_messages = [
    ("system", "You are a helpful assistant."),
    ("human", "Generate a request for more details for this neutral feedback: {feedback}"),
]
neutral_feedback_template = ChatPromptTemplate.from_messages(neutral_messages)

escalate_messages = [
    ("system", "You are a helpful assistant."),
    ("human", "Generate a message to escalate this feedback to a human agent: {feedback}"),
]
escalate_feedback_template = ChatPromptTemplate.from_messages(escalate_messages)

# Define a feedback classification template
classification_messages = [
    ("system", "You are a helpful assistant."),
    ("human", "Classify the sentiment of this feedback as positive, negative, neutral, or escalate: {feedback}"),
]
classification_template = ChatPromptTemplate.from_messages(classification_messages)

# Define the runnable branches
branches = RunnableBranch(
    (lambda x: "positive" in x, positive_feedback_template | model | StrOutputParser()),
    (lambda x: "negative" in x, negative_feedback_template | model | StrOutputParser()),
    (lambda x: "neutral" in x, neutral_feedback_template | model | StrOutputParser()),
    escalate_feedback_template | model | StrOutputParser()
)

# Create a chain which branches according to the LLM's classification
chain = classification_template | model | StrOutputParser() | branches

# Run the chain with an example review
# Good review - "The product is excellent. I really enjoyed using it and found it very helpful."
# Bad review - "The product is terrible. It broke after just one use and the quality is very poor."
# Neutral review - "The product is okay. It works as expected but nothing exceptional."
# Default - "I'm not sure about the product yet. Can you tell me more about its features and benefits?"
print ("-----Good review-----")
review = "The product is excellent. I really enjoyed using it and found it very helpful."
result = chain.invoke({"feedback": review})
print(result)

print ("-----Bad review-----")
review = "The product is terrible. It broke after just one use and the quality is very poor."
result = chain.invoke({"feedback": review})
print(result)

print ("-----Neutral review-----")
review = "The product is okay. It works as expected but nothing exceptional."
result = chain.invoke({"feedback": review})
print(result)

print ("-----Default-----")
review = "I'm not sure about the product yet. Can you tell me more about its features and benefits?"
result = chain.invoke({"feedback": review})
print(result)