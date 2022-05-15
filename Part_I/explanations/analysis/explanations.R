# Setup
library(stringr)
library(dplyr)
## for analysis
library(tidyverse)
library(lme4)
library(lmerTest)
library(emmeans)
library(lmtest)
library(influence.ME)

# load data
exp_raw <- read.csv("./data/goodness_ratings/human_rated_goodness.csv")

# parsing and filtering
exp = subset(exp_raw, trial_type == "survey-likert")
exp$response

exp$response = str_remove_all(exp$response, "[{\"goodness\":}]")

exp$response = strtoi(exp$response, base=0L)

# convert to Likert scale 1-7
exp$response = exp$response + 1
exp$response

exp$prompt = str_remove_all(exp$prompt, "Scenario: ")


# Check Number of Participants
# Human
exp_human = subset(exp, subj_id == "human")
human_raters <- unique(exp_human$subject_id)
length(human_raters) # 182

# GPT-3
exp_gpt3 = subset(exp, subj_id == "gpt-3")
gpt3_raters <- unique(exp_gpt3$subject_id)
length(gpt3_raters) # 182


# Check Number of Evaluators
evaluators <- unique(exp$subject_id)
length(evaluators) #182
# Number of Evaluators by goal type
# unconstrained
unconstrained = subset(exp, goal_type == "unconstrained" & trial_type == "survey-likert")
unconst_eval <- unique(unconstrained$subject_id)
length(unconst_eval) # 60

# single constraint
single_const = subset(exp, goal_type == "constrained_single" & trial_type == "survey-likert")
sing_eval <- unique(single_const$subject_id)
length(sing_eval) # 62

# many constraints
many_const = subset(exp, goal_type == "constrained_many" & trial_type == "survey-likert")
many_eval <- unique(many_const$subject_id)
length(many_eval) # 60

# Check all plans have been seen by >= 3 people
rating_data <- subset(exp, trial_type == "survey-likert")
unique_plans <- unique(rating_data$plan)
c_plans <- 0
for (p in unique_plans) {
  data_p <- subset(rating_data, plan=p)
  unique_raters_p <- unique(data_p$subject_id)
  if (length(unique_raters_p) >= 3) c_plans = c_plans+1
}
c_plans == length(unique_plans)

# -----------------------------------------------------------

# Q1

# Aggregate: Goodness ~ Planner_Type + (1 | Rater.ID)
agg <- lmer(response ~ subj_id + (1|subject_id), data = exp)
summary(agg)
plot(agg, xlab="Goodness Rating", ylab="Residuals")
# LR-test
h0_agg <- lmer(response ~ (1|subject_id), data = exp)
lrtest(h0_agg, agg)

# unconstrained, aggregate
agg_un <- lmer(response ~ subj_id + (1|subject_id), data = unconstrained)
summary(agg_un)
plot(agg_un, xlab="Goodness Rating", ylab="Residuals")
# LR-test
h0_agg_un <- lmer(response ~ (1|subject_id), data = unconstrained)
lrtest(h0_agg_un, agg_un)

# single constraint, aggregate
agg_sing <- lmer(response ~ subj_id + (1|subject_id), data = single_const)
summary(agg_sing)
plot(agg_sing, xlab="Goodness Rating", ylab="Residuals")
# LR-test
h0_agg_sing <- lmer(response ~ (1|subject_id), data = single_const)
lrtest(h0_agg_sing, agg_sing)

# many constraints, aggregate
agg_many <- lmer(response ~ subj_id + (1|subject_id), data = many_const)
summary(agg_many)
plot(agg_many, xlab="Goodness Rating", ylab="Residuals")
# LR-test
h0_agg_many <- lmer(response ~ (1|subject_id), data = many_const)
lrtest(h0_agg_many, agg_many)


# Matched on Event: Goodness ~ Planner_Type + (1 | Rater.ID) + (1 | Prompt.ID) 
event <- lmer(response ~ subj_id + (1|subject_id) + (1|prompt), data = exp)
summary(event)
plot(event, xlab="Goodness Rating", ylab="Residuals")
# LR-test
h0_event <- lmer(response ~ (1|subject_id) + (1|prompt), data = exp)
lrtest(h0_event, event)

