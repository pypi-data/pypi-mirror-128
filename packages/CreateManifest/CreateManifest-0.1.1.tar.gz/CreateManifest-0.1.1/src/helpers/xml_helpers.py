import xml.etree.ElementTree as et
import re

run_once = 0
def generate_xml_template(outfilename, mozart_id, validation_level = "minimum"):

    root = et.Element("manifest")

    configs = et.Element("configs")
    root.append(configs)

    var = et.SubElement(configs,"var", {"section":"vizzini", "key":"validation_level"})
    var.text = validation_level
    
    tests = et.Element("tests")
    root.append (tests)
    
    tree = et.ElementTree(root)
    et.indent(tree, space='\t', level=0)


    with open(outfilename, mode = 'wb') as out:
        tree.write(out)


def add_test_to_xml(outfilename, line):

    if(not re.search('\[\w+\]',line)):
        tree = et.parse(outfilename)
        tests = tree.find("tests") 
        test = et.SubElement(tests,"test")
        test.text = line.strip()
        et.indent(tree, space='\t', level=0)
        tree.write(outfilename)