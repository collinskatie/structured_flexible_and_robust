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
# 15-shot
plans_raw <- read.csv("./data/goodness_ratings/human_rated_goodness.csv")
dim(plans_raw)

plans <- plans_raw
dim(plans)

# parsing and filtering
plans = subset(plans_raw, trial_type == "survey-likert")
plans$response

plans$response = str_remove_all(plans$response, "[{\"goodness\":}]")

plans$response = strtoi(plans$response, base=0L)

# convert to Likert scale 1-7
plans$response = plans$response + 1

plans$response

plans.long <- melt(plans, id.vars = c("subject_id", "response", "prompt", "subj_id", 
                                    "plan", "goal_type"))
plans.long$response <- as.numeric(plans.long$response)

# -----------------------------------------------------------

# Check Number of Participants
# Human
plans_human = subset(plans, subj_id == "human")
human_raters <- unique(plans_human$subject_id)
length(human_raters) # 190

# GPT-3
plans_gpt3 = subset(plans, subj_id == "gpt-3")
gpt3_raters <- unique(plans_gpt3$subject_id)
length(gpt3_raters) # 190


# Check Number of Evaluators
evaluators <- unique(plans$subject_id)
length(evaluators) #190
# Number of Evaluators by goal type
# unconstrained
unconstrained = subset(plans, goal_type == "unconstrained" & trial_type == "survey-likert")
unconst_eval <- unique(unconstrained$subject_id)
length(unconst_eval) # 62

# single constraint
single_const = subset(plans, goal_type == "constrained_single" & trial_type == "survey-likert")
sing_eval <- unique(single_const$subject_id)
length(sing_eval) # 66

# many constraints
many_const = subset(plans, goal_type == "constrained_many" & trial_type == "survey-likert")
many_eval <- unique(many_const$subject_id)
length(many_eval) # 65

# Check all plans have been seen by >= 3 people
rating_data <- subset(plans, trial_type == "survey-likert")
unique_plans <- unique(rating_data$plan)
c_plans <- 0
for (p in unique_plans) {
  data_p <- subset(rating_data, plan=p)
  unique_raters_p <- unique(data_p$subject_id)
  if (length(unique_raters_p) >= 3) c_plans = c_plans+1
}
c_plans == length(unique_plans)

hist(plans$response, xlab="goodness rating")

# -----------------------------------------------------------

# Q1

# Aggregate: Goodness ~ Planner_Type + (1 | Rater.ID)
agg <- lmer(response ~ subj_id + (1|subject_id), data = plans)
summary(agg)
plot(agg, xlab="Goodness Rating", ylab="Residuals")
plot(allEffects(agg))

# LR-test
h0_agg <- lmer(response ~ (1|subject_id), data = plans)
lrtest(h0_agg, agg)

# unconstrained, aggregate
agg_un <- lmer(response ~ subj_id + (1|subject_id), data = unconstrained)
summary(agg_un)
plot(agg_un, xlab="Goodness Rating", ylab="Residuals")
plot(allEffects(agg_un))
# LR-test
h0_agg_un <- lmer(response ~ (1|subject_id), data = unconstrained)
lrtest(h0_agg_un, agg_un)

# single constraint, aggregate
agg_sing <- lmer(response ~ subj_id + (1|subject_id), data = single_const)
summary(agg_sing)
plot(agg_sing, xlab="Goodness Rating", ylab="Residuals")
plot(allEffects(agg_sing))
# LR-test
h0_agg_sing <- lmer(response ~ (1|subject_id), data = single_const)
lrtest(h0_agg_sing, agg_sing)

# many constraints, aggregate
agg_many <- lmer(response ~ subj_id + (1|subject_id), data = many_const)
summary(agg_many)
plot(agg_many, xlab="Goodness Rating", ylab="Residuals")
plot(allEffects(agg_many))
# LR-test
h0_agg_many <- lmer(response ~ (1|subject_id), data = many_const)
lrtest(h0_agg_many, agg_many)


# Matched on Goal: Goodness ~ Planner_Type + (1 | Rater.ID) + (1 | Prompt.ID) 
goal <- lmer(response ~ subj_id + (1|subject_id) + (1|prompt), data = plans)
summary(goal)
plot(goal, xlab="Goodness Rating", ylab="Residuals")
# LR-test
h0_goal <- lmer(response ~ (1|subject_id) + (1|prompt), data = plans)
lrtest(h0_goal, goal)

