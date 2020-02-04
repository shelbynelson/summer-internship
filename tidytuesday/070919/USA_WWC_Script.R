#Shelby Nelson
#071019
#Women's World Cup TidyTuesday 

library(tidyverse)

wwc_outcomes <- readr::read_csv("https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2019/2019-07-09/wwc_outcomes.csv")

ggplot(data = filter(wwc_outcomes,team=="USA"))+geom_point(mapping=aes(x=year,y=score),color="blue")+geom_smooth(mapping=aes(x=year,y=score),se=FALSE)+labs(title="USA's Women's World Cup Scores",subtitle= "1991-2019",x="Year",y="Score")
