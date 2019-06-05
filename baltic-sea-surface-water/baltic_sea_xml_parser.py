#!/usr/bin/env python3
"""
Author : Shelby Nelson shelbeezy@email.arizona.edu
Date   : 2019-06-05
Purpose: Print nutrient profiles from the Baltic Sea Surface Water Metagenomes with seperated values and units
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
        description='Baltic Sea Surface Water Metagenomes XML Parser',
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
    withUnits = re.compile('^('+ float_pattern + ')(\s)(([\w/-]+)?(\s)?([\w/-]+)?)$')
    longLat = re.compile('((' + float_pattern + ')(\s*([NS]))?)(?:\s*,)?\s+((' + float_pattern + ')(\s*([EW]))?)')
    date = re.compile('^(?P<year>\d{4})-(?P<month>\d{1,2})(?:-(?P<day>\d{1,2}))?')
    shortMonth = re.compile('^(?P<day>\d{1,2})'
                     '[,-]'
                     '(?P<month>'
                     'Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec'
                     ')'
                     '[,-]'
                     '\s*'
                     '(?P<year>\d{4})')
    longMonth = re.compile('^(?P<day>\d{1,2})'
                     '[,-]'
                     '(?P<month>'
                     'January|February|March|April|May|June|July|August|'
                     'September|October|November|December'
                     ')'
                     '[,-]'
                     '\s*'
                     '(?P<year>\d{4})')

    short_months = 'Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec'.split()
    short_mon2num = dict(map(reversed, enumerate(short_months, 1)))

    long_months = ('January February March April May June July August '
                   'September October November December').split()
    long_mon2num = dict(map(reversed, enumerate(long_months, 1)))
   
    # parse the xml file and make a list of dictionaries containing all the metadata
    for elem in root:
        count = 1
        d = {}
        print('NEW SAMPLE______________________________________________________________')
        for sample in elem.findall('SAMPLE'):
            alias = sample.attrib['alias']              #alias = "LMO_12051"
            accession = sample.attrib['accession']      #accession = "SRS954980"    -might bring out since in count 1
            for elements in sample:
                #print(element.tag)                     #element tag like "IDENTIFIERS"
                
                for att in elements:
                    if (count == 1) or (count == 2):
                        colName = att.tag                 #Tag like "Primary_ID"
                        if colName == 'EXTERNAL_ID':
                            colName = 'BIOSAMPLE'
                        d[colName] = att.text                   #Value like "SAMN03351372"
                        #print(colName)
                        #print(value)            
                    if count == 4:
                        #print(att.tag)                    #Tag like "Sample_attribute"
                        for tags in att:
                            if tags.tag == 'TAG':
                                colName = tags.text         #Tag like "day_length (h)"
                            else:
                                d[colName] = tags.text      #Value like: 24.42
                                
                count = count + 1
                
                
                


                               
        #print(d)
        data_list.append(d)
        #break
    df = pd.DataFrame(data_list) 
    df.to_csv('baltic_sea_all.tsv', sep='\t', encoding='utf-8')
    #print(data_list)

# --------------------------------------------------
if __name__ == '__main__':
    main()