# unconstrained, matched on goal
goal_un <- lmer(response ~ subj_id + (1|subject_id) + (1|prompt), data = unconstrained)
summary(goal_un)
plot(goal_un, xlab="Goodness Rating", ylab="Residuals")
# LR-test
h0_goal_un <- lmer(response ~ (1|subject_id) + (1|prompt), data = unconstrained)
lrtest(h0_goal_un, goal_un)

# single constraint, matched on goal
goal_sing <- lmer(response ~ subj_id + (1|subject_id) + (1|prompt), data = single_const)
summary(goal_sing)
plot(goal_sing, xlab="Goodness Rating", ylab="Residuals")
# LR-test
h0_goal_sing <- lmer(response ~ (1|subject_id) + (1|prompt), data = single_const)
lrtest(h0_goal_sing, goal_sing)

# many constraints, matched on goal
goal_many <- lmer(response ~ subj_id + (1|subject_id) + (1|prompt), data = many_const)
summary(goal_many)
plot(goal_many, xlab="Goodness Rating", ylab="Residuals")
# LR-test
h0_goal_many <- lmer(response ~ (1|subject_id) + (1|prompt), data = many_const)
lrtest(h0_goal_many, goal_many)

# -----------------------------------------------------------

# Q2
# Human Planners: Goodness ~ Constraint_Type  + (1 | Prompt.ID) + (1 | Rater.ID), within human data

human <- lmer(response ~ goal_type + (1|prompt) + (1|subject_id), data = plans_human)
summary(human)
plot(human, xlab="Goodness Rating", ylab="Residuals")

# null hypothesis: Goodness ~ (1 | Prompt.ID) + (1 | Rater.ID)
# compare to h0 using LR-test
h0_human <- lmer(response ~ (1|prompt) + (1|subject_id), data = plans_human)
lrtest(h0_human, human)

# GPT-3 Planners: Goodness ~ Constraint_Type  + (1 | Prompt.ID) + (1 | Rater.ID), within GPT-3 data

gpt3 <- lmer(response ~ goal_type + (1|prompt) + (1|subject_id), data = plans_gpt3)
summary(gpt3)
plot(gpt3, xlab="Goodness Rating", ylab="Residuals")

# null hypothesis: Goodness ~ (1 | Prompt.ID) + (1 | Rater.ID)
# compare to h0 using LR-test
h0_gpt3 <- lmer(response ~ (1|prompt) + (1|subject_id), data = plans_gpt3)
lrtest(h0_gpt3, gpt3)

# -----------------------------------------------------------

# Q3
# Goodness ~ (Planner_Type * Constraint_Type) + Planner_Type + Constraint_Type + (1 | Rater.ID) + (1 | Prompt.ID) 
plans_q3 <- lmer(response ~ (subj_id * goal_type) + subj_id + goal_type + (1|subject_id) + (1|prompt), data=plans)
summary(plans_q3)
plot(plans_q3, xlab="Goodness Rating", ylab="Residuals")

# null model: Goodness ~ Planner_Type + Constraint_Type + (1 | Rater.ID) + (1 | Prompt.ID) 
h0_q3 <- lmer(response ~ subj_id + goal_type + (1|subject_id) + (1|prompt), data=plans)
# LR-test
lrtest(h0_q3, plans_q3)


# Unconstrained vs Single Constraints
unsing <- plans[!(plans$goal_type == "constrained_many"),]

## Human
unsing_human = subset(unsing, subj_id == "human")
plans_unsing_human <- lmer(response ~ goal_type + (1|subject_id) + (1|prompt), data=unsing_human)
summary(plans_unsing_human)

# null model
h0_unsing_human <- lmer(response ~ (1|subject_id) + (1|prompt), data=unsing_human)
# LR-test
lrtest(h0_unsing_human, plans_unsing_human)


## GPT-3
unsing_gpt3 = subset(unsing, subj_id == "gpt-3")
plans_unsing_gpt3 <- lmer(response ~ goal_type + (1|subject_id) + (1|prompt), data=unsing_gpt3)
summary(plans_unsing_gpt3)

# null model
h0_unsing_gpt3 <- lmer(response ~ (1|subject_id) + (1|prompt), data=unsing_gpt3)
# LR-test
lrtest(h0_unsing_gpt3, plans_unsing_gpt3)



# Unconstrained vs Many Constraints
unmany <- plans[!(plans$goal_type == "constrained_single"),]

## Human
unmany_human = subset(unmany, subj_id == "human")
plans_unmany_human <- lmer(response ~ goal_type + (1|subject_id) + (1|prompt), data=unmany_human)
summary(plans_unmany_human)

