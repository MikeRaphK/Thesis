# Notes on how prompts are used

from openai import OpenAI
client = OpenAI()

# # Typical user query. Just like chatting with ChatGPT
# query = "Which is the fastest programming language?"
# response = client.chat.completions.create(
#     model="gpt-4o-mini",
#     messages=[
#         {"role": "user", "content": query},
#     ]
# )

# System role: Top-level instructions to the model to describe behavior
system_description = "You are a helpful assistant that answers programming questions in no more that 3 sentences."
query = "Which is the fastest programming language?"
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": system_description},
        {"role": "user", "content": query},
    ]
)

# # Assistant role: Provide examples to the model for how it should respond to the current request
# assistant_reply = "Who's there?"
# response = client.chat.completions.create(
#     model="gpt-4o-mini",
#     messages=[
#         {"role": "user", "content": "Knock knock"},
#         {"role": "assistant", "content": assistant_reply},
#         {"role": "user", "content": "Dishes"},
#     ]
# )

# Print the response
print(response.choices[0].message.content)
print(f"This conversation took {response.usage.total_tokens} total tokens")