#!/usr/bin/env python3
"""
Author : Shelby Nelson shelbeezy@email.arizona.edu
Date   : 2019-06-18
Purpose: Parse data from a JSON Amazon Continuum Metagenomes file with seperated values and units
"""
import json
import csv
import argparse
import sys
import os
import xml.etree.ElementTree as ET
import pandas as pd
import re

# --------------------------------------------------
def get_args():
    """get command-line arguments"""
    parser = argparse.ArgumentParser(
        description='Argparse Python script',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument(
        'jsonf', metavar='JSONFILE', help='JSON input')

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
    in_file = args.jsonf

    if not os.path.isfile(in_file):
        print('input file "{}" is not a file'.format(in_file), file=sys.stderr)
        sys.exit(1)

    data_list = []
    count = 0
    mu = '\u03BC'
    

    data = open(in_file).read()
    fixed_file = json.loads(re.sub('[\r\n]', '', data))

    for section in fixed_file:
        if count == 1:
            data_dict = fixed_file[section]

            for data in data_dict:
                d = {}
                key_count = 0

                for key in data:
                    value = data[key]
                    if key_count < 2:
                        d[key] = value
                        #print('{}: '.format(key),end='')                    #key like "type or id"
                        #print('{}\n'.format(value))                 #value like "samples or SRS5657..."
                    elif key == 'attributes':
                        for key2 in value:
                            if key2 == 'sample-metadata':
                                metadata_dict = value[key2]
                                for attrib in metadata_dict:
                                    for keys in attrib:
                                        attrib_dict = attrib[keys]
                                        if keys == 'key':
                                            col_header = attrib_dict
                                            if col_header == 'bacterialcarbon production':
                                                col_header = 'bacterial carbon production'
                                            elif col_header == 'samplingcruise':
                                                col_header = 'sampling cruise'

                                        elif keys == 'unit':
                                            unit_header = col_header + '_units'
                                            if (attrib_dict is not None) and ('&micro;' in attrib_dict):
                                                attrib_dict = attrib_dict.replace('&micro;', mu)
                                            if (attrib_dict is not None) and ('&deg;' in attrib_dict):
                                                attrib_dict = attrib_dict.replace('&deg;', '')
                                            unit_val = attrib_dict

                                        else:
                                            data_val = attrib_dict
                                            d[col_header] = data_val
                                            d[unit_header] = unit_val
                                            if unit_val is None:
                                                del d[unit_header]
                                            if col_header == 'collection date':
                                                del d[col_header]       
                            
                            else:
                                d[key2] = value[key2]                        
                    '''
                    elif key == 'links':
                        for key2 in value:
                            print('{}: '.format(key2),end='')            #self      #I think this isnt needed, but unsure
                            print('{}'.format(value[key2]))             #The link
                    '''
                    key_count = key_count + 1
                data_list.append(d)
                #break                                                  #For debugging
        count = count + 1

    df = pd.DataFrame(data_list) 
    df.to_csv('amazon_data_output.tsv', sep='\t', encoding='utf-8') 

# --------------------------------------------------
if __name__ == '__main__':
    main()