# null model
h0_unmany_human <- lmer(response ~ (1|subject_id) + (1|prompt), data=unmany_human)
# LR-test
lrtest(h0_unmany_human, plans_unmany_human)


## GPT-3
unmany_gpt3 = subset(unmany, subj_id == "gpt-3")
plans_unmany_gpt3 <- lmer(response ~ goal_type + (1|subject_id) + (1|prompt), data=unmany_gpt3)
summary(plans_unmany_gpt3)
plot(plans_unmany_gpt3, xlab="Goodness Rating", ylab="Residuals")

# null model
h0_unmany_gpt3 <- lmer(response ~ (1|subject_id) + (1|prompt), data=unmany_gpt3)
# LR-test
lrtest(h0_unmany_gpt3, plans_unmany_gpt3)



# Single Constraints vs Many Constraints
singmany <- plans[!(plans$goal_type == "unconstrained"),]

## Human
singmany_human = subset(singmany, subj_id == "human")

plans_singmany_human <- lmer(response ~ goal_type + (1|subject_id) + (1|prompt), data=singmany_human)
summary(plans_singmany_human)
plot(plans_singmany_human, xlab="Goodness Rating", ylab="Residuals")

# null model
h0_singmany_human <- lmer(response ~ (1|subject_id) + (1|prompt), data=singmany_human)
# LR-test
lrtest(h0_singmany_human, plans_singmany_human)


## GPT-3
singmany_gpt3 = subset(singmany, subj_id == "gpt-3")

plans_singmany_gpt3 <- lmer(response ~ goal_type + (1|subject_id) + (1|prompt), data=singmany_gpt3)
summary(plans_singmany_gpt3)
plot(plans_singmany_gpt3, xlab="Goodness Rating", ylab="Residuals")

# null model
h0_singmany_gpt3 <- lmer(response ~ (1|subject_id) + (1|prompt), data=singmany_gpt3)
# LR-test
lrtest(h0_singmany_gpt3, plans_singmany_gpt3)


# -----------------------------------------------------------

# Q4
# load typicality data
unconstrained$prompt = str_remove_all(unconstrained$prompt, "Goal: ")
typicality_data <- read.csv("./data/typicality_ratings/typicality.csv", header=TRUE, quote = "\"")
colnames(typicality_data)[which(names(typicality_data) == "Original.Goals")] <- "prompt"
merged_typicality <- merge(unconstrained, typicality_data, by="prompt")

# Does typicality matter?
# Goodness ~ Typicality + (1 | Rater.ID) + (1 | Prompt.ID)

## Human
typ_human = subset(merged_typicality, subj_id == "human")
plans_q4_1_human <- lmer(response ~ Avg.Rating + (1|subject_id) + (1|prompt), data=typ_human)
summary(plans_q4_1_human)

# null model: Goodness ~ (1 | Rater.ID) + (1 | Prompt.ID)
h0_q4_1_human <- lmer(response ~ (1|subject_id) + (1|prompt), data=typ_human)
# LR-test
lrtest(h0_q4_1_human, plans_q4_1_human)


## GPT-3
typ_gpt3 = subset(merged_typicality, subj_id == "gpt-3")
plans_q4_1_gpt3 <- lmer(response ~ Avg.Rating + (1|subject_id) + (1|prompt), data=typ_gpt3)
summary(plans_q4_1_gpt3)

# null model: Goodness ~ (1 | Rater.ID) + (1 | Prompt.ID)
h0_q4_1_gpt3 <- lmer(response ~ (1|subject_id) + (1|prompt), data=typ_gpt3)
# LR-test
lrtest(h0_q4_1_gpt3, plans_q4_1_gpt3)

# Does typicality matter more for GPT-3?
# Goodness ~ (Planner_Type * Typicality) + Planner_Type + Typicality + (1 | Rater.ID) + (1 | Prompt.ID)
plans_q4_2 <- lmer(response ~ (subj_id * Avg.Rating) + subj_id + Avg.Rating + (1|subject_id) + (1|prompt), data=merged_typicality)
summary(plans_q4_2)
plot(plans_q4_2, xlab="Goodness Rating", ylab="Residuals")

# null model: Goodness ~ Planner_Type + Typicality + (1 | Rater.ID) + (1 | Prompt.ID)
h0_q4_2 <- lmer(response ~ subj_id + Avg.Rating + (1|subject_id) + (1|prompt), data=merged_typicality)
# LR-test
lrtest(h0_q4_2, plans_q4_2)