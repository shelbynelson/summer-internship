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

    data_list = []
    count = 0
    data = open(in_file).read()
    #print(json.loads(re.sub('[\r\n]', '', data)))                       For debugging
    fixed_file = json.loads(re.sub('[\r\n]', '', data))
    for section in fixed_file:
        if count == 1:
            data_dict = fixed_file[section]
            for data in data_dict:
                d = {}
                #print('{}\n\n'.format(data))
                key_count = 0
                for key in data:
                    value = data[key]
                    #print('{}:'.format(key))                    #key like "type or attributes"
                    #print('{}\n'.format(value))                 #value like "samples or SRS5657..."
                    
                    if key_count < 2:
                        d[key] = value
                        #print('{}: '.format(key),end='')                    #key like "type or id"
                        #print('{}\n'.format(value))                 #value like "samples or SRS5657..."
                        
                    elif key == 'attributes':
                        for key2 in value:
                            if key2 == 'sample-metadata':
                                metadata_dict = value[key2]
                                #print('{}: '.format(key2),end='')            #key
                                for attrib in metadata_dict:
                                    #print('{}'.format(attrib))             #for debugging total value with key val and unit
                                    for keys in attrib:
                                        attrib_dict = attrib[keys]
                                        #print('{}: '.format(keys),end='')                    #key like "key unit or value" these will be column headers
                                        #print('{}'.format(attrib_dict))                   #value like "microseconds or 19.78" needs to go under column header
                                        if keys == 'key':
                                            col_header = attrib_dict
                                        elif keys == 'unit':
                                            unit_header = col_header + '_units'
                                            unit_val = attrib_dict
                                        else:
                                            data_val = attrib_dict
                                            #print('{}: {}, {}: {}'.format(col_header,data_val,unit_header,unit_val))
                                            d[col_header] = data_val
                                            d[unit_header] = unit_val
                                #print(d)        
                                    
                                    #print('\n')
                            else:
                                d[key2] = value[key2]
                                #print('{}: '.format(key2),end='')            #key
                                #print('{}'.format(value[key2]))             #value
                        #print(d)
                        #print('\n')
                    '''
                    elif key == 'links':
                        for key2 in value:
                            print('{}: '.format(key2),end='')            #self      I think this isnt needed
                            print('{}'.format(value[key2]))   #The link
                    '''
                    key_count = key_count + 1
                #print('NEW------------')                            #for debugging
                data_list.append(d)
                #break
        
        
        count = count + 1
        #data_list.append(d)
        #print(data_list)
    df = pd.DataFrame(data_list) 
    df.to_csv('amazon_data_output.tsv', sep='\t', encoding='utf-8') 

    '''
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
    long_mon2num = dict(map(reversed, enumerate(long_months, 1)))'''
    '''
    # parse the xml file and make a list of dictionaries containing all the metadata
    for elem in root:
        d = {}
        for ids in elem.findall('Ids'):
            for sub_ids in ids:
                for key, val in sub_ids.attrib.items():
                    d[val] = sub_ids.text
                    
        for att in elem.findall('Attributes'):
            for sub_att in att:
                units = ''
                value = '' 
                attr_name  = sub_att.attrib['attribute_name']               
                d[attr_name] = sub_att.text
                print(d)
                
                match1 = date.match(sub_att.text)
                match2 = shortMonth.match(sub_att.text) or longMonth.match(sub_att.text)

                if withUnits.match(sub_att.text):
                    match = withUnits.match(sub_att.text)
                    value = match.group(1)
                    units = match.group(5)
                elif longLat.match(sub_att.text):
                    match = longLat.match(sub_att.text)

                    latitude = match.group(2)
                    laTotal = match.group(1)
                    if 'S' in laTotal:
                        latitude = '-' + latitude

                    longitude = match.group(8)
                    loTotal = match.group(7)
                    if 'W' in loTotal:
                        longitude = '-' + longitude

                    d['latitude'] = latitude
                    d['longitude'] = longitude
                    del d[attr_name]
                
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

                #Assigning/deleting columns        
                if units:
                    d[attr_name + '_Value'] = value
                    d[attr_name + '_units'] = units
                    del d[attr_name]
                if cleanDate:
                    d[attr_name + '_'] = cleanDate
                    del d[attr_name]
                if (attr_name == 'collection_time') and (':' not in d[attr_name]):
                    d[attr_name] = d[attr_name][:2] + ':' + d[attr_name][2:]'''
 


# --------------------------------------------------
if __name__ == '__main__':
    main()
