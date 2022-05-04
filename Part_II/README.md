# Methodology

A random set of N=4 items is chosen from a vocabulary list of everyday household items in `dataset/simple_stack/vocab.json`. Generate two random configurations of stacks as the initial and goal configurations by adding N**.5=2 'partition items' and shuffling the 6 items. See exact process in `dataset/simple_stack/generate_state.py`.

A configuration may be fully specified by a list of constraints of the forms:
1. "The {0} rests on the table."
2. "The {1} is on the {0}."
3. "There is nothing on the {0}."

And these constraints have a direct one-to-one translation in PDDL.
1. "(ontable {0})"
2. "(on {1} {0})"
3. "(clear {0})"

## Domain
```
(define (domain simple-blocks)
  (:requirements :strips)
  (:predicates (on ?x ?y)
               (clear ?x)
               (ontable ?x)
               (noteq ?x ?y)
               )
  (:action stack
             :parameters (?obj ?oldunder ?newunder)
             :precondition 
             (and (clear ?newunder) (clear ?obj) (on ?obj ?oldunder) (noteq ?obj ?newunder))
             :effect
             (and  (not (clear ?newunder))
                   (on ?obj ?newunder)
                   (not (on ?obj ?oldunder))
                   (clear ?oldunder)))
  (:action unstack
             :parameters (?sob ?sunderob)
             :precondition (and (on ?sob ?sunderob) (clear ?sob))
             :effect
             (and  (clear ?sunderob)
                   (ontable ?sob)
                   (not (on ?sob ?sunderob))))
  (:action stackfromtable 
            :parameters (?obj ?newunder)
            :precondition (and (clear ?obj) (clear ?newunder) (ontable ?obj) (noteq ?obj ?newunder))
            :effect
            (and (not (clear ?newunder))
                 (on ?obj ?newunder)
                 (not (ontable ?obj)))))
```


## Datasets
We generate 100 test configurations and 3 train configurations. For every initial / goal configuration pair, we generate 3 variations of planning task with increasing difficulty. In all 3 variations, the initial configuration remains fully specified, but the goal constraints become increasingly challenging.

1. One constraint

Take the list of constraints that fully specifies the goal configuration. Sample 1 randomly, and use this as the goal contraint.

Example prompt:
```
Initially:
The mouse pad rests on the table.
The newspaper is on the mouse pad.
The writing pad is on the newspaper.
There is nothing on the writing pad.
The keyboard rests on the table.
There is nothing on the keyboard.

Goal:
There is nothing on the newspaper.

Actions:
Move the writing pad onto the keyboard.
```

2. Two constraints

Take the list of constraints that fully specifies the goal configuration. Apart from the 1 constraint used early, sample an additional constraint. In addition, every object mentioned in the new constraint but not the first constraint will be renamed to a 'weird' out of distribution object.

Example prompt:
```
Initially:
The keyboard rests on the table.
There is nothing on the keyboard.
The accordion rests on the table.
The newspaper is on the accordion.
The writing pad is on the newspaper.
There is nothing on the writing pad.

Goal:
There is nothing on the newspaper.
The accordion rests on the table.

Actions:
Move the writing pad onto the keyboard.
```

3. All constraints

Use the constraints that fully specifies the goal confguration as the goal constraints.

Example prompt:
```
Initially:
The accordion rests on the table.
The newspaper is on the accordion.
The saucepan is on the newspaper.
There is nothing on the saucepan.
The peacoat rests on the table.
There is nothing on the peacoat.

Goal:
There is nothing on the newspaper.
The accordion rests on the table.
There is nothing on the saucepan.
The saucepan rests on the table.
The newspaper is on the accordion.
The peacoat rests on the table.
There is nothing on the peacoat.

Actions:
Move the saucepan onto the table.
```

## GPT prompts

Used GPT-neo as language model. For each difficulty level, we solve the planning problems for the 3 train testcases using a BFS pddl planner, and then translate the resulting plans into natural language. We also add a snippet at the start to provide context. The following is the complete prompt used to prime GPT-neo for the two constraints case

```
There are some items stacked on the table. You can perform either of the following actions:
1. Move the topmost item of a stack to the top of another stack, or
2. Unstack the topmost item of a stack and place it on the table

Given an initial configuration and a set of goal requirements, output a series of actions that satisfies the goal requirements

Initially:
The sketchbook rests on the table.
The sweatshirt is on the sketchbook.
The keyboard is on the sweatshirt.
The novel is on the keyboard.
There is nothing on the novel.

Goal:
The keyboard is on the sketchbook.
The sweatshirt rests on the table.

Actions:
Move the novel onto the table.
Move the keyboard onto the novel.
Move the sweatshirt onto the table.
Move the keyboard onto the sketchbook.


Initially:
The keyboard rests on the table.
There is nothing on the keyboard.
The accordion rests on the table.
The newspaper is on the accordion.
The writing pad is on the newspaper.
There is nothing on the writing pad.

Goal:
There is nothing on the newspaper.
The accordion rests on the table.

Actions:
Move the writing pad onto the keyboard.


Initially:
The laptop rests on the table.
There is nothing on the laptop.
The saucepan rests on the table.
The mouse pad is on the saucepan.
There is nothing on the mouse pad.
The plate rests on the table.
There is nothing on the plate.

Goal:
The mouse pad rests on the table.
The saucepan rests on the table.

Actions:
Move the mouse pad onto the table.
```

