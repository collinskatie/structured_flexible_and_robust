This is the official codebase for our 2022 CogSci paper:

# Structured, flexible, and robust: benchmarking and improving large language models towards more human-like behavior in out-of-distribution reasoning tasks

Katherine M. Collins*, Catherine Wong*, Jiahai Feng, Megan Wei, and Joshua B. Tenenbaum

*Contributed equally

## Abstract

Many of our thoughts are communicated through language, from the stories we tell each other, to our explanations and instructions for plans. Moreover, language plays a critical role in children's learning to think. As such, here we ask the question: can learning to think be captured by learning patterns in language alone? We contribute a new challenge benchmark, over two problem-solving domains (goal-based planning and causal explanation generation), designed to untangle the interaction of thinking and learning patterns of language. We compare humans and distributional large language models (LLMs), finding that humans are comparatively more robust under our increasingly out-of-distribution language production tasks. We next propose an alternative computational approach: a structured, Parse-and-Solve model which reasons directly in the space of programs. We devise an analogous, progressively-constrained task and find that our method achieves greater adaptability, demonstrating the promise of hybrid AI models for more human-like reasoning.

## Repository Details 

Code for "Part I: Linguistic reasoning benchmark for humans and language models" can be found in the `Part_I` directory.

Human and LLM generations, as well as all stimuli, can be found in the nested `data` directories for each domain (`plans` and `explanations`, respectively). 

Code for "Part II: Integrating language with structured reasoning models" can be found in the `Part_II` directory. 




