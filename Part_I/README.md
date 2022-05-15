# Part I Code 

Here, we include the code and stimuli used in Part I of our paper -- which considered two core reasoning domain: goal-based planning and causal explanations. We separate each of the domains into the `plans` and `explanations` directories, respectively. Both domains have identically structured nested folders, as discussed below. 

## Data 

Data for all experiments can be found in the `data` directory within each domain. There are further subdirectories for `generation` (language production task; human- and LLM-generated), `typicality_ratings` (human-rated typicality of the base goals and scenarios in Condition 1), `hummaness_ratings` (human ratings used to prescreen LLM-generations), and `goodness_ratings` (final human ratings of overall plan or explanation goodness). 

Files prefixed with `raw-` in the `generations` folder house human generations before processing. Human-generated plans and explanations can be found in the `response` column. Information about the stimuli is in the `prompt` column, with constraint(s) if in Condition 2 or 3 being listed in the `constraint` column, which can be concatenated during analysis. Reaction time (`rt`) per response is in milliseconds. We save out separate files for Condition 1 (unconstrained) and the constrained Conditions (Conditions 2 and 3, referred to as `constrained_single` and `constrained_many`). 

The final set of processed plans used in the goodness ratings, and to prompt the LLM, are found in the `human_plans.csv` and `human_explanations.csv` files within the `data/generations` folders of the respective domains. An easily readable breakdown of these same plans and explanations -- per stimuli, per condition -- can be found in the `per_condition_per_stim_human` subfolder as `.txt` files to make them easily readable. It was these files were read from to construct the LLM prompts.

In all files, `goal` represents the stimuli and `plan` the generated response. We note that this is used for consistency in the codebase; however, in the explanations domain -- this means `goal` is synonymous with `scenario` and `plan` with explanation. 

All human results have been scraped to remove potentially identifying information, with each participant being re-assigned a new ID. Note, the IDs are assigned per experiment type, and therefore may not be unique (but we note that each human participant was only included in one experiment type). 

We further note that all ratings were conducted using 7-point Likert scales. These are saved out on a 0-6 scale; however, in our later analyses, we transform the ratings to a 1-7 base. The csv files have the original 0-6 form. 

## Prompting and filtering the LLM

Code used to prompt the LLM (here, GPT-3) can be found in `prompting_and_filtering_llm`. Note, a valid OpenAI key is required to run custom generations.

As noted in our paper, the LLM was prompted with *human* generations -- which can be found in our `data` directory, as noted above. 

We additionally prescreen, or filter, LLM generations for humanness. Plans and explanations which were rated zero on humanness by *any* rater are saved into the `rated_zero.csv` files per domain. Code to run humaness studies is included in this directory, with some processing in `utils`. As these humanness ratings involved actual human elicitation, further scripts were written to run gather annotations -- as discsussed next.

## Human experiments

The code and associated stimuli files used to re-create the human experiments run for this study (e.g., for language production, humanness ratings, and goodness ratings) can be found in the `human_experiments` folder. Each subfolder is a separate experiment type that was run. All .js files needed are contained in each subfolder. Our studies were hosted on Cognition, which allows users to have a main .js file and link with additional stimuli (also .js files). Human and LLM-generations, and/or pre-specified stimuli batches, were passed to the Cognition server via constructed .js files. 

## Analysis

Statistical analyses are included in the `analysis` subfolder. The analysis code for `plans` is in `plans.R` and for `explanations` is in `explanations.R`.

Use RStudio and R version 4.0.2 to run the analysis code.

We include auxillary fine-grained exploratory analyses that we ran; for instance, extracting all human- and LLM-generated plans and explanations which achieved a mean rating > 6 (on a 1-7 scale), in the `good-` text files -- and all generations achieving a mean rating < 2 in the `bad-` files. We also generate plots per goal and scenario containing a breakdown of the mean (over >= 3 annotators per) ratings over all stimuli, across conditions -- these data can be found in the `per_stimuli_goodness.pdf` file. 

## Utils

Additional batch creation and data processing files are contained in `utils`. 

## Figures in paper

The code used to generate the main results figure for Part I (Fig. 3) is housed in `paper_figures.` Note, the file includes pre-extracted p-values, which are drawn from the analysis code for the respective domains. 
