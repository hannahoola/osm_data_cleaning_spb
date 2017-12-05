#!/usr/bin/env python
# -*- coding: utf-8 -*-
#import xml.etree.ElementTree as ET
import re
import codecs
import tkinter.filedialog

FILENAME = tkinter.filedialog.askopenfilename()
OUTPUT = "streamed.osm"


"""
- fix the street names
"""

expected = ["улица", "шоссе", "проспект", "проезд", "переулок", "аллея", "бульвар", "вал",
			"линия", "набережная", "площадь", "садоводство", "проток", "дорога", "коса",
			"крепость", "поле"]

mapping = { "улица": ["ULITSA", "ул.", "ул", "улицаы", "Улица"],
			"улица С": ["ул.С"],
			"проспект": ["пр.", "пр"],
			"переулок": ["пер."],
			"аллея": ["ал."],
			"площадь": ["пл"],
			"набережная": ["наб"],
			"-я линия": ["-линия"],
			"1-я линия": ["1линия"],
			"садоводство": ["сдт"],
			"линия": ["Линия"]
			}

street_re = re.compile(r'k="addr:street"')
name_re = re.compile(r'(v=")(.*)("[ ]?)')

			
def update_name(name, mapping):
    done = False
    for item in mapping:
        bad_street = ""
        for street in mapping[item]:
            if street in name and len(street)>len(bad_street):
                bad_street = street
        if bad_street != "" and not done:
            name = name.replace(bad_street, item)
            done = True
    return name

def is_good_street(name, expected):
    good = False
    for word in name:
        if any(item == word for item in expected):
            good = True
    return good

def is_street_name(line):
    return (street_re.search(line))

def get_street_name(line):
    return (name_re.search(line).group(2))

def update_osm(osmfile, output):
    osm_file = codecs.open(osmfile, "r", encoding='utf8')
    with codecs.open(output, "w", encoding='utf8') as output:
        for line in osm_file:
            if "<tag" in line and is_street_name(line):
                    name = get_street_name(line)
                    name_list = name.split(' ')
                    if is_good_street(name_list, expected):
                        pass
                    else:
                        name = update_name(name, mapping)
                        line = name_re.sub(r'\g<1>'+name+r'\g<3>', line)
                    output.write(line)
            else:
                output.write(line)
    osm_file.close()
    return True
	
update_osm(FILENAME, OUTPUT)	
