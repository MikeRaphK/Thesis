# Notes on how o1-preview and o1-mini are used
# For applications that need images, function calling, and fast response times, GPT-4o and GPT-4o-mini are the right choice.
# However, for applications that demand deep reasoning and can accommodate longer response times, o1 models are an excellent choice
# o1 queries can take anywhere from a few seconds to several minutes

from openai import OpenAI
client = OpenAI()

query = "Write a program in C++ that checks if a given number is prime"
response = client.chat.completions.create(
    model="o1-mini",
    messages=[
        {"role": "user", "content": query},
    ]
)

print(response.choices[0].message.content)
print(f"This conversation took {response.usage.completion_tokens} completion tokens and {response.usage.total_tokens} total tokens")