from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnableParallel, RunnableLambda
from langchain_openai import ChatOpenAI

# Create the model
model = ChatOpenAI(model="gpt-4o-mini")

# Define prompt templates
messages = [
    ("system", "You are an expert product reviewer."),
    ("human", "List me the main features of the product {product_name}"),
]
prompt_template = ChatPromptTemplate.from_messages(messages)

def analyze_pros(features):
    messages = [
        ("system", "You are an expert product reviewer."),
        ("human", "Given these features: {features}, list the pros of these features."),
    ]
    pros_template = ChatPromptTemplate.from_messages(messages)
    return pros_template.format_prompt(features=features)

# Pros branch
pros_branch_chain = (
    RunnableLambda(lambda x: analyze_pros(x)) | model | StrOutputParser()
)

def analyze_cons(features):
    messages = [
        ("system", "You are an expert product reviewer."),
        ("human", "Given these features: {features}, list the cons of these features."),
    ]
    cons_template = ChatPromptTemplate.from_messages(messages)
    return cons_template.format_prompt(features=features)

# Cons branch
cons_branch_chain = (
    RunnableLambda(lambda x: analyze_cons(x)) | model | StrOutputParser()
)

# Combine pros and cons into a final review
def combine_pros_cons(pros, cons):
    return f"Pros:\n{pros}\n\nCons:\n{cons}"

# Create a chain and make output readable
chain = (
    prompt_template
    | model
    | StrOutputParser()
    | RunnableParallel(branches={"pros": pros_branch_chain, "cons": cons_branch_chain})
    | RunnableLambda(lambda x: combine_pros_cons(x["branches"]["pros"], x["branches"]["cons"]))
)

# Run the chain
result = chain.invoke({"product_name": "The Latest iPhone"})
print(result)