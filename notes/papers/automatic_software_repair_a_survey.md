# **Automatic Software Repair: A Survey (01/2019)**

## Abstract
This paper organizes the knowledge in automatic repair techniques by surveying a body of 108 papers, illustrating the algorithms and the approaches, comparing them on representative examples, and discussing the open challenges and the empirical evidence reported so far.

**Keywords:** Automatic program repair, generate and validate, search-based, semantics-driven repair, correct by construction, program
synthesis, self-repairing


## 3. Software Repair
- **Software Healing:** Detect software failures in-the-field and respond to them by making the necessary adjustments to restore the normal operation of a system. These adjustments are not deployed at the source code level, but rather applied at runtime on the deployed application.
- **Software Repairing:** Detect software failures, localize where a fix could be applied, and make the necessary adjustments to fix the fault, and thus prevent further failures caused by the same fault. The adjustments are generated in-house, such as at testing and design time, and deployed at the source code level.
- **Automatic software healing/repairing(Self-healing/Self-repairing):** The human only supervises the process and his intervention is not involved.
- **Workaround:** Temporary solution to a software bug.
- **Fix(patch):** Permanent solution to a software bug.

## 5. Localization
- **Fault localization:** Identify the faulty statements.
- **Fix locus localization:** Detect the statements where the effect of the fault can be observed and eliminated.

## 6. Fix Generation
- **Generate-and-validate approaches:** Define and explore a space of potential solutions.
- **Semantic-driven(correct-by-construction) approaches:** Formally encode the problem, then find a solution that is guaranteed to solve it.
- **General repairing techniques:** Not designed to target a specific class of faults. Can potentially repair any class of faults
in a program.
- **Fault-specific repairing techniques:** Address some classes of faults only, such as wrong conditions in conditional statements and buffer overflows.

## 7. Fix Recommenders
Fix recommenders are techniques that do not attempt to produce fixes, but simply suggest a few changes that might be operated on the software to repair the fault.

## 9. Open Challenges
- **Fix Correctness Challenges:** Most of the techniques can generate plausible fixes, for instance fixes that pass all the test cases in an available test suite. In contrast, developers need correct fixes, that is, fixes that satisfy all the requirements of the program under repair
- **Process Challenges:** While program repair techniques can sometime automatically produce reasonable fixes, the acceptability of a fix is still relegated to the judgment of developers. This means that we cannot have a Fully Automatic Repair Process.
- **Technical Challenges:** There are many software repair techniques and many studies available, however findings are still scattered and difficult to be synthesized into a clear picture.