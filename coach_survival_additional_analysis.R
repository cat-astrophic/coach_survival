# This script runs additional models for the exit discrimination paper

# Loading libraries

library(dplyr)
library(lmtest)
library(ggrepel)
library(ggplot2)
library(margins)
library(sandwich)
library(stargazer)

# Project directory

direc <- 'D:/coach_survival/'

# Reading in the data

df <- read.csv(paste0(direc, 'data/ref.csv'))

# Running linear probability models

mod <- lm(Y ~ log(1+Games)*Black + Black*Rooney + Win_Percentage + Any_Previous_Experience, data = df)
amod <- lm(Y ~ log(1+Games) + Black*Rooney + Win_Percentage + Any_Previous_Experience, data = df)
bmod <- lm(Y ~ log(1+Games) + Black*Rooney + Win_Percentage + Any_Previous_Experience, data = df[which(df$Black == 1),])
wmod <- lm(Y ~ log(1+Games) + Black*Rooney + Win_Percentage + Any_Previous_Experience, data = df[which(df$Black == 0),])

# Robust standard errors

modx <- coeftest(mod, vcov = vcovCL(mod, type = 'HC0'))
amodx <- coeftest(amod, vcov = vcovCL(amod, type = 'HC0'))
bmodx <- coeftest(bmod, vcov = vcovCL(bmod, type = 'HC0'))
wmodx <- coeftest(wmod, vcov = vcovCL(wmod, type = 'HC0'))

# Viewing results

stargazer(mod, modx, amod, amodx, bmod, bmodx, wmod, wmodx, type = 'text', omit.stat = c('f', 'ser'))

# Save results

write.csv(stargazer(modx, amodx, bmodx, wmodx), paste0(direc, 'results/additional_models.txt'), row.names = FALSE)

# Repeating linear probability models with Games4

mod <- lm(Y ~ Games4*Black + Black*Rooney + Win_Percentage + Any_Previous_Experience, data = df)
amod <- lm(Y ~ Games4 + Black*Rooney + Win_Percentage + Any_Previous_Experience, data = df)
bmod <- lm(Y ~ Games4 + Black*Rooney + Win_Percentage + Any_Previous_Experience, data = df[which(df$Black == 1),])
wmod <- lm(Y ~ Games4 + Black*Rooney + Win_Percentage + Any_Previous_Experience, data = df[which(df$Black == 0),])

# Robust standard errors

modx <- coeftest(mod, vcov = vcovCL(mod, type = 'HC0'))
amodx <- coeftest(amod, vcov = vcovCL(amod, type = 'HC0'))
bmodx <- coeftest(bmod, vcov = vcovCL(bmod, type = 'HC0'))
wmodx <- coeftest(wmod, vcov = vcovCL(wmod, type = 'HC0'))

# Viewing results

stargazer(mod, modx, amod, amodx, bmod, bmodx, wmod, wmodx, type = 'text', omit.stat = c('f', 'ser'))

# Save results

write.csv(stargazer(modx, amodx, bmodx, wmodx), paste0(direc, 'results/additional_models_4.txt'), row.names = FALSE)

# Repeating linear probability models with Games8

mod <- lm(Y ~ Games8*Black + Black*Rooney + Win_Percentage + Any_Previous_Experience, data = df)
amod <- lm(Y ~ Games8 + Black*Rooney + Win_Percentage + Any_Previous_Experience, data = df)
bmod <- lm(Y ~ Games8 + Black*Rooney + Win_Percentage + Any_Previous_Experience, data = df[which(df$Black == 1),])
wmod <- lm(Y ~ Games8 + Black*Rooney + Win_Percentage + Any_Previous_Experience, data = df[which(df$Black == 0),])

# Robust standard errors

modx <- coeftest(mod, vcov = vcovCL(mod, type = 'HC0'))
amodx <- coeftest(amod, vcov = vcovCL(amod, type = 'HC0'))
bmodx <- coeftest(bmod, vcov = vcovCL(bmod, type = 'HC0'))
wmodx <- coeftest(wmod, vcov = vcovCL(wmod, type = 'HC0'))

# Viewing results

stargazer(mod, modx, amod, amodx, bmod, bmodx, wmod, wmodx, type = 'text', omit.stat = c('f', 'ser'))

# Save results

write.csv(stargazer(modx, amodx, bmodx, wmodx), paste0(direc, 'results/additional_models_8.txt'), row.names = FALSE)

