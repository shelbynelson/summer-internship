#Shelby Nelson @shelbynelson
#7/23/2019
#This code includes the Hurwitz Lab theme and colors. It also includes plots from the metadata from this American Gut Study: https://www.ebi.ac.uk/ena/data/view/PRJEB11419

library(tidyverse)
library(extrafont)
font_import()
fonts()
loadfonts(device = 'win')
library(ggplot2)
library(ggmap)
library(maps)
library(mapdata)
library(treemap)

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

#------COMBINING DATA----------------------------------------------------------------------

metadata <- read_tsv("C:/Users/Shelbeezy/work/summer-internship/metagenome-project/10317_20190722-115427.txt")

wgs_data <- read_tsv("C:/Users/Shelbeezy/work/summer-internship/metagenome-project/WGS_data.txt")

wgs_metadata <- inner_join(metadata,wgs_data, by = "sample_name")

#view(wgs_metadata)

#write_tsv(wgs_metadata,"C:/Users/Shelbeezy/work/summer-internship/metagenome-project/wgs_metadata.txt")

#------GENDER------------------------------------------------------------------------------

gender <- select(wgs_metadata, sex) %>%
       mutate(sex = case_when(sex == "Not provided" ~ "other/NA",
                              sex == "not provided" ~ "other/NA",
                              sex == "other" ~ "other/NA",
                              sex == "not applicable" ~ "other/NA",
                              sex == "Not applicable" ~ "other/NA",
                              sex == "LabControl test" ~ "other/NA",
                              sex == "unspecified" ~ "other/NA",
                              sex == "NA" ~ "other/NA",
                              TRUE ~ sex))

gender[is.na(gender)] <- "other/NA"

ggplot(data = gender) +
  geom_bar(mapping = aes(x = sex,
                         y = ..count..,
                         fill = sex),
           width = 0.5,
           size = 4.2,
           stat = "count") +
  scale_fill_manual(values = hurwitz_colors) +
  labs(title = "American Gut Biome WGS Samples by Sex",
       subtitle = "Created by Shelby Nelson @shelbynelson",
       x = "Sex",
       y = "Number of Samples",
       fill = "Sex") +
  theme(legend.position = "none") +
  hurwitz_theme


#-----WORLD GEOGRAPHICAL DENSITY-----------------------------------------------------------------

geo_density <- select(wgs_metadata, longitude, latitude)
geo_density[geo_density == "LabControl test" | geo_density == "Not provided" | geo_density == "not provided" | geo_density == "Unspecified" | geo_density == "unspecified"] <- NA
geo_density <- na.omit(geo_density)
geo_density$longitude <- as.numeric(as.character(geo_density$longitude))
geo_density$latitude <- as.numeric(as.character(geo_density$latitude))
geo_density <- na.omit(geo_density)

#view(geo_density)

world <- map_data("world") %>%
  filter(region != "Antarctica")

ggplot() + 
  geom_polygon(data = world, 
               mapping = aes(x = long, 
                             y = lat, 
                             group = group),
               fill = "#61cddc",
               color = "white") +
  coord_fixed(1.3) +
  geom_point(data = geo_density, 
             mapping = aes(x = longitude, 
                           y = latitude),
             color = "black",
             size = 2) +
  geom_point(data = geo_density, 
             mapping = aes(x = longitude, 
                           y = latitude),
             color = "#f5811f",
             size = 1) +
  labs(title = "American Gut Biome WGS Samples in the World",
       subtitle = "Created by Shelby Nelson @shelbynelson",
       x = "Longitude",
       y = "Latitude") +
  guides(fill = FALSE) +
  hurwitz_theme


#-----US GEOGRAPHICAL DENSITY-----------------------------------------------------------------

us_geo_density <- filter(wgs_metadata, country == "USA", latitude > 25, latitude < 55) %>%
  select(longitude,latitude)

us_geo_density$longitude <- as.numeric(as.character(us_geo_density$longitude))
us_geo_density$latitude <- as.numeric(as.character(us_geo_density$latitude))
us_geo_density <- na.omit(us_geo_density)

#view(us_geo_density)

states <- map_data("state")

ggplot() + 
  geom_polygon(data = states, 
               mapping = aes(x = long, 
                             y = lat, 
                             group = group),
               fill = "#61cddc",
               color = "white") +
  coord_fixed(1.3) +
  geom_point(data = us_geo_density, 
             mapping = aes(x = longitude, 
                           y = latitude),
             color = "black",
             size = 3) +
  geom_point(data = us_geo_density, 
             mapping = aes(x = longitude, 
                           y = latitude),
             color = "#f5811f",
             size = 1.5) +
  labs(title = "American Gut Biome WGS Samples in the Contiguous United States",
       subtitle = "Created by Shelby Nelson @shelbynelson",
       x = "Longitude",
       y = "Latitude") +
  guides(fill = FALSE) +
  hurwitz_theme

#-----AGE VS BMI-----------------------------------------------------------------------------------

age_bmi_df <- select(wgs_metadata,age_years,bmi,age_cat)
age_bmi_df[age_bmi_df == "Not applicable" | age_bmi_df == "Not provided"] <- NA
age_bmi_df <- na.omit(age_bmi_df)
age_bmi_df$age_years <- as.numeric(as.character(age_bmi_df$age_years))
age_bmi_df$bmi <- as.numeric(as.character(age_bmi_df$bmi))
age_bmi_df <- filter(age_bmi_df,bmi < 50 & bmi > 5)

#view(age_bmi_df)

ggplot() + 
  geom_point(data = age_bmi_df, 
             mapping = aes(x = age_years, 
                           y = bmi,
                           color = age_cat),
             size = 3) +
  scale_color_manual(values = hurwitz_colors) +
  geom_smooth(data = age_bmi_df,
              mapping = aes(x = age_years,
                            y = bmi),
              se = FALSE,
              color = "black") +
  labs(title = "American Gut Biome WGS Samples Age vs BMI",
       subtitle = "Created by Shelby Nelson @shelbynelson",
       x = "Age (Years)",
       y = "BMI",
       color = "Age Categories") +
  ylim(10,50) +
  hurwitz_theme

#------------------------------------------------------------------------

sleep_dur <- select(wgs_metadata, sleep_duration)
sleep_dur[sleep_dur == "Not applicable" | sleep_dur == "Not provided"] <- NA
sleep_dur <- na.omit(sleep_dur)

view(sleep_dur)

categories <- c("Less than 5 hours", "5-6 hours", "6-7 hours", "7-8 hours", "8 or more hours")

sum_less5 = (sum(sleep_dur$sleep_duration == "Less than 5 hours"))
sum_5 = (sum(sleep_dur$sleep_duration == "5-6 hours"))
sum_6 = (sum(sleep_dur$sleep_duration == "6-7 hours"))
sum_7 = (sum(sleep_dur$sleep_duration == "7-8 hours"))
sum_8 = (sum(sleep_dur$sleep_duration == "8 or more hours"))

total_sum <- c(sum_less5, sum_5, sum_6, sum_7, sum_8)

treemap(sleep_dur,
        index="categories",
        vSize="total_sum",
        type="index")

treemap