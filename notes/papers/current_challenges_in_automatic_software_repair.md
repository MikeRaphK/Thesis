# **Current Challenges in Automatic Software Repair (07/06/2013)**

## Abstract
This article serves three purposes:
1. Summarize algorithmic improvements and recent experimental results.
2. Review related work in the rapidly growing subfield of automatic program repair.
3. Outline important open research challenges that we believe should guide future research in the area.

**Keywords:** automatic program repair, software engineering, evolutionary computation

## 2. GenProg
- **GenProg:** Repair program that uses genetic programming (GP) to repair a wide range of defect types in legacy software without requiring a
priori knowledge or formal specifications.

## 2.2 Overview
- **Inputs:** 
    - A program.
    - A set of test cases that encode the bug (negative test cases).
    - Required behavior that cannot be changed (positive test cases).
- Each individual or **variant** is represented as a *patch* or a sequence of edit operations to the original program.
- The goal is to produce a patch that causes the original program to pass all test cases.
- When the algorithm starts, a number of random initial patches are applied, therefore creating the population. From the population, the most high-fitted individual are selected as **parents** in the next **generation**. Parents then create two new **offspring** variants. Each parent and each offspring is mutated once (mutate), and the result forms the incoming population for the next generation.
- The GP loop terminates if a valid patch is found that causes the input program to pass all tests or when a predetermined time limit is exceeded.
- Each execution of the GP algorithm is referred to as a **trial**. Multiple executions of the algorithm are typically run in parallel for a given bug, each with a distinct random seed.

## 2.3 Representation
- In older versions, GP represented individuals by their abstract syntax tree (AST). ASTs, however, limit scalability and have been replaced by patches.

## 2.4 Fitness
- The fitness of an individual in a program repair task should assess how well the patch causes the program to avoid the bug while still retaining all other required functionality.
- This is done by using test cases by applying a candidate patch to the original program and then rerunning the test suite on the result.
- Since running **all** test cases for **all** possible patches takes a lot of time, o evaluate candidates on subsamples of the tests. **SampleFit** evaluates a candidate patch on a random sample of the positive tests and on all the negative test cases.
- Variants that maximize SampleFit are fully tested on the
entire test suite (**FullFitness**).
- The final fitness of a variant is the weighted
sum of the number of tests it passes, where negative tests are typically weighted more heavily than the positive ones.  Programs that do not compile are assigned fitness zero.

## 2.5 Mutation and Crossover
- In each mutation, a destination statement d is randomly chosen to be mutated.
- Three types of mutation:
    - **Delete:** Statement d is completely deleted.
    - **Insert:** A new statement s is inserted right after statement d.
    - **Replace:** d is replaced by a new statement s.
- **Crossover** selects two variants and exchanges subsequences between the two list of edits.
- The motivation for this operator is that valid partial solutions might be discovered by different variants, and crossover can combine them efficiently.

# 3. Evaluation
- **Generality:** GenProg can repair many different types of bugs in real-world programs.
- **Scalability:** GenProg can repair programs containing millions of lines of code, without requiring special coding practices or annotations.

# 5 Open Research Challenges
- GP can take up to 12 hours of working in order to produce a valid solution.
- Cannot repair complicated bugs, e.g. SQL injections or synchronization primitives (lock and unlock).
- We cannot fully establish the credibility of automated repairs.
- Patch quality: How can we be confident that a given patch correctly repairs a defect without violating other system requirements?
- GenProg uses testing to guide a search or measure acceptability. We need to manually write these tests or rely on automated test case generation.
- GenProg starts with a program that is almost correct and has a single identified defect. What would it take for automated repair to start with a partially debugged program and iteratively improve the program until all the defects were eliminated, perhaps in the style of extreme programming?