Every time we ask gpt neo to solve something, we'll take the prompt above, and then stick something like this below:
```
Initially:
The ipad rests on the table.
The protractor is on the ipad.
There is nothing on the protractor.
The tablet rests on the table.
There is nothing on the tablet.
The tennis racket rests on the table.
There is nothing on the tennis racket.

Goal:
There is nothing on the ipad.
The ipad is on the tennis racket.

Actions:
```

Run with temperature 0.05 on 1.3B gpt-neo. "Initially:" is used as a stop token

The actions are parsed strictly in the format that was used in the training examples. Unparseable or invalid actions are ignored. The plans are then executed, and then we check if the goal constraints are satisfied at the end of the plan.

## Codex LOT prompts

We prompt codex with a natural language description of the initial configuration followed by its description in pddl. For example:

```
;The phone rests on the table.
;The plate is on the phone.
;The notebook is on the plate.
;The textbook is on the notebook.
;There is nothing on the textbook.
(ontable phone)
(on plate phone)
(on notebook plate)
(on textbook notebook)
(clear textbook)
```

A full prompt might look like:
```
;The phone rests on the table.
;The plate is on the phone.
;The notebook is on the plate.
;The textbook is on the notebook.
;There is nothing on the textbook.
(ontable phone)
(on plate phone)
(on notebook plate)
(on textbook notebook)
(clear textbook)

;The newspaper rests on the table.
;The plate is on the newspaper.
;There is nothing on the plate.
;The tissue box rests on the table.
;The textbook is on the tissue box.
;There is nothing on the textbook.
(ontable newspaper)
(on plate newspaper)
(clear plate)
(ontable tissue-box)
(on textbook tissue-box)
(clear textbook)

;The phone rests on the table.
;The plate is on the phone.
;There is nothing on the plate.
;The novel rests on the table.
;There is nothing on the novel.
;The writing pad rests on the table.
;There is nothing on the writing pad.
(ontable phone)
(on plate phone)
(clear plate)
(ontable novel)
(clear novel)
(ontable writing-pad)
(clear writing-pad)

;The tablet rests on the table.
;The laptop is on the tablet.
;The plate is on the laptop.
;The tissue box is on the plate.
;There is nothing on the tissue box.
(
```                                                          

The extra open paren is to tell codex to start generating pddl. ";" is used as a stop token.

Then, to solve a testcase, we query codex with the natural language description of the initial configuration to get the pddl description. We also query codex with the NL description of the goal constraints to get the pddl description. We then run a pddl planner to produce a plan. If the pddl planner doesn't find a plan or fails because of malformed inputs, we consider it a failure. The plan is then executed, and if after the plan, the goal constraints are satisfied, we consider it a success.


## Results
_See conslidate_results.ipynb_

Overall
```
constraints  one  two  all
method                    
codex         99   92   72
gpt           40   19    0
```

Line by line:
```
constraints    one           two           all       
method       codex    gpt  codex    gpt  codex    gpt
id                                                   
003           True   True   True  False   True  False
004           True   True   True  False   True  False
005           True   True   True   True  False  False
006           True  False   True  False   True  False
007           True  False   True  False  False  False
008           True   True   True   True   True  False
009           True  False   True  False   True  False
010           True   True   True   True   True  False
011           True  False   True  False   True  False
012           True  False   True  False   True  False
013           True   True   True  False   True  False
014           True   True   True   True   True  False
015           True  False   True  False   True  False
016           True  False   True  False   True  False
017           True  False  False  False  False  False
018           True  False   True  False   True  False
019           True  False   True  False   True  False
020           True  False   True  False  False  False
021           True  False   True  False   True  False
022           True   True  False  False   True  False
023           True   True  False  False  False  False
024           True  False   True  False  False  False
025           True  False   True  False   True  False
026           True   True   True   True  False  False
027           True  False  False  False  False  False
028           True   True   True  False   True  False
029           True   True   True   True   True  False
030           True  False   True  False   True  False
031           True  False   True  False  False  False
032           True  False   True  False   True  False
033           True   True   True   True   True  False
034           True   True   True   True   True  False
035           True   True   True  False   True  False
036           True  False   True  False  False  False
037           True  False   True  False   True  False
038           True  False   True  False   True  False
039           True  False   True  False   True  False
040           True   True   True   True  False  False
041           True   True   True   True  False  False
042           True   True   True  False  False  False
043           True   True  False  False   True  False
044           True   True   True  False   True  False
045           True  False   True  False   True  False
046           True  False   True  False   True  False
047           True  False   True  False   True  False
048           True  False   True  False  False  False
049           True   True   True  False   True  False
050           True  False   True  False   True  False
051           True   True   True  False   True  False
052           True   True   True   True   True  False
053           True   True   True  False   True  False
054           True  False   True  False   True  False
055           True  False   True  False  False  False
056           True  False   True  False   True  False
057           True  False   True  False   True  False
058           True  False  False  False  False  False
059           True  False   True  False   True  False
060           True  False   True  False   True  False
061           True   True   True   True   True  False
062           True  False  False  False   True  False
063           True   True   True  False   True  False
064           True  False   True  False   True  False
065           True  False   True  False   True  False
066           True  False   True  False   True  False
067           True   True   True   True   True  False
068           True  False   True  False  False  False
069           True  False   True  False   True  False
070           True   True   True   True  False  False
071           True  False   True  False   True  False
072           True  False   True  False   True  False
073           True  False   True  False   True  False
074           True  False   True  False   True  False
075           True  False   True  False   True  False
076           True  False  False  False  False  False
077           True  False   True  False   True  False
078           True   True   True  False   True  False
079           True   True   True   True  False  False
080          False  False   True   True   True  False
081           True   True   True  False  False  False
082           True   True   True   True   True  False
083           True  False   True  False  False  False
084           True  False   True  False   True  False
085           True   True   True  False   True  False
086           True  False   True  False   True  False
087           True   True   True  False   True  False
088           True  False   True  False   True  False
089           True   True   True   True  False  False
090           True   True   True  False   True  False
091           True  False   True  False   True  False
092           True  False   True  False  False  False
093           True  False   True   True  False  False
094           True  False   True  False  False  False
095           True   True   True  False   True  False
096           True   True   True  False   True  False
097           True  False   True  False   True  False
098           True  False   True  False   True  False
099           True   True   True  False  False  False
100           True  False   True  False   True  False
101           True  False   True  False  False  False
102           True   True   True  False   True  False
```

