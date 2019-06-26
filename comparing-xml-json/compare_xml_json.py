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
        description='Argparse Python script',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument(
        'files', metavar='FILES', help='Text.tsv file input', nargs='+')

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
    files_ = args.files
    
    biosample_re = re.compile('^bio([\s/-])?sample(s)?$')
    file_count = 1
    for tsv_file in files_:
        samples_d = []
        if not os.path.isfile(tsv_file):
            die('input file "{}" is not a file'.format(tsv_file))
        else:
            #print(tsv_file)             #file name 
            with open(tsv_file) as f:
                reader = csv.DictReader(f, dialect='excel-tab')
                d_list = []
                for line in reader:
                    d_list.append(line)
                #print(d_list)
                for sample in d_list:
                    #print(sample)                      #All of indiv sample data
                    for col_header in sample:
                        #print(col_header)              #column header
                        #print(sample[col_header])      #column value
                        
                        if biosample_re.match(col_header.lower()):
                            #print(col_header)           #prints biosample in the file's form
                            #print(sample[col_header])    #sample name
                            samples_d.append(sample[col_header])
        if file_count == 1:
            first_samples_d = samples_d

        file_count = file_count + 1
        
        #break
    first_file_d = set(first_samples_d)
    sec_file_d = set(samples_d)

    in_both = first_file_d.intersection(sec_file_d)
    all_samples = first_file_d.union(sec_file_d)
    not_in_both = all_samples - in_both
    

    print(in_both)
    print(len(in_both))
    print('\n')
    print(all_samples)
    print(len(all_samples))
    print('\n')
    print(not_in_both)
    print(len(not_in_both))

# --------------------------------------------------
if __name__ == '__main__':
    main()