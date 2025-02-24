from langchain_community.document_loaders import GitLoader
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
import os
import sys

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if __name__ == "__main__":
    # Read arguments
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <GitHub URL>")
        exit()

    # Load repostiory contents
    loader = GitLoader(clone_url=sys.argv[1], repo_path="./cloned_repo/")
    documents = loader.load()

    # Create the model
    model = ChatOpenAI(model="gpt-4o-mini", openai_api_key=OPENAI_API_KEY)
    chat_history = [
        SystemMessage(content="You are a helpful AI assistant that analyzes and improves GitHub repositories. You should provide clear modifications in a structured format so they can be applied automatically.")
    ]

    # Give user input by combining all file contents
    content = "Here are the files in the repository:\n"
    for doc in documents:
        content += f"File Name: {doc.metadata['file_name']}\n"
        content += f"File Path: {doc.metadata['file_path']}\n"
        content += f"File Content: {doc.page_content}"
        content += f"\n\n"
    content += "Provide specific code modifications in this format:\n"
    content += "---MODIFIED <file_path>---\n<new_code>\n---END---\n"
    content += "Only suggest changes that can be directly applied without breaking functionality."
    user_message = HumanMessage(content=content)
    chat_history.append(user_message)

    # Invoke the LLM
    result = model.invoke(chat_history)
    response = result.content
    print(response)
    
