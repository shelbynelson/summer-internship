#Shelby Nelson
#07/16/2019
#UFO Sighting Data from tidytuesday 06/25/2019, this code plots the UFO shape per year in Tucson, Arizona fro 1990-2015

library(tidyverse)
library(lubridate)
library(extrafont)
font_import()
fonts()
loadfonts(device = 'win')


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

#--------COLORS--------------------------------------------------------------------------------

hurwitz_colors <- c("#018d97", "#f5811f", "gold", "#61cddc", "#6a6a6a", "tomato4", "tan", "darkslategray1", "gray20", "gray80", "burlywood4", "red", "yellow", "darkgreen", "blue", "purple")



#--------THEME---------------------------------------------------------------------------------   

hurwitz_theme <- theme(text = element_text(family = "Times New Roman",      #This sets every text in the plot to the default: Times New Roman, size 15, black
                                           size = 15,
                                           color = "black"),
                       
                       panel.background = element_rect(fill = "#f8f8f8"),   #The background color of the plot. Default: light gray
                       
                       panel.grid = element_blank(),                        #The gridlines. Default: no gridlines
                       
                       panel.spacing = unit(0.2, "line"),                   #The spacing between facet panels. Default spacing: 0.2 for thin line
                       
                       axis.ticks = element_blank(),                        #The axis tick marks. Default: no tickmarks
                       
                       axis.line = element_line(color = "black"),           #The axis line. Default: black
                       
                       axis.text.x = element_text(size = 15,                #The X-axis text. Default: size 15, 45 deg angle, adjusted to fit below the X-axis
                                                  angle = 45,
                                                  hjust = 1),
                       
                       axis.text.y = element_text(size = 15),               #The Y-axis text, just like X-axis, you can adjust the size, angle, and placement. Default size: 15
                       
                       axis.title = element_text(size = 17),                #Both X and Y axis titles. Default size: 17
                       
                       plot.title = element_text(size = 20,                 #The title, left: hjust=0, centered: hjust=0.5, right: hjust=1. Default: size 20, centered: hjust = 0.5
                                                 hjust = 0.5),
                       
                       plot.subtitle = element_text(size = 15,              #The subtitle below the title. Default: size = 15, centered: hjust = 0.5
                                                    hjust = 0.5),
                       
                       legend.title = element_text(size = 17),              #The title of the legend. Default size: 17
                       
                       legend.text = element_text(size = 15),               #The text in the legend. Default size: 15
                       
                       legend.key = element_blank(),                        #The key/icon background. Default: no background
                       
                       legend.key.size = unit(1.5,"line"),                  #The size of the key/icon next to the text in the legend. Default: 1.5 units
                       
                       strip.background = element_rect(fill = "#eee4ce"))   #The facet title strip background color. Default: light tan

#---------------------------------------------------------------------------------------------                       



ggplot(data = ufo_tucson) +
  geom_bar(mapping = aes(x = year_spotted,
                            y = ..count..,
                            fill = ufo_shape),
              stroke = 1.75,
              
              width = 0.5,
              height = 0.25,
              size = 4.2,
              stat = "count") +
  facet_wrap(~ month_spotted, nrow = 4)+
  
  scale_fill_manual(values = hurwitz_colors)+
 # scale_color_manual(values = hurwitz_colors)+
  labs(title = "UFO Sightings in Tucson, Arizona from 1990-2015",
       subtitle = "Created by Shelby Nelson @shelbynelson",
       x = "Year",
       y = "Number of Sightings",
       fill="UFO Shape") +
  hurwitz_theme


  
