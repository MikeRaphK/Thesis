# **Automated Program Repair via Conversation: Fixing 162 out of 337 Bugs for $0.42 Each using ChatGPT (16-20/09/2024)**

## Abstract
- State-of-the-art LLM APR tools still follow the classic Generate and Validate (G&V) repair paradigm of first generating lots of patches by sampling from the same initial prompt and then validating each one afterwards. 
- **ChatRepair:** The first fully automated conversation-driven APR approach that interleaves patch generation with instant feedback to perform APR in a conversational style.
- ChatRepair first feeds the LLM with relevant test failure information to start with, and then learns from both failures and successes of earlier patching attempts of the same bug for more powerful APR. In this way, we can avoid making the same mistakes.
- Defects4j and QuixBugs dataset.
- ChatRepair is able to fix 162 out of 337 bugs for $0.42 each!

**Keywords:** Automated Program Repair, Large Language Model

## 1. Introduction
- Researchers have proposed learning-based APR approaches. Learning-based approaches are mainly based on either Neural Machine Translation (NMT) or Large Language Model (LLM).
- NMT-based APR tools rely heavily on its training data, obtained by scraping open-source repositories for bug fixing commits.
- Modern LLMs are trained on billions of open-source code snippets, demonstrating impressive performance on many code-related tasks, and can learn to directly generate code given the surrounding context
- **ChatRepair:** 
    - Extracts relevant test failure information to serve as the initial prompt to provide ChatGPT more contextual information for APR.
    - Learns from both failures and successes of earlier patching attempts of the same bug for more powerful APR.
    - For patches that failed, combines the incorrect patches with their corresponding test failure information.
    - For patches that succeeded, generates alternative variations of the original plausible patches.

## 3. Approach
- Initialize ChatGPT with the system message: `You are an Automated Program Repair tool`.
- Construct the initial prompt(HumanMessage) for ChatGPT which contains the buggy function to be fixed and the relevant test failure information to fix the bug.
- Invoke the model. ChatGPT generates a potential patch and we then mpove onto the conversation stage.
- Evaluate patch against the original test suite. If tests fail, ChatRepair offers feedback that includes relevant failure information (test failure/compilation error messages) and re-queries ChatGPT for a new patch while trying to avoid similar failures.
- Repeat until a plausible patch is produced or maximum conversation length is reached.
- After a plausible patch, ChatGPT is invoked using earlier plausible patches to generate more alternative plausible patches.
- ChatRepair obtains multiple plausible patches which can increase the chance of getting the correct patch.

## 4. Experimental Design
- Repair scenarios:
    - **Single-line:** replacing/adding a single line
    - **Single-hunk:** placing/adding a continuous code hunk
    - **Single-function:** generating a new function to replace the original buggy version

## 6. Limitations & Future Work
- While ChatRepair is able to achieve state-of-the-art repair performance of the studied benchmarks, there are still bugs that it struggles to fix. One particular category are multi-hunk bugs that require patches across multiple functions or files.
- Also due to the context window size, ChatRepair does not have access to project and repository specific information.
- We aim to further improve ChatRepair with LLM-based agents. This improves fault localization and repair-specific unformation.