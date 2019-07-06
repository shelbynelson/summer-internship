#!/usr/bin/env python3
"""
Author : Shelby Nelson shelbeezy@email.arizona.edu
Date   : 2019-06-18
Purpose: Parse data from a JSON file to get the general columns, values, and units. This program DOES NOT catch duplicate columns like "collection date" vs "collection-date"
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
    mu = '\u03BC'

    data = open(in_file).read()
    fixed_file = json.loads(re.sub('[\r\n]', '', data))

    for section in fixed_file:                          #Overall sections like data, links, and meta
        if section == 'data':                           #data section including all samples
            data_dict = fixed_file[section]
            for data in data_dict:
                d = {}
                for key in data:
                    value = data[key]
                    if ((key == 'type') or (key == 'id')):      #type and ID section for individual sample
                        d[key] = value  
                    elif key == 'attributes':                   #attributes section for individual sample
                        for key2 in value:
                            if key2 == 'sample-metadata':       #sample metadata for individual sample
                                metadata_dict = value[key2]
                                for attrib in metadata_dict:
                                    for keys in attrib:                 #Pasted here

                                        attrib_dict = attrib[keys]
                                        
                                        if keys == 'key':               #This saves keys from metadata like "latitude"
                                            col_header = attrib_dict
                                        elif keys == 'value':           #This saves value from metadata like "406.5"
                                            data_val = attrib_dict
                                        else:                           #This saves units from metadata like "pmol"
                                            if (attrib_dict is not None) and ('&micro;' in attrib_dict):
                                                attrib_dict = attrib_dict.replace('&micro;', mu)
                                            if (attrib_dict is not None) and ('&deg;' in attrib_dict):
                                                attrib_dict = attrib_dict.replace('&deg;', '')
                                            unit_val = attrib_dict

                                    unit_header = col_header + '_units'        
                                    d[col_header] = data_val
                                            
                                    if unit_val is not None:
                                        d[unit_header] = unit_val                                                                     
                            else:                                       #This is for the key,value pairs that are in the attributes section and not in metadata
                                d[key2] = value[key2]
                        #'''                              
                    elif key == 'links':                                #This is the links that is in an individual sample
                        for key2 in value:
                            d['samples '+key+' '+key2] = value[key2]  
                    elif key == 'relationships':                        #This is for the data in the relationships section for a sample
                        for key2 in value:
                            value2 = value[key2]
                            for key3 in value2:
                                value3 = value2[key3]    
                                for key4 in value3:
                                    if (key3 == 'data') and (key2 == 'studies'):        #gets data from studies
                                        for pair in key4:
                                            if pair == 'links':                         #gets the link from relationships>studies>data>links>self>"the link"
                                                deeper = key4[pair]
                                                for keylink in deeper:
                                                    d[key +' '+pair+' '+key2+' '+keylink] = deeper[keylink]
                                            else:
                                                d[pair+' '+key2] = key4[pair]            
                                    elif key3 == 'links':                               #Relationship links for biome, runs, and studies
                                        d[key +' '+key3+' '+key2] = value3[key4]       
                                    elif (key3 == 'data') and (key2 == 'biome'):        #biome's data
                                        d[key4+' '+key2]= value3[key4]                            
                data_list.append(d)
                #break                                                  #For debugging one sample
    
    df = pd.DataFrame(data_list) 
    df.to_csv('raw_parsed_output.tsv', sep='\t', encoding='utf-8')
    

# --------------------------------------------------
if __name__ == '__main__':
    main()
