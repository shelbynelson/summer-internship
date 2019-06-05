#!/usr/bin/env python3
"""
Author : Shelby Nelson shelbeezy@email.arizona.edu
Date   : 2019-06-05
Purpose: Print nutrient profiles from the Arctic Ocean Metagenomes with seperated values and units
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
    #float_pattern = '[+-]?\d+(\.\d+)?([eE]\d+)?'
    #longLat = re.compile('((' + float_pattern + ')(\s*([NS]))?)(?:\s*,)?\s+((' + float_pattern + ')(\s*([EW]))?)')
    dateTime = re.compile('^((?P<year>\d{4})-(?P<month>\d{1,2})(?:-(?P<day>\d{1,2}))?)T((?P<hour>\d{1,2}):(?P<minute>\d{1,2}):(?P<seconds>\d{1,2})?)Z')
    shortMonth = re.compile('^(?P<day>\d{1,2})'
                            '[,-]'
                            '(?P<month>'
                            'Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec'
                            ')'
                            '[,-]'
                            '\s*'
                            '(?P<year>\d{4})')    

    short_months = 'Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec'.split()
    short_mon2num = dict(map(reversed, enumerate(short_months, 1)))

    # parse the xml file and make a list of dictionaries containing all the metadata
    for elem in root:
        count = 1
        d = {}
        for sample in elem.findall('SAMPLE'):
            colName = 'Sample_Alias'
            d[colName] = sample.attrib['alias']              #alias = "LMO_12051"   
            for elements in sample:               
                for att in elements:
                                                
                    if count == 4:
                        for tags in att:
                            if tags.tag == 'TAG':
                                colName = tags.text.lower()         #Tag like "day_length (h)"

                            else:
                                d[colName] = tags.text      #Value like: 24.42
                                if 'latitude' in colName:
                                    d['latitude'] = tags.text
                                    del d[colName]
                                if 'longitude' in colName:
                                    d['longitude'] = tags.text
                                    del d[colName]
                                if (colName == 'project name') or (colName == 'sample name'):
                                    del d[colName]
                                if dateTime.match(tags.text):
                                    match = dateTime.match(d[colName])
                                    d['event date'] = match.group(1)
                                    d['event time'] = match.group(5)
                                    del d[colName]
                                if shortMonth.match(tags.text):
                                    match = shortMonth.match(tags.text)
                                    month = short_mon2num[match.group(2)]
                                    d[colName + ' date'] = '{}-{:02d}-{}'.format(match.group(3), month, match.group(1))
                                    del d[colName]
                            
                                
                count = count + 1
        print(d)
        data_list.append(d)
        #break
'''
    df = pd.DataFrame(data_list) 
    df.to_csv('arctic_ocean_all_testtime.tsv', sep='\t', encoding='utf-8')
'''
# --------------------------------------------------
if __name__ == '__main__':
    main()
