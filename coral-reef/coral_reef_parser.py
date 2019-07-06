#!/usr/bin/env python3
"""
Author : Shelby Nelson shelbeezy@email.arizona.edu
Date   : 2019-06-19
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
import requests

# --------------------------------------------------
'''
def get_args():
    """get command-line arguments"""
    parser = argparse.ArgumentParser(
        description='Argparse Python script',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument(
        'jsonf', metavar='JSONFILE', help='JSON input')

    return parser.parse_args()
'''
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
def get_data(count):
    headers = {'accept':'application/json',}
    params = (('page',count),)
    response = requests.get('https://www.ebi.ac.uk/metagenomics/api/v1/biomes/root:Environmental:Aquatic:Marine:Intertidal%20zone:Coral%20reef/samples', headers=headers, params=params)
    
    json_text = response.text
    file = open('page{}.json'.format(count), "w")
    file.write(json_text)
    file.close()
    data = open('page{}.json'.format(count)).read()
    fixed_file = json.loads(re.sub('[\r\n]', '', data))

    return fixed_file

# --------------------------------------------------
def main():
    '''
    args = get_args()
    in_file = args.jsonf

    if not os.path.isfile(in_file):
        print('input file "{}" is not a file'.format(in_file), file=sys.stderr)
        sys.exit(1)'''
    '''
    #---------------------------This gathers data from web and creates the entire 700 sample dataframe--------
    data_list = []
    page_count = 1
    fixed_file = get_data(page_count)

    while page_count is not None: 
        for section in fixed_file:
            #print(section)                             #links,data,relationships,meta
            if section == "links":
                links_dict = fixed_file[section]
                for links in links_dict:
                    
                    #print(links)
                    #print(links_dict[links])
                    if links == "next":
                        #print(links_dict[links])
                        if links_dict[links] == None:
                            page_count = None
                        else:
                            page_count = page_count + 1
                        #print(page_count)
            if section == "data":
                data_dict = fixed_file[section]
                for all_data in data_dict:
                    d = {}
                    key_count = 0
                    for data_tag in all_data:
                        #print(data_tag)                                #type,id,attributes,relationships,links
                        
                        value = all_data[data_tag]
                        if key_count < 2:
                            d[data_tag] = value
                            #print('{}: '.format(data_tag),end='')           #type or id
                            #print('{}'.format(value))                       #'samples' or 'SRS691150'
                        elif data_tag == 'attributes':
                            for data in value:
                                #print(data)                                #latitude,collection-date, etc
                                #print(value[data])                          #The value like -54.16 and 18-05-06
                                
                                if data == 'sample-metadata':
                                    metadata_dict = value[data]
                                    for attrib in metadata_dict:
                                        
                                        #print(attrib)                      #{key:date, val: 18-05-06, unit: None}
                                        for keys in attrib:
                                            attrib_dict = attrib[keys]
                                            
                                            #print(keys)                    #key,value,unit -NOT always in that order
                                            if keys == 'key':
                                                col_header = attrib_dict
                                                #print(col_header)
                                            elif keys == 'value':
                                                data_val = attrib_dict
                                            else:
                                                unit_val = attrib_dict

                                        unit_header = col_header + '_units'        
                                        d[col_header] = data_val
                                               
                                        if unit_val is not None:
                                            d[unit_header] = unit_val
                                        if ((col_header == 'environment (biome)') or (col_header == 'environment (feature)') or (col_header == 'environment (material)') or (col_header == 'geographic location (country and/or sea,region)') or (col_header == 'geographic location (longitude)') or (col_header == 'geographic location (latitude)')):
                                                del d[col_header]  
                                
                                else:
                                    d[data] = value[data] 
                        key_count = key_count + 1
                    data_list.append(d)                
                    #print(d)    
                    #print('new sample....')             #This loop has all info for one indiv sample
                    #break   
                #print(data_list)      
                #break        
        #break
        
        
        df = pd.DataFrame(data_list) 
        df.to_csv('coral_reef_pg1_output.tsv', sep='\t', encoding='utf-8')          #For a single page
        break
        
        if page_count is not None:                
            fixed_file = get_data(page_count)
        
    
    df = pd.DataFrame(data_list)                                            #These creates the whole 700 lined dataframe
    df.to_csv('coral_reef_all_pgs_output.tsv', sep='\t', encoding='utf-8')   
 
    #---------------------------------------------------------------------------------------
    '''
    #-------------------------This section is for if the entered a search/keyword----------
    count = 0
    all_samp_data = open('datalist.txt').read()
    for sample in all_samp_data:
        
        if count < 6:
            print(sample)
        else:
            break
        count = count + 1
 
# --------------------------------------------------
if __name__ == '__main__':
    main()