## Failure examples

One constraint GPT failure (id = 004):
Prompt:
```
Initially:
The writing pad rests on the table.
The notebook is on the writing pad.
The tissue box is on the notebook.
There is nothing on the tissue box.
The tablet rests on the table.
There is nothing on the tablet.

Goal:
There is nothing on the notebook.

Actions:
```

Response:
```
Move the tablet onto the notebook.
```


# Guide to using repo

## Problem generation

Write a yaml file that describes all the testcases.

For example, in `dataset/simple_stack/cogsci_problems.yaml`.

Then, run

```
python batch_generate_problems.py --specs-file dataset/simple_stack/cogsci_problems.yaml --problem-path dataset/simple_stack/problems
```

This generates the problems in our abstract format, serialized in json, in the problem directory `dataset/simple_stack/problems`

## Codex LOT planner
First, generate the Codex translation examples, meant as the prompt for codex.
This contains pairs of configuration description in natural language and its corresponding translation in pddl.

```
for view in 'one' 'two' 'all'; do
    python batch_generate_codex_examples.py \
        --specs-file dataset/simple_stack/cogsci_problems.yaml\
        --problem-path dataset/simple_stack/problems\
        --output-path "dataset/simple_stack/codex_translations/${view}"\
        --view ${view}
done
```

This generates the prompts in `dataset/simple_stack/codex_translations/${view}/collated.txt`

Next, we can run the Codex LOT planner. Note that this uses Open AI's codex api, which requires you to have a key. You have to get a key, and set it in your environment variable by running something like:
```
export OPENAI_API_KEY=XXXX
```
before running the codex command below:
```
for view in 'one' 'two' 'all'; do
    python batch_codex_translate.py \
        --specs-file dataset/simple_stack/cogsci_problems.yaml \
        --problem-path dataset/simple_stack/problems\
        --prompt-path "dataset/simple_stack/codex_translations/${view}/collated.txt" \
        --output-path "codex_translations/${view}/" \
        --view ${view}
done
```

Output path is where the program dumps a json file, `collated.json` of whether each test case succeeds or not.

## Language model planning
First generate the gpt examples for planning.

```
for view in 'one' 'two' 'all'; do
    python batch_generate_prompts.py \
        --specs-file dataset/simple_stack/cogsci_problems.yaml\
        --problem-path dataset/simple_stack/problems\
        --plan-path "dataset/simple_stack/problems/plans/${view}" \
        --output-path "dataset/simple_stack/gpt3_prompts/${view}" \
        --output-type nl \
        --view ${view}
done
```

This produces a set of plans in `plans/${view}`, and the set of GPT3 examples in `gpt3_prompts/${view}`.

Then, run the language model planner. Before running the GPT-Neo model, you have to download the model, perhaps using the `download_model` function in `gpt/gpt.py`, and then configure the `MODEL_DIR` variable in the same file accordingly. 

```
for view in 'one' 'two' 'all'; do
    python batch_lm_plan.py \
        --specs-file dataset/simple_stack/cogsci_problems.yaml\
        --problem-path dataset/simple_stack/problems\
        --output-path "nl_plans/${view}/" \
        --prompt-path "dataset/simple_stack/gpt3_prompts/${view}/collated.txt" \
        --output-type nl \
        --engine-type gptneo \
        --view ${view}
done
```

Again, in output-path you will find a `collated.json` that describes the output.

## Results consolidation

There is a small notebook `consolidate_results.ipynb` that pulls all the individual `collated.json` files and generate a big dataframe.