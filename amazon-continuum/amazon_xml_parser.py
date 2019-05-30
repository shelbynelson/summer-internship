#!/usr/bin/env python3
"""
Author : Shelby Nelson shelbeezy@email.arizona.edu
Date   : 2019-05-28
Purpose: Print nutrient profiles from the Amazon Continuum Metagenomes
"""

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
        'xml', metavar='XML', help='XML input')


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
    in_file = args.xml

    if not os.path.isfile(in_file):
        print('input file "{}" is not a file'.format(in_file), file=sys.stderr)
        sys.exit(1)

    tree = ET.parse(in_file)
    root = tree.getroot()
    data_list = []

    #RegExs
    float_pattern = '[+-]?\d+(\.\d+)?([eE]\d+)?'
    withUnits = re.compile('^'+ float_pattern + '(\s)(([\w/-]+)?(\s)?([\w/-]+)?)$')
    longLat = re.compile('(' + float_pattern + '(\s*([NS]))?)(?:\s*,)?\s+(' + float_pattern + '(\s*([EW]))?)')

    #count = 0          #For Debugging
    # parse the xml file and make a list of dictionaries containing all the metadata
    for elem in root:
        print('NEW ELEMENT.........................................................')   #For Debugging
        d = {}
        for ids in elem.findall('Ids'):
            for sub_ids in ids:
                for key, val in sub_ids.attrib.items():
                    d[val] = sub_ids.text

        for att in elem.findall('Attributes'):
            for sub_att in att:               
                d[sub_att.attrib['attribute_name']] = sub_att.text

                if withUnits.match(sub_att.text):
                    match = withUnits.match(sub_att.text)
                    units = match.group(4)
                elif longLat.match(sub_att.text):
                    match = longLat.match(sub_att.text)
                    latitude = match.group(1)
                    longitude = match.group(6)
                    units = latitude,longitude
                else:
                    units = ''
                
                print(d[sub_att.attrib['attribute_name']],'\t\t', units)   #For debugging
                      
        data_list.append(d)
        
        '''                   #For debugging
        count = count + 1
        if count == 28:
            break
        '''
        
    #  df = pd.DataFrame(data_list) 
    #  df.to_csv('amazon_cont_all.tsv', sep='\t', encoding='utf-8') 

# --------------------------------------------------
if __name__ == '__main__':
    main()
