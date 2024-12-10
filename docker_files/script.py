from openai import OpenAI
client = OpenAI()

# Typical user query. Just like chatting with ChatGPT
query = "Hello ChatGPT! This is just a test query. Do we have a connection?"
print("Mike: " + query)
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": query},
    ]
)

# Print the response
print("ChatGPT: " + response.choices[0].message.content)
print(f"This conversation took {response.usage.total_tokens} total tokens")