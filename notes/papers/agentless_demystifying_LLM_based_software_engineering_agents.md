# **AGENTLESS: Demystifying LLM-based Software Engineering Agents (29/10/2024)**

## Abstract
- **LLM agents:** LLMs equipped with the ability to use tools, run commands, observe feedback from the environment, and plan for future actions.
- **AGENTLESS:** An agentless approach to automatically resolve software development issues.
    - Three-phase process of localization, repair, and patch validation.
    - 32.00% performance 9(6 correct fixes) and low cost ($0.70).
    - OpenAI as the go-to approach to showcase the real-world coding performance of both GPT-4o and the new OpenAI o1 models.

## 1. Introduction
- **SWE-bench:** A benchmark. Each problem consists of a real-world GitHub issue description and the corresponding Python repository. The task is to modify the repository to resolve the issue, either fixing a bug or introducing a new feature.
- **Do we really have to employ complex autonomous software agents?**

## 2. Background and Related Work

### 2.1 Agent-based Software Engineering
- **Devin:** One of the first end-to-end LLM agent-based framework. Devin uses agents to first perform planning based on user requirement, then allows the agent to use file editor, terminal, and web search engine tools to iteratively perform the task.
- **SWE-agent** designs a custom agent-computer interface (ACI) that allows the LLM agent to interact with the repository environment with actions such as reading, editing files, and running bash commands.
- **Aider** first provides a detailed repository map constructed with static and call graph analysis to the LLM to localize the files that require editing; then it generates a simple diff format as the editing patch and uses regression testing to verify if the patch is plausible.
- ...

### 2.2 Fault Localization and Program Repair
- **Fault localization (FL)** techniques aim to identify the suspicious locations (e.g., statements or methods) in source code related to bugs.
- After localizing the bug, the next step is to perform repair. **Automated program repair (APR)** has been widely studied to automatically generate patches for bugs.
- Different from most LLM-based APR techniques, AGENTLESS generates patches using a simple diff format to avoid generating the complete code and instead focus on producing cost-efficient small edits, increasing the reliability and accuracy of patch generation (less chances for hallucination).

### 2.3 LLM-based Test Generation
- Another research area that has been adopting LLM is test generation. One area of test generation is fuzz testing, also known as fuzzing, to generate large amounts of inputs in order to expose bugs in systems.
- Besides fuzzing, researchers have also proposed to leverage LLMs for unit test generation to test individual software units (e.g., methods/classes), such as CodeMosa, ChatTester, TestPilot, and CoverUp.


## 3. AGENTLESS Approach
All of this looks important.