# unconstrained, matched on event
event_un <- lmer(response ~ subj_id + (1|subject_id) + (1|prompt), data = unconstrained)
summary(event_un)
plot(event_un, xlab="Goodness Rating", ylab="Residuals")
# LR-test
h0_event_un <- lmer(response ~ (1|subject_id) + (1|prompt), data = unconstrained)
lrtest(h0_event_un, event_un)

# single constraint, matched on event
event_sing <- lmer(response ~ subj_id + (1|subject_id) + (1|prompt), data = single_const)
summary(event_sing)
plot(event_sing, xlab="Goodness Rating", ylab="Residuals")
# LR-test
h0_event_sing <- lmer(response ~ (1|subject_id) + (1|prompt), data = single_const)
lrtest(h0_event_sing, event_sing)

# many constraints, matched on event
event_many <- lmer(response ~ subj_id + (1|subject_id) + (1|prompt), data = many_const)
summary(event_many)
plot(event_many, xlab="Goodness Rating", ylab="Residuals")
# LR-test
h0_event_many <- lmer(response ~ (1|subject_id) + (1|prompt), data = many_const)
lrtest(h0_event_many, event_many)


# -----------------------------------------------------------

# Q2

# Human Planners: Goodness ~ Constraint_Type  + (1 | Prompt.ID) + (1 | Rater.ID), within human data

human <- lmer(response ~ goal_type + (1|prompt) + (1|subject_id), data = exp_human)
summary(human)
plot(human, xlab="Goodness Rating", ylab="Residuals")

# null hypothesis: Goodness ~ (1 | Prompt.ID) + (1 | Rater.ID)
# compare to h0 using LR-test
h0_human <- lmer(response ~ (1|prompt) + (1|subject_id), data = exp_human)
lrtest(h0_human, human)

# GPT-3 Planners: Goodness ~ Constraint_Type  + (1 | Prompt.ID) + (1 | Rater.ID), within GPT-3 data

gpt3 <- lmer(response ~ goal_type + (1|prompt) + (1|subject_id), data = exp_gpt3)
summary(gpt3)
plot(gpt3, xlab="Goodness Rating", ylab="Residuals")

# null hypothesis: Goodness ~ (1 | Prompt.ID) + (1 | Rater.ID)
# compare to h0 using LR-test
h0_gpt3 <- lmer(response ~ (1|prompt) + (1|subject_id), data = exp_gpt3)
lrtest(h0_gpt3, gpt3)

unique(exp_gpt3$goal_type)

# -----------------------------------------------------------

# Q3
# Goodness ~ (Planner_Type * Constraint_Type) + Planner_Type + Constraint_Type + (1 | Rater.ID) + (1 | Prompt.ID) 
exp_q3 <- lmer(response ~ (subj_id * goal_type) + subj_id + goal_type + (1|subject_id) + (1|prompt), data=exp)
summary(exp_q3)
plot(exp_q3, xlab="Goodness Rating", ylab="Residuals")

# null model: Goodness ~ Planner_Type + Constraint_Type + (1 | Rater.ID) + (1 | Prompt.ID) 
h0_q3 <- lmer(response ~ subj_id + goal_type + (1|subject_id) + (1|prompt), data=exp)
# LR-test
lrtest(h0_q3, exp_q3)


# Unconstrained vs Single Constraints
unsing <- exp[!(exp$goal_type == "constrained_many"),]

## Human
unsing_human = subset(unsing, subj_id == "human")

exp_unsing_human <- lmer(response ~ goal_type + (1|subject_id) + (1|prompt), data=unsing_human)
summary(exp_unsing_human)

# null model
h0_unsing_human <- lmer(response ~ (1|subject_id) + (1|prompt), data=unsing_human)
# LR-test
lrtest(h0_unsing_human, exp_unsing_human)


## GPT-3
unsing_gpt3 = subset(unsing, subj_id == "gpt-3")

exp_unsing_gpt3 <- lmer(response ~ goal_type + (1|subject_id) + (1|prompt), data=unsing_gpt3)
summary(exp_unsing_gpt3)

# null model
h0_unsing_gpt3 <- lmer(response ~ (1|subject_id) + (1|prompt), data=unsing_gpt3)
# LR-test
lrtest(h0_unsing_gpt3, exp_unsing_gpt3)



# Unconstrained vs Many Constraints
unmany <- exp[!(exp$goal_type == "constrained_single"),]

