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
    withUnits = re.compile('^('+ float_pattern + ')(\s)(([\w/-]+)?(\s)?([\w/-]+)?)$')
    longLat = re.compile('(' + float_pattern + '(\s*([NS]))?)(?:\s*,)?\s+(' + float_pattern + '(\s*([EW]))?)')
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


    count = 0          #For Debugging
    # parse the xml file and make a list of dictionaries containing all the metadata
    for elem in root:
        #print('NEW ELEMENT.........................................................')   #For Debugging
        d = {}
        for ids in elem.findall('Ids'):
            for sub_ids in ids:
                for key, val in sub_ids.attrib.items():
                    d[val] = sub_ids.text
                    
        
        for att in elem.findall('Attributes'):
            #print(d.keys())
            for sub_att in att:
                attr_name  = sub_att.attrib['attribute_name']               
                d[attr_name] = sub_att.text
                units = ''
                value = ''    
                #print(d.keys()) 
                match1 = date.match(sub_att.text)
                match2 = shortMonth.match(sub_att.text) or longMonth.match(sub_att.text)

                if withUnits.match(sub_att.text):
                    match = withUnits.match(sub_att.text)
                    value = match.group(1)
                    units = match.group(5)
                elif longLat.match(sub_att.text):
                    match = longLat.match(sub_att.text)
                    latitude = match.group(1)
                    longitude = match.group(6)
                    units = 'Lat: {}, Lon: {}'.format(latitude, longitude)
                    
                elif match1:
                    day = match1.group('day') or '01'
                    cleanDate = '{}-{}-{}'.format(match1.group('year'), match1.group('month'), match1.group('day'))
                elif match2:
                    day = match2.group('day')
                    month = match2.group('month')
                    year = match2.group('year')
                    month_num = short_mon2num[
                        month] if month in short_mon2num else long_mon2num[month]
                    cleanDate = '{}-{:02d}-{}'.format(year, month_num, day)
                else:
                    units = ''
                    cleanDate = ''
                        
                if units:
                    d[attr_name + '_Value'] = value
                    d[attr_name + '_units'] = units
                    del d[attr_name]
                if cleanDate:
                    d[attr_name + '_'] = cleanDate
                    del d[attr_name]

                #print(sub_att.text,'\t\t', value, '  ', units)      
        data_list.append(d)
        
        '''                 #For debugging
        count = count + 1
        if count == 5:
            break'''
    #print(data_list)  
        
    df = pd.DataFrame(data_list) 
    df.to_csv('amazon_cont_all.tsv', sep='\t', encoding='utf-8') 

# --------------------------------------------------
if __name__ == '__main__':
    main()
