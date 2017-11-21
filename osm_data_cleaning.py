#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
import tkinter.filedialog


#FILENAME = tkinter.filedialog.askopenfilename()
FILENAME = "saint-petersburg_russia.osm/saint-petersburg_russia.osm"

def count_tags(filename):
        """ (file)-> dict
	process map file and return a dict with first-level tag name as key 
	and number of times this tag can be encountered in map as value.	
	"""
        tags = {}
        tag = ""
        for event, elem in ET.iterparse(filename, events = ("start", )):
                if elem.tag in tags:
                        tags[elem.tag]+=1
                        elem.clear()
                else:
                        tags[elem.tag] = 1
                        elem.clear()
        return tags

tags = count_tags(FILENAME)
print(tags)	
