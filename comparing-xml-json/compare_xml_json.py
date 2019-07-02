#!/usr/bin/env python3
"""
Author : Shelby Nelson shelbeezy@email.arizona.edu
Date   : 2019-06-26
Purpose: Compare two files to check the differences in the biosamples within the files. 
It will print the number of samples that are missing in each one and list which samples are not in each one.
"""

import argparse
import csv
import sys
import os
import re

# --------------------------------------------------
def get_args():
    """get command-line arguments"""
    parser = argparse.ArgumentParser(
        description='Comparing the output of two .tsv files Python script',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument(
        'file', metavar='FILE', help='Text.TSV file input', nargs=2)

    return parser.parse_args()

# --------------------------------------------------
def warn(msg):
    """Print a message to STDERR"""
    print(msg, file=sys.stderr)

# --------------------------------------------------
def die(msg='Something bad happened'):
    """warn() and exit with error"""
    warn(msg)
    sys.exit(1)

# --------------------------------------------------
def main():
    args = get_args()
    files_ = args.file
    
    #---------------------------This section reads the files and gets the biosample names--------------------------------------------------
    biosample_re = re.compile('^bio([\s/-])?sample(s)?$')
    file_count = 1
    
    for tsv_file in files_:
        samples_d = []
        if not os.path.isfile(tsv_file):
            die('input file "{}" is not a file'.format(tsv_file))
        elif (('.tsv' not in tsv_file) and ('.csv' not in tsv_file)):
            die('input file "{}" is not a .tsv or .csv file'.format(tsv_file))
        else:
            with open(tsv_file) as f:    
                reader = csv.DictReader(f, dialect='excel-tab')
                d_list = []
                for line in reader:
                    d_list.append(line)  
                for sample in d_list:                  
                    for col_header in sample:
                        if biosample_re.match(col_header.lower()):
                            samples_d.append(sample[col_header])

        if file_count == 1:
            first_samples_d = samples_d
            first_file_name = tsv_file
        elif file_count == 2:
            sec_file_name = tsv_file
        file_count += 1
    
    #--------------This section compares the two lists-------------------------------------------------------------------------
    first_file_d = set(first_samples_d)
    sec_file_d = set(samples_d)

    in_both = first_file_d.intersection(sec_file_d)
    all_samples = first_file_d.union(sec_file_d)
    not_in_both = all_samples - in_both
    
    #print(first_file_d)                #Prints all of the samples in the first file
    f1_count = len(first_file_d)        #The count of samples in the first file
    #print(sec_file_d)                  #Prints all of the samples in the second file
    f2_count = len(sec_file_d)          #The count of samples in the second file
    #print(in_both)                     #Prints all of the samples that are intersecting/in both of the files
    #print(len(in_both))                #Prints the number of samples that are the same in both files
    #print(all_samples)                 #Prints the union or all of the samples in
    #print(len(all_samples))            #Prints the total number of samples in both files
    #print(not_in_both)                 #Prints the samples that are not the same in both files
    #print(len(not_in_both))            #Printd the number of samples that are not the same in both files

    nf1_counter = 0                     #counts the number of samples that are not in the first file
    nf2_counter = 0                     #counts the number of samples that are not in the second file
    in_1_not_2 = []
    in_2_not_1 = []
    for samp in not_in_both:            #Compares samples in "not_in_both" to samples in the first and second files
        for biosample in first_file_d:
            if biosample == samp:
                in_1_not_2.append(samp)   #Appends the samples to a list that are in the first file and are not in the second file
                nf1_counter+=1
        for biosample in sec_file_d:
            if biosample == samp:
                in_2_not_1.append(samp)     #Appends the samples to a list that are in the second file and are not in the first file
                nf2_counter+=1

    #-----------This section writes the outcome of the program to comparizon_output.txt-----------------------------------------------------------------------------
    outfile = open('comparison_output.txt', 'w')

    #print('\nThere are {} samples in {}\n\nThere are {} samples in {}\n'.format(f1_count,first_file_name,f2_count, sec_file_name))
    outfile.write('There are {} samples in {}\n\nThere are {} samples in {}\n\n'.format(f1_count,first_file_name,f2_count, sec_file_name))

    #print('There are {} samples in {} file that are not found in {} file: '.format(nf1_counter, first_file_name, sec_file_name))
    outfile.write('There are {} samples in {} file that are not found in {} file: '.format(nf1_counter, first_file_name, sec_file_name))
    if in_1_not_2:
        #print(in_1_not_2)
        outfile.write(str(in_1_not_2))

    #print('\nThere are {} samples in {} file that are not found in {} file:'.format(nf2_counter,sec_file_name, first_file_name))
    outfile.write('\n\nThere are {} samples in {} file that are not found in {} file:'.format(nf2_counter,sec_file_name, first_file_name))
    if in_2_not_1:
        #print(in_2_not_1)
        outfile.write(str(in_2_not_1))
    print('The output has been written to "comparison_output.txt"')
        
# ------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()