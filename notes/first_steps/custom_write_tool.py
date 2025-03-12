from langchain_core.tools import tool

# File writing tool
@tool
def write_to_file_tool(file_path : str, content : str) -> str:
    """
    Writes content to a file.
    """
    with open(file_path, "w") as f:
        f.write(content)
    return f"Summary saved to {file_path}"

content = """
#include <stdio.h>

int main(void) {
    printf("Hello world!\\n");
    return 0;
}
"""
result = write_to_file_tool.invoke({"file_path": "./main.c", "content": content})
