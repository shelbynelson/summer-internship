#Shelby Nelson
#07/16/2019
#UFO Sighting Data from tidytuesday 06/25/2019

library(tidyverse)
library(lubridate)

ufo_sightings <- readr::read_csv("https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2019/2019-06-25/ufo_sightings.csv")

ufo_sightings_US <- filter(ufo_sightings, country == "us", state == "az", city_area == "tucson") %>% mutate(date_time = mdy_hm(date_time)) %>% mutate(year_spotted = year(date_time), month_spotted = month(date_time),day_spotted=day(date_time)) %>% filter(year_spotted >= 1990) %>% select(ufo_shape, year_spotted, month_spotted, day_spotted)

ufo_tucson <- mutate(ufo_sightings_US, ufo_shape = case_when(ufo_shape == "cigar"~"cigar/ cylinder",ufo_shape == "cylinder"~"cigar/ cylinder",ufo_shape == "unknown" ~ "other/ unknown",ufo_shape == "other" ~ "other/ unknown",ufo_shape == "circle" ~ "circle/ disk/ sphere",ufo_shape == "disk" ~ "circle/ disk/ sphere",ufo_shape == "sphere" ~ "circle/ disk/ sphere",ufo_shape == "oval" ~ "egg/ oval",ufo_shape == "egg"~"egg/ oval",ufo_shape== "fireball"~"fireball/ flash/ light",ufo_shape == "flash" ~ "fireball/ flash/ light",ufo_shape == "light"~"fireball/ flash/ light", TRUE ~ ufo_shape)) %>% na.omit()

ggplot(data=ufo_tucson)+geom_jitter(mapping=aes(x=year_spotted, y = ..count.., shape = ufo_shape),stroke=1.75,color="green4",width = 0.5,height = 0.25,size = 5,stat = "count")+scale_shape_manual(values=c(11,14,10,1,3,5,16,8,9,4,0,6,2))+labs(title="UFO Sightings in Tucson, Arizona from 1990-2015",subtitle="Created by Shelby Nelson @shelbynelson",x="Year",y="Number of Sightings")+theme(plot.background = element_rect(color = "black"),panel.background = element_rect(fill="paleturquoise"),panel.grid = element_line(color="tan"), axis.text=element_text(size = 13),axis.title = element_text(size = 16), plot.title = element_text(size=18),plot.subtitle=element_text(size = 16),legend.title = element_text(size=16),legend.text = element_text(size=13))
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
view(ufo_tucson)
