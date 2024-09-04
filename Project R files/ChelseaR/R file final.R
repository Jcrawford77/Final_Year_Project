#Read Datasets
chelsea <- read.csv('chelseaplayers.csv',stringsAsFactors = FALSE)
str(chelsea)
leagues <-read.csv('league.csv')



#extrafont::font_import()
extrafont :: loadfonts(device = "win")
#install.packages("ggrepel")

# load packages
library (tidyverse)
library (ggplot2)
library (lubridate)
library (ggrepel)
library (ggforce)
library (Cairo)

#show histograms
  

#histogram showing the chelsea players
hist(chelsea$sh90, main ="shots per 90", xlab= "sh90")

#histogram showing the chelsea players
hist(chelsea$Assists, main ="Top assists", xlab= "Assits")

#histogram showing the chelsea players
hist(chelsea$Apps, main ="Appearances", xlab= "Apperances")


#histogram showing the chelsea players
hist(chelsea$Goals, main ="Top Goal Scorers", xlab= "Goals")


#histogram showing the chelsea players
hist(chelsea$Min, main ="Minutes players", xlab= "Minutes played")

#histogram showing the chelsea players
hist(chelsea$xA, main ="Expected Assists", xlab= "Expected Assists")

#histogram showing the chelsea players
hist(chelsea$xA90, main ="Expected Assists per 90 minutes", xlab= "xA90")

#histogram showing the chelsea players
hist(chelsea$xG, main ="Expected Goals", xlab= "Expected Goals")

#histogram showing the chelsea players
hist(chelsea$xG90, main ="Expected Goals per 90", xlab= "xG90")

#histograms showing league dataset
#histogram showing the chelsea players
hist(leagues$Points, main ="Points", xlab= "Points")

#histogram showing the chelsea players
hist(leagues$Goal.Difference, main ="Goal Difference", xlab= "Goal Difference")

#histogram showing the chelsea players
hist(leagues$xG, main ="Expected Goals", xlab= "Expected Goals")

#GG PLOT
#gg plots did not function
#subsequenlty removed from code
#howver gg object for ggplot can be viewed in global environment

#Scatterplot
#ScatterplotS
plot(x= chelsea$Apps, y = chelsea$Goals,
     main = "scatterplot of Goals by Appearances",
     ylab = "Goals")

plot(x= chelsea$xG, y = chelsea$Goals,
     main = "Expected Goals v Goals",
     ylab = "Goals")

plot(x= chelsea$xA, y = chelsea$Assists,
     main = "Expected Assists v Assists",
     ylab = "Assists")

#scatterplot for league data
plot(x= leagues$xG.Points, y = leagues$Points,
     main = "Expected Points v Points league",
     ylab = "Points")

#Prediction Tool
#Knn