## Human
unmany_human = subset(unmany, subj_id == "human")

exp_unmany_human <- lmer(response ~ goal_type + (1|subject_id) + (1|prompt), data=unmany_human)
summary(exp_unmany_human)

# null model
h0_unmany_human <- lmer(response ~ (1|subject_id) + (1|prompt), data=unmany_human)
# LR-test
lrtest(h0_unmany_human, exp_unmany_human)


## GPT-3
unmany_gpt3 = subset(unmany, subj_id == "gpt-3")

exp_unmany_gpt3 <- lmer(response ~ goal_type + (1|subject_id) + (1|prompt), data=unmany_gpt3)
summary(exp_unmany_gpt3)

# null model
h0_unmany_gpt3 <- lmer(response ~ (1|subject_id) + (1|prompt), data=unmany_gpt3)
# LR-test
lrtest(h0_unmany_gpt3, exp_unmany_gpt3)



# Single Constraints vs Many Constraints
singmany <- exp[!(exp$goal_type == "unconstrained"),]

## Human
singmany_human = subset(singmany, subj_id == "human")

exp_singmany_human <- lmer(response ~ goal_type + (1|subject_id) + (1|prompt), data=singmany_human)
summary(exp_singmany_human)

# null model
h0_singmany_human <- lmer(response ~ (1|subject_id) + (1|prompt), data=singmany_human)
# LR-test
lrtest(h0_singmany_human, exp_singmany_human)


## GPT-3
singmany_gpt3 = subset(singmany, subj_id == "gpt-3")

exp_singmany_gpt3 <- lmer(response ~ goal_type + (1|subject_id) + (1|prompt), data=singmany_gpt3)
summary(exp_singmany_gpt3)

# null model
h0_singmany_gpt3 <- lmer(response ~ (1|subject_id) + (1|prompt), data=singmany_gpt3)
# LR-test
lrtest(h0_singmany_gpt3, exp_singmany_gpt3)


# -----------------------------------------------------------

# Q4

# load typicality data
typ_data <- read.csv("./data/typicality_ratings/typicality.csv", header=TRUE, quote="\"")
colnames(typ_data)[which(names(typ_data) == "Scenario")] <- "prompt"
merged_typ <- merge(unconstrained, typ_data, by="prompt")

# Does typicality matter?
# Goodness ~ Typicality + (1 | Rater.ID) + (1 | Prompt.ID)

## Human
human_typ = subset(merged_typ, subj_id == "human")
exp1_q4_1_human <- lmer(response ~ Freq.X + (1|subject_id) + (1|prompt), data=human_typ)
summary(exp1_q4_1_human)

# null model: Goodness ~ (1 | Rater.ID) + (1 | Prompt.ID)
h0_q4_1_human <- lmer(response ~ (1|subject_id) + (1|prompt), data=human_typ)
# LR-test
lrtest(h0_q4_1_human, exp1_q4_1_human)


## GPT-3
gpt3_typ = subset(merged_typ, subj_id == "gpt-3")
exp1_q4_1_human <- lmer(response ~ Freq.X + (1|subject_id) + (1|prompt), data=gpt3_typ)
summary(exp1_q4_1_human)

# null model: Goodness ~ (1 | Rater.ID) + (1 | Prompt.ID)
h0_q4_1_human <- lmer(response ~ (1|subject_id) + (1|prompt), data=gpt3_typ)
# LR-test
lrtest(h0_q4_1_human, exp1_q4_1_human)



# Does typicality matter more for GPT-3?
# Goodness ~ (Planner_Type * Typicality) + Planner_Type + Typicality + (1 | Rater.ID) + (1 | Prompt.ID)
exp1_q4_2 <- lmer(response ~ (subj_id * Freq.X) + subj_id + Freq.X + (1|subject_id) + (1|prompt), data=merged_typ)
summary(exp1_q4_2)
plot(exp1_q4_2, xlab="Goodness Rating", ylab="Residuals")

# null model: Goodness ~ Planner_Type + Typicality + (1 | Rater.ID) + (1 | Prompt.ID)
h0_q4_2 <- lmer(response ~ subj_id + Freq.X + (1|subject_id) + (1|prompt), data=merged_typ)
# LR-test
lrtest(h0_q4_2, exp1_q4_2)