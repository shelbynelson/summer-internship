
#Shelby Nelson
#7/9/2019

path <- "C:/Users/Shelbeezy/work/summer-internship/R-practice/raw_parsed_output_baltic.tsv"

baltic <- read.table(path,header = TRUE,sep = "\t",stringsAsFactors = FALSE)

plot(baltic$X,baltic$temperature)


