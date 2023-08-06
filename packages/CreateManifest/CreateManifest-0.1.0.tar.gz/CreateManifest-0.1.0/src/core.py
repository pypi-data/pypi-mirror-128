import os
import re
from helpers import xml_helpers

dirname =  os.path.dirname(__file__)
datafilename = os.path.join(dirname, '../data/mozart_ids.txt')
outfiledir = os.path.join(dirname, '../data/')

with open(datafilename, mode='r') as infile:
    for line in infile:
        groupname = re.search('\[(\w+)\]', line)
        if(groupname):
            outfilename = outfiledir + groupname[1] + '_' + 'manifest.xml'
            xml_helpers.generate_xml_template(outfilename, line)
        xml_helpers.add_test_to_xml(outfilename, line)
