
# Hurwitz Lab Theme

## Hurwitz Lab Colors

The following variable, `hurwitz_colors`, holds the Hurwitz Lab colors. The first eleven colors follow the Hurwitz Lab theme and the last five are random colors in case there is more keys in the data. 

     hurwitz_colors <- c("#018d97", "#f5811f", "gold", "#61cddc", "#6a6a6a", "tomato4", "tan", "darkslategray1", "gray20", "gray80", "burlywood4", "red", "yellow", "darkgreen", "blue", "purple")
     
![The First Eleven Hurwitz Theme Colors in Order](https://github.com/shelbynelson/summer-internship/blob/master/hurwitz-lab-theme-r/Hurwitz_Lab_Colors.jpg)

This variable is intended to be used in the ggplot line of code. The following is an example of how it would be used.

     scale_fill_manual(values = hurwitz_colors)


## Hurwitz Lab Theme Descriptive Code

The following code block puts the theme into the `hurwitz_theme` variable. Each line includes an element in the theme followed by a short description of the element and the "default" for this theme. For example, the first element is text and this sets all of the text throughout the plot to be the same font, size, and color. 
     
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
## Hurwitz Lab Theme Code

The following code block is a condensed and cleaned up version of the above descriptive code.

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

## All Code Needed to Use the Theme 

The following code block includes all of the code you would need to be able to use the Hurwitz colors, theme, and font. Here is the actual [script](https://github.com/shelbynelson/summer-internship/blob/master/hurwitz-lab-theme-r/Hurwitz_Theme_Code.R) for the theme code. Sidenote: `loadfonts(device = 'win')` loads the fonts onto a windows device.

     library(tidyverse)
     library(extrafont)
     font_import()
     fonts()
     loadfonts(device = 'win')	

     hurwitz_colors <- c("#018d97", "#f5811f", "gold", "#61cddc", "#6a6a6a", "tomato4", "tan", "darkslategray1", "gray20", "gray80", "burlywood4", "red", "yellow", "darkgreen", "blue", "purple")
     
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




