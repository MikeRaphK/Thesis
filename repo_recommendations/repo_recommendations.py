from langchain_community.document_loaders import GitLoader
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

import os
import sys

from build_graph import build_graph
from write_to_file_tool import write_to_file

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
    print(f"Initializing LLM...\n")
    model = ChatOpenAI(model="gpt-4o-mini", openai_api_key=OPENAI_API_KEY)
    chat_history = [
        SystemMessage(content="You are a helpful AI assistant that analyzes and improves code found on GitHub repositories. You should provide clear modifications in a structured format so they can be applied automatically.")
    ]

    # Get the toolkit
    tools = [write_to_file]

    # Create the graph
    print(f"Building graph...\n")
    APP = build_graph(tools=tools, llm=model)
    img = APP.get_graph().draw_mermaid_png()
    with open("graph.png", "wb") as f:
        f.write(img)

    # Give user input by combining all file contents
    user_prompt = "Here are the files in the repository:\n"
    for doc in documents:
        user_prompt += f"File Name: {doc.metadata['file_name']}\n"
        user_prompt += f"File Path: {doc.metadata['file_path']}\n"
        user_prompt += f"File Content: {doc.page_content}"
        user_prompt += f"\n\n"
    user_prompt += "Provide specific code modifications in this format:\n"
    user_prompt += "---MODIFIED <file_path>---\n<new_code>\n---END---\n"
    user_prompt += "Only suggest changes that can be directly applied without breaking functionality."
    user_prompt += "Also add a summary of changes for each file at the end."
    chat_history.append(HumanMessage(content=user_prompt))

    # Invoke the LLM
    print(f"Getting recommendations...\n")
    result = model.invoke(chat_history)
    response = result.content
    print(response)

    # Write each recommendation
    print(f"Writing recommendations...\n")
    chat_history.append(AIMessage(content=response))
    write_prompt = "Please create a new file for each recommendation you have given under the ./updated_files directory."
    write_prompt += "Each new file should have the name MODIFIED_<old_file_path>.<old_file_type> and the corresponding changes you gave as its contents."
    chat_history.append(HumanMessage(content=write_prompt))
    output_state = APP.invoke({"messages" : chat_history})
    content = output_state["messages"][-1].content
    print(f"ChatGPT: {content}")
