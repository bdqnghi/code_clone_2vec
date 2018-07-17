import os
import codecs
import numpy as np
from xml_util import parse_tree
from xml_util import get_parent_map
from xml_util import iterate_to_get_node_with_type
from xml_util import get_package_name_of_file
from xml_util import get_class_node_cs
from xml_util import get_parameter_type_of_method

STUPID_URL = "{http://www.srcML.org/srcML/src}"
cs_signatures = list()
try:
	tree = parse_tree("Temp.xml")
	root  = tree.getroot()
	parent_map = get_parent_map(tree)
	
except Exception as e:
	print "Error in this block : " + str(e)

decorations = ["class","interface"]
for decoration in decorations:
	cs_class_nodes = list()
	cs_class_nodes = iterate_to_get_node_with_type(root,decoration,cs_class_nodes)

	biggest_block_cs = None
	class_name = None

	if len(cs_class_nodes) != 0:
		for c in cs_class_nodes[0].getchildren():
			tag = c.tag.replace(STUPID_URL,"")
			if tag == "block":
				biggest_block_cs = c
			if tag == "name":
				if c.text != None:
					class_name = c.text
				else:
					for c2 in c.getchildren():
						tag2 = c2.tag.replace(STUPID_URL,"")
						if tag2 == "name":
							class_name = c2.text


		package_nodes = list()
		package_nodes = iterate_to_get_node_with_type(root,"namespace",package_nodes)
		package_name = ""
		package_name = get_package_name_of_file(root,"cs",package_name)
		functions = list()

		if decoration == "class":
			tag_type = "function"
		if decoration == "interface":
			tag_type = "function_decl"

		functions = iterate_to_get_node_with_type(biggest_block_cs,tag_type,functions)

		for function in functions:
			for elem in function.getchildren():
				child_tag = elem.tag.replace(STUPID_URL,"")
				if child_tag == "name":
					parameters = get_parameter_type_of_method(function)

					parameter_tostr = ""
					if len(parameters) != 0:
						parameters = [x for x in parameters if x != None]
						parameter_tostr = ",".join(parameters)
					if package_name != None and package_name != "" and class_name != None and elem.text != None:	
						full_signature = package_name + "." + class_name + "." + elem.text + "(" + parameter_tostr + ")"
						cs_signatures.append(full_signature)

print cs_signatures