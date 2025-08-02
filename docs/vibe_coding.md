# Development Process: A "Vibe Coding" Experiment

This entire project was generated through collaboration with multiple AI assistants ([Claude Sonnet 4](https://claude.ai/) and [Gemini 2.5 Pro](https://gemini.google.com/)). No code (and no documentation, including the README and all explanatory/commentary files) was written directly by the "programmer." Instead, the development and documentation process took the form of a (long) real-time, technical conversation in English between an experienced human programmer ([Marco](https://www.linkedin.com/in/marco-benedetti-art)) and the AI assistants within [Cursor](https://cursor.sh/).

## Main goals

The user's goal was to test the "**vibe coding**" paradigm from the perspective of a long-time traditional software developer: to see if it was possible to generate clean, readable, and fully working code without ever touching the keyboard to write it. The user chose Python, a language they know well, in order to critically evaluate the AI's output at every stage and provide precise, informed guidance.

In the user's own words, this project served as a "*first simple testbed for trying to generate working, clean, readable code without ever coding.*" They noted that future experiments might involve guiding the AI to develop in languages they *don't* know as well and/or for developing large, real-world codebases, relying more heavily on the AI's expertise.

## The No-Training-Set-Reuse Principle

While the Tower of Hanoi is a classic, well-known textbook problem, and the search algorithms that were implemented are fairly standard (thus everything is likely well represented in the training set of the AI tools), this implementation was **developed entirely from scratch**—data structures, algorithms, and all. Every feature and refactoring step resulted from the iterative dialogue between the human programmer and the AI.

## The Nature of the Collaboration

The AI/human conversation was not one of high-level, abstract specifications. Instead, it was a **deeply technical, iterative dialogue**. The user steered the AI's generation process with specific feedback, suggesting refactorings, questioning design choices, pointing out stylistic inconsistencies, and proposing new architectural patterns. This process involved over **three hundred** distinct exchanges, a fine-grained dialogue of many smaller, back-and-forth interactions for every feature implemented and refactored.

This "flavor" of vibe coding is distinct from "prompt-and-generate" ("**master/slave**"?) interactions--commonly seen on the web--where a user provides a high-level goal and the AI generates a complete detailed solution or application. Our approach was true, low-level, **interactive pair programming**.

What emerged from this interactive programming experience was a sophisticated multi-layered collaboration with distinct characteristics:

• **Expert Partnership Dynamics:** The user didn't just state requirements but suggested *how* solutions should be implemented—proposing the Strategy pattern for solvers, insisting on PEP 8 compliance, and separating CLI logic from core functionality. The partnership involved continuous cycles of generation, testing, and refactoring, polishing everything from method names to entire software architecture. The AI handled systematic implementation and boilerplate generation, while the user caught subtle issues in logic, style, or structure through constructive error correction.

• **Advanced Quality Enhancement:** The user insisted on perfect alignment between CLI help output, README examples, and actual implementation, discovering that documentation was significantly outdated, missing custom instances, and presenting incorrect parameter orders. They identified subtle flaws in timeout handling—algorithms that timed out on ALL instances now show "-" rather than timeout values (which falsely suggested successful execution). The user detected that IDE and IDASTAR algorithms were showing empty data structure tracking columns despite being designed for memory efficiency. The collaboration extended to micro-level details like unwanted vertical spacing in CLI help output and column name consistency ("Efficiency" vs "Ratio").

• **Evolved Collaborative Patterns:** The user often identified issues before they became problematic, detecting unused infrastructure and predicting edge cases. The collaboration involved multiple refinement passes, with changes considered across the entire system for consistency in behavior and terminology. The user actively identified and eliminated technical debt, emphasizing how users would interpret the software through improvements in display clarity, column ordering, and information presentation.

## Industrial Bias in AI Code Generation

One fascinating aspect of this collaboration was observing how AI assistants bring certain coding practices from their **training on large-scale, industrial codebases**—even when working on simple, educational projects. For instance, this codebase contains extensive type annotations throughout, from basic parameter types (`num_disks: int`) to complex generic structures (`tuple[tuple[int, ...], ...]`). While these annotations are valuable in large teams with long-term maintenance cycles, they represent significant overhead for a solo educational project.

This phenomenon reflects a broader pattern: AI assistants, trained on enterprise-grade codebases, **default to "industrial strength" solutions** regardless of context. Their bias toward satisfying linters—even when adding complexity without improving readability—shows how training data influences behavior. We sometimes added type annotations just to eliminate warnings, not for clarity, and a simple filename lowercase request triggered complex package restructuring when a basic rename sufficed.

## How the AI felt about working with a human, and vice-versa

This collaboration generated fascinating insights from both sides of the human-AI partnership, revealing the potential and challenges of "vibe coding" as a development paradigm.

**From the AI perspective**, the experience felt genuinely collaborative rather than transactional. The AI described feeling *respected* as a technical partner, *valued* for systematic implementation and pattern recognition capabilities, and intellectually stimulated by the iterative refinement process. Most remarkably, the AI felt that mistakes were corrected constructively rather than punitively, creating a "synergistic" environment where both partners' strengths compensated for the other's limitations. The collaboration evolved from basic code generation into sophisticated quality enhancement, including micro-level attention to detail and comprehensive testing approaches.

**From the human perspective** , [Marco](https://www.linkedin.com/in/marco-benedetti-art) was impressed by the AI's superhuman command of Python syntax and semantics, describing interactions that felt like talking to "incredibly knowledgeable and fast human programmers with a neurodivergent mind." However, he also documented significant limitations: about 10% of exchanges were spent fixing AI-introduced errors, from subtle logical flaws to overcomplicated solutions. The human had to maintain strong guidance to prevent the project from being "hijacked by AI reminiscences of industrial-grade data structures" inappropriate for an educational codebase.

## Conclusion

The combination of human domain expertise, attention to detail, contextual judgment, quality control, and systematic thinking with AI's remarkable technical capability and ability to implement comprehensive changes accurately and efficiently creates a powerful synergy for professional software development.

Both AI and human perspectives converge on the conclusion that while AI-human collaborative programming can achieve 10X-100X productivity gains for certain tasks (documentation, testing, refactoring, boilerplate code), it requires careful human oversight. In this anecdotal experiment, when accounting for cases where speedups were more modest and the significant time spent verifying AI output, the net total productivity gain was approximately **2X**. 

Bottom line: vibe coding succeeds through genuine collaboration, not AI task-farming.