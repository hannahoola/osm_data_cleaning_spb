# osm_data_cleaning_spb
The goal of the project was to do a little clean-up of a certain area of OpenStreetMap data. I have chosen Saint-Petersburg, Russia - 
a city, where a lived for 5 years, and which I know relatively well. I have decided to examine street names and fix them so that 
they are coherent within the entire datase. For example, if there were streets called "Vanilla Str." and "Lemon Street", I would have 
wanted to end up with either "Vanilla Str." and "Lemon Str." or "Vanilla Street" and "Lemon Street" depending on which way of naming 
a street type is prevalent in the dataset.

## Getting started
### Prerequisites
The version of Python used for the project is 3.6.3.
### Dataset
I downloaded a metro extract from [Mapzen](https://mapzen.com/data/metro-extracts/metro/saint-petersburg_russia/) in a form of an OSM XML data file
and started working with it.

The first script osm_data_audit.py .It takes an OSM file of your choice and loops through all the tags named "tag", which are nested
within "node" or "way" tags and which contain an attribute k="addr:street". Since the OSM file is quite large (~1Gb) and would require a lot of 
memory if parsed using DOM methods, for parsing an XML tree I used ElementTree **iterpase** method:
```
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
```
