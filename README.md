This is the official codebase for our 2022 CogSci paper:

# Structured, flexible, and robust: benchmarking and improving large language models towards more human-like behavior in out-of-distribution reasoning tasks

Katherine M. Collins*, Catherine Wong*, Jiahai Feng, Megan Wei, and Joshua B. Tenenbaum

*Contributed equally

Paper: https://arxiv.org/pdf/2205.05718.pdf

Project Page: https://sites.google.com/view/structured-flexible-and-robust/home

## Abstract

Human language offers a powerful window into our thoughts -- we tell stories, give explanations, and express our beliefs and goals through words. Abundant evidence also suggests that language plays a developmental role in structuring our learning. Here, we ask: how much of human-like thinking can be captured by learning statistical patterns in language alone? We first contribute a new challenge benchmark for comparing humans and distributional large language models (LLMs). Our benchmark contains two problem-solving domains (planning and explanation generation) and is designed to require generalization to new, out-of-distribution problems expressed in language. We find that humans are far more robust than LLMs on this benchmark. Next, we propose a hybrid Parse-and-Solve model, which augments distributional LLMs with a structured symbolic reasoning module. We find that this model shows more robust adaptation to out-of-distribution planning problems, demonstrating the promise of hybrid AI models for more human-like reasoning.

## Repository Details 

Code for "Part I: Linguistic reasoning benchmark for humans and language models" can be found in the `Part_I` directory.

Human and LLM generations, as well as all stimuli, can be found in the nested `data` directories for each domain (`plans` and `explanations`, respectively). 

Code for "Part II: Integrating language with structured reasoning models" can be found in the `Part_II` directory. 

## Citing

If citing us, please consider the following bibtex entry: 

```
@misc{https://doi.org/10.48550/arxiv.2205.05718,
  doi = {10.48550/ARXIV.2205.05718},
  
  url = {https://arxiv.org/abs/2205.05718},
  
  author = {Collins, Katherine M. and Wong, Catherine and Feng, Jiahai and Wei, Megan and Tenenbaum, Joshua B.},
  
  keywords = {Computation and Language (cs.CL), Artificial Intelligence (cs.AI), Machine Learning (cs.LG), Symbolic Computation (cs.SC), FOS: Computer and information sciences, FOS: Computer and information sciences},
  
  title = {Structured, flexible, and robust: benchmarking and improving large language models towards more human-like behavior in out-of-distribution reasoning tasks},
  
  publisher = {arXiv},
  
  year = {2022},
  
  copyright = {Creative Commons Attribution 4.0 International}
}
```


