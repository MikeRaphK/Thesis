# **RepairAgent: An Autonomous, LLM-Based Agent for Program Repair (28/10/2024)**

## Abstract
- **RepairAgent:** the first work to address the program repair challenge through an autonomous agent based on a LLM.
- Agent capable of autonomously planning and executing actions to fix bugs by invoking suitable tools.
- **Defects4J dataset:** A benchmark with 835 bugs for evaluating program repair techniques.
- 270,000 tokens per bug, ~14 cents per bug.

## 1. Introduction
- The first generation of LLM-based repair uses a one-time interaction with the model, where the model receives a prompt containing the buggy code and produces a fixed version.
- The second and current generation of LLM-based repair introduces iterative approaches, which query the LLM repeatedly based on feedback obtained from previous fix attempts.
- RepairAgent has tools to extract information about the bug by reading specific lines of code, to gather repair ingredients by searching the code base, and to propose and validate fixes by applying a patch and executing test cases.
- We do not hard-code how and when to use these tools, but instead let the LLM autonomously decide which tool to invoke next.
- RepairAgent successfully fixes 164 bugs from Defects4J. 39 of those have not been fixed by prior work.
- [Open-source](https://github.com/sola-st/RepairAgent).

## 3. Approach

### B. Terminology
- A **cycle** represents one round of interaction with the LLM agent. Consists of:
    1) Query the agent
    2) Post-process the response
    3) Execute the command suggested by the agent
    4) Update the dynamic prompt based on the command’s output

- The **dynamic prompt** is a sequence of text sections P = [s0, s1, ..., sn], where each section si is one of the following:
    - A *static section*, which remains the same across all cycles.
    - A *dynamic section*, which may differ across cycles.

### C. Dynamic Prompting
1) Role
2) Goals  
    a) Locate the bug  
    b) Gather information about the bug  
    c) Suggest simple fixes to the bug  
    d) Suggest complex fixes  
    e) Iterate over the previous goals  
3) Guidelines
4) State Description  
    a) Understand the bug  
    b) Collect information to fix the bug  
    c) Try to fix the bug  
5) Available Tools
6) Gathered Information
7) Output Format
8) Last Executed Command and Result

### D. Tools
1) Reading and Extracting Code
2) Search and generate code (by invoking another LLM)
3) Testing and Patching
4) Control

### E. Middleware
1) Parsing and Refining LLM Output
2) Callign the Tool
3) Updating the Promp