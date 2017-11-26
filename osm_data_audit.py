#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
from collections import defaultdict
import tkinter.filedialog
import codecs


FILENAME = tkinter.filedialog.askopenfilename()
"""
- audit the OSMFILE and create the variables 'mapping' and 'expected' to reflect
    the changes needed to fix the unexpected street types to the appropriate
    ones in the expected list.

"""

street_type_re = re.compile(r'^[^А-Я\s]+\b|\b[^А-Я\s]+\.?$')
  

def count_street_type(street_types, street_name):
        m = street_type_re.search(street_name)
        if m:
                street_type = m.group()
                street_types[street_type] += 1
                

def is_street_name(elem):
        return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
        osm_file = codecs.open(osmfile, "r", encoding='utf8')
        street_types = defaultdict(int)
        for event, elem in ET.iterparse(osm_file, events=("start",)):
                if elem.tag == "node" or elem.tag == "way":
                        for tag in elem.iter("tag"):
                                if is_street_name(tag):
                                        count_street_type(street_types, tag.attrib['v'])
                        elem.clear()                
        osm_file.close()
        return street_types

street_types = audit(FILENAME)
pprint.pprint(street_types)
input()
