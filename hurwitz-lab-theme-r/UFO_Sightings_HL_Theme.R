#Shelby Nelson
#07/16/2019
#UFO Sighting Data from tidytuesday 06/25/2019, this code plots the UFO shape per year in Tucson, Arizona in July-December from 1990-2015 using the Hurwitz theme 

library(tidyverse)
library(lubridate)
library(extrafont)
font_import()
fonts()
loadfonts(device = 'win')

#--------COLORS--------------------------------------------------------------------------------

hurwitz_colors <- c("#018d97", "#f5811f", "gold", "#61cddc", "#6a6a6a", "tomato4", "tan", "darkslategray1", "gray20", "gray80", "burlywood4", "red", "yellow", "darkgreen", "blue", "purple")



#--------THEME---------------------------------------------------------------------------------   

hurwitz_theme <- theme(text = element_text(family = "Times New Roman",      
                                           size = 15,
                                           color = "black"),
                       panel.background = element_rect(fill = "#f8f8f8"),   
                       panel.grid = element_blank(),                        
                       panel.spacing = unit(0.2, "line"),                   
                       axis.ticks = element_blank(),                        
                       axis.line = element_line(color = "black"),           
                       axis.text.x = element_text(size = 15,                
                                                  angle = 45,
                                                  hjust = 1),
                       axis.text.y = element_text(size = 15),               
                       axis.title = element_text(size = 17),                
                       plot.title = element_text(size = 20,                 
                                                 hjust = 0.5),
                       plot.subtitle = element_text(size = 15,              
                                                    hjust = 0.5),
                       legend.title = element_text(size = 17),              
                       legend.text = element_text(size = 15),               
                       legend.key = element_blank(),                        
                       legend.key.size = unit(1.5,"line"),                  
                       strip.background = element_rect(fill = "#eee4ce"))   


#----TRANSFORMING DATA-------------------------------------------------------------------------                       

ufo_sightings <- readr::read_csv("https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2019/2019-06-25/ufo_sightings.csv")

ufo_sightings_US <- 
  filter(ufo_sightings,
         country == "us",
         state == "az") %>%
  mutate(date_time = mdy_hm(date_time)) %>%
  mutate(year_spotted = year(date_time),
         month_spotted = month(date_time),
         day_spotted=day(date_time)) %>%
  filter(year_spotted >= 2000, year_spotted <= 2005, month_spotted > 6) %>%
  select(ufo_shape,
         year_spotted,
         month_spotted,
         day_spotted)

ufo_tucson <- 
  mutate(ufo_sightings_US, 
         ufo_shape = case_when(ufo_shape == "cigar" ~ "cigar/ cylinder",
                               ufo_shape == "cylinder" ~ "cigar/ cylinder",
                               ufo_shape == "unknown" ~ "other/ unknown",
                               ufo_shape == "other" ~ "other/ unknown",
                               ufo_shape == "circle" ~ "circle/ disk/ sphere",
                               ufo_shape == "disk" ~ "circle/ disk/ sphere",
                               ufo_shape == "sphere" ~ "circle/ disk/ sphere",
                               ufo_shape == "oval" ~ "egg/ oval",
                               ufo_shape == "egg" ~ "egg/ oval",
                               ufo_shape == "fireball" ~ "fireball/ flash/ light",
                               ufo_shape == "flash" ~ "fireball/ flash/ light",
                               ufo_shape == "light" ~ "fireball/ flash/ light",
                               TRUE ~ ufo_shape)) %>% 
  na.omit()


#------PLOTTING DATA----------------------------------------------------------------------------

ggplot(data = ufo_tucson) +
  geom_bar(mapping = aes(x = year_spotted,
                            y = ..count..,
                            fill = ufo_shape),
              
              width = 0.5,
              size = 4.2,
              stat = "count") +
  facet_wrap(~ month_spotted, nrow = 4)+
  
  scale_fill_manual(values = hurwitz_colors)+
  #scale_color_manual(values = hurwitz_colors)+
  labs(title = "UFO Sightings in Tucson, Arizona\n in July-December from 1990-2015",
       subtitle = "Created by Shelby Nelson @shelbynelson",
       x = "Year",
       y = "Number of Sightings",
       fill="UFO Shape") +
  hurwitz_theme

