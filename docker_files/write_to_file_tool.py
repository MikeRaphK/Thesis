from langchain_core.tools import tool

@tool
def write_to_file(path : str, content : str) -> str:
    """
    Call this tool to write the given content to a file at the specified path
    """
    try:
        with open(path, "w", encoding="utf-8") as file:
            file.write(content)
        return f"Successfully wrote to {path}"
    except Exception as e:
        return f"Error writing to file: {e}"
