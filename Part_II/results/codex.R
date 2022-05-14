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
exp_codex <- read.csv('final-output.csv')
exp_codex$succeed <- as.logical(exp_codex$succeed)
drop <- c("gpt_prompt", "gpt_res")
exp_codex = exp_codex[,!(names(exp_codex) %in% drop)]

one <- subset(exp_codex, constraints == "one")
two <- subset(exp_codex, constraints == "two")
all <- subset(exp_codex, constraints == "all")

codex <- subset(exp_codex, method == "codex")
gpt <- subset(exp_codex, method == "gpt")

one_two <- exp_codex[!(exp_codex$constraints == "all"),]
one_all <- exp_codex[!(exp_codex$constraints == "two"),]
two_all <- exp_codex[!(exp_codex$constraints == "one"),]

# -----------------------------------------------------------

# Q1

# Matched on prompt: succeed ~ method + (1 | id)
prompt <- lmer(succeed ~ method + (1 | id), data=exp_codex)
summary(prompt)
# LR-test
h0_prompt <- lmer(succeed ~ (1 | id), data=exp_codex)
lrtest(h0_prompt, prompt)

# one constraint
prompt_1 <- lmer(succeed ~ method + (1 | id), data=one)
summary(prompt_1)
# LR-test
h0_prompt_1 <- lmer(succeed ~ (1 | id), data=one)
lrtest(h0_prompt_1, prompt_1)

# two constraints
prompt_2 <- lmer(succeed ~ method + (1 | id), data=two)
summary(prompt_2)
# LR-test
h0_prompt_2 <- lmer(succeed ~ (1 | id), data=two)
lrtest(h0_prompt_2, prompt_2)

# all constraints
prompt_all <- lmer(succeed ~ method + (1 | id), data=all)
summary(prompt_all)
# LR-test
h0_prompt_all <- lmer(succeed ~ (1 | id), data=all)
lrtest(h0_prompt_all, prompt_all)


# -----------------------------------------------------------

# Q2

# succeed ~ constraints + (1 | id)
const <- lmer(succeed ~ constraints + (1 | id), data=exp_codex)
summary(const)
# LR-test
h0_const <- lmer(succeed ~ (1 | id), data=exp_codex)
lrtest(h0_const, const)

# codex
unique(codex$succeed)
codex_const <- lmer(succeed ~ constraints + (1 | id), data=codex)
summary(codex_const)
# LR-test
h0_codex <- lmer(succeed ~ (1 | id), data=codex)
lrtest(h0_codex, codex_const)

# gpt
gpt_const <- lmer(succeed ~ constraints + (1 | id), data=gpt)
summary(gpt_const)
# LR-test
h0_gpt <- lmer(succeed ~ (1 | id), data=gpt)
lrtest(h0_gpt, gpt_const)

# -----------------------------------------------------------

# Q3

# succeed ~ (method * constraints) + method + constraints + (1 | id)
both <- lmer(succeed ~ (method * constraints) + method + constraints + (1 | id), data=exp_codex)
summary(both)
# LR-test
h0_both <- lmer(succeed ~ method + constraints + (1 | id), data=exp_codex)
lrtest(h0_both, both)

# one constraint vs two constraints
onetwo <- lmer(succeed ~ (method * constraints) + method + constraints + (1 | id), data=one_two)
summary(onetwo)
# LR-test
h0_onetwo <- lmer(succeed ~ method + constraints + (1 | id), data=one_two)
lrtest(h0_onetwo, onetwo)

## codex
codex_one_two = subset(one_two, method == "codex")

onetwo_codex <- lmer(succeed ~ constraints + (1 | id), data=codex_one_two)
summary(onetwo_codex)
# LR-test
h0_onetwo_codex <- lmer(succeed ~ (1 | id), data=codex_one_two)
lrtest(h0_onetwo_codex, onetwo_codex)


## gpt
gpt_one_two = subset(one_two, method == "gpt")

onetwo_gpt <- lmer(succeed ~ constraints + (1 | id), data=gpt_one_two)
summary(onetwo_gpt)
# LR-test
h0_onetwo_gpt <- lmer(succeed ~ (1 | id), data=gpt_one_two)
lrtest(h0_onetwo_gpt, onetwo_gpt)



# one constraint vs all constraints
oneall <- lmer(succeed ~ (method * constraints) + method + constraints + (1 | id), data=one_all)
summary(oneall)
# LR-test
h0_oneall <- lmer(succeed ~ method + constraints + (1 | id), data=one_all)
lrtest(h0_oneall, oneall)

## codex
codex_one_all = subset(one_all, method == "codex")

oneall_codex <- lmer(succeed ~ constraints + (1 | id), data=codex_one_all)
summary(oneall_codex)
# LR-test
h0_oneall_codex <- lmer(succeed ~ (1 | id), data=codex_one_all)
lrtest(h0_oneall_codex, oneall_codex)


## gpt
gpt_one_all = subset(one_all, method == "gpt")

oneall_gpt <- lmer(succeed ~ constraints + (1 | id), data=gpt_one_all)
summary(oneall_gpt)
# LR-test
h0_oneall_gpt <- lmer(succeed ~ (1 | id), data=gpt_one_all)
lrtest(h0_oneall_gpt, oneall_gpt)



# two constraints vs all constraints
twoall <- lmer(succeed ~ (method * constraints) + method + constraints + (1 | id), data=two_all)
summary(twoall)
# LR-test
h0_twoall <- lmer(succeed ~ method + constraints + (1 | id), data=two_all)
lrtest(h0_twoall, twoall)

## codex
codex_two_all = subset(two_all, method == "codex")

twoall_codex <- lmer(succeed ~ constraints + (1 | id), data=codex_two_all)
summary(twoall_codex)
# LR-test
h0_twoall_codex <- lmer(succeed ~ (1 | id), data=codex_two_all)
lrtest(h0_twoall_codex, twoall_codex)

## gpt
gpt_two_all = subset(two_all, method == "gpt")

twoall_gpt <- lmer(succeed ~ constraints + (1 | id), data=gpt_two_all)
summary(twoall_gpt)
# LR-test
h0_twoall_gpt <- lmer(succeed ~ (1 | id), data=gpt_two_all)
lrtest(h0_twoall_gpt, twoall_gpt)

