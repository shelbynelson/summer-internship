#Here is the code needed to run and use the Hurwitz colors, theme, and font.

library(tidyverse)
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