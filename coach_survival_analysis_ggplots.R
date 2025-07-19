
library(ggplot2)


vars <- c('Experience', 'Black', 'Division Wins', 'Playoff Apps', 'Playoff Win Pct', 'Win Pct', 'OSRS',
          'DSRS', 'Super Bowl Champion', 'Black x Experience', 'Rooney Rule', 'Black x Rooney Rule')
coefs <- c(-0.206, 1.295, 0.111, -0.373, -0.938, -1.299, -0.036, -0.010, 0.523 -0.074, 0.071, -0.732)
serrs <- c(0.021, 0.559, 0.096, 0.076, 0.348, 0.799, 0.029, 0.029, 0.293, 0.055, 0.134, 0.542)


data1 <- as.data.frame(cbind(vars, coefs, serrs))
data1$coefs <- as.numeric(data1$coefs)
data1$serrs <- as.numeric(data1$serrs)
data1 <- data1[order(data1$coefs),]
data1$ids <- 1:nrow(data1)
row.names(data1) <- NULL


ggplot(data1, aes(x = ids, y = coefs)) +
  geom_point(size = 3) +
  geom_errorbar(aes(ymin = coefs - 1.96*serrs, ymax = coefs + 1.96*serrs), width = 0.2) +
  labs(title = 'Hazard Model Results with Team Fixed Effects', x = '', y = 'log(Hazard Ratio) (95% CI)') +
  theme_minimal() + 
  theme(plot.title = element_text(hjust = 0.5)) +
  scale_x_discrete(limits = data1$vars) +
  geom_line(y = 0) + 
  ylim(c(-3,3)) +
  scale_y_continuous(breaks = seq(-2, 2, 1), labels = seq(-2, 2, 1)) +
  coord_flip()


vars2 <- c('Experience', 'Black', 'Division Wins', 'Playoff Apps', 'Playoff Win Pct', 'Win Pct', 'OSRS',
           'DSRS', 'Super Bowl Champion', 'Black x Experience', 'Rooney Rule', 'Black x Rooney Rule')
coefs2 <- c(-0.206, 1.400, 0.102, -0.347, -0.895, -0.810, -0.043, -0.022, 0.346, -0.111, 0.127, -0.709)
serrs2 <- c(0.021, 0.533, 0.090, 0.074, 0.323, 0.749, 0.027, 0.027, 0.278, 0.050, 0.120, 0.517)


data2 <- as.data.frame(cbind(vars2, coefs2, serrs2))
data2$coefs2 <- as.numeric(data2$coefs2)
data2$serrs2 <- as.numeric(data2$serrs2)
data2 <- data2[order(data2$coefs2),]
data2$ids <- 1:nrow(data2)
row.names(data2) <- NULL


ggplot(data2, aes(x = ids, y = coefs2)) +
  geom_point(size = 3) +
  geom_errorbar(aes(ymin = coefs2 - 1.96*serrs2, ymax = coefs2 + 1.96*serrs2), width = 0.2) +
  labs(title = 'Hazard Model Results without Team Fixed Effects', x = '', y = 'log(Hazard Ratio) (95% CI)') +
  theme_minimal() + 
  theme(plot.title = element_text(hjust = 0.5)) +
  scale_x_discrete(limits = data2$vars2) +
  geom_line(y = 0) + 
  ylim(c(-3,3)) +
  scale_y_continuous(breaks = seq(-2, 2, 1), labels = seq(-2, 2, 1)) +
  coord_flip()





