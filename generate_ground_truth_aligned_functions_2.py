import os
import codecs
import numpy as np
from xml_util import parse_tree
from xml_util import get_parent_map
from xml_util import iterate_recursive
# from xml_util import get_package_name_of_node
from util import process_srcml_source_code
from xml_util import transform_source_code
from xml_util import get_necessary_information_to_process_source_code
from xml_util import iterate_function_node_to_get_text
from xml_util import iterate_to_get_node_with_type
from xml_util import find_biggest_block
from xml_util import get_information_of_decl_stmts
from util import remove_empty_intext

CURRENT_DIR = os.getcwd()
STUPID_URL = "{http://www.srcML.org/srcML/src}"
# projects = ["antlr","cordova","datastax","factual","fpml","log4j","spring","lucene","uap","zeromq","aws","mongodb"]

# projects = ["antlr","cordova","datastax","factual","fpml","log4j","spring","lucene","uap","zeromq","itext","jgit","poi","jts","db4o","mongodb","aws"]
projects = ["antlr","cordova","datastax","factual","fpml","log4j","spring","lucene","uap","zeromq","itext","jgit","poi","jts","db4o"]
def get_class_node_cs(root):
	class_node = None
	for elem in root.getchildren():
		tag = elem.tag.replace(STUPID_URL,"")
		if tag == "namespace":
			for elem2 in elem.getchildren():
				tag2 = elem2.tag.replace(STUPID_URL,"")
				if tag2 == "block":
					for elem3 in elem2.getchildren():
						tag3 = elem3.tag.replace(STUPID_URL,"")
						if tag3 == "class":
							class_node = elem3
	return class_node


def get_class_node_java(root):
	class_node = None
	for elem in root.getchildren():
		tag = elem.tag.replace(STUPID_URL,"")
		if tag == "class":
			class_node = elem
	return class_node


for project in projects:
	cs_paths = list()
	java_paths = list()
	for r,ds,files in os.walk(os.path.join(CURRENT_DIR,"SRCML_DATA",project)):
		for file in files:
			file_path = os.path.join(r,file)
			split = file_path.split("/")
			if split[7] == "cs":
				cs_paths.append(file_path)
			if split[7] == "java":
				java_paths.append(file_path)


	for cs_path in cs_paths:
		
		for java_path in java_paths:

			cs_splits = cs_path.split("/")
			java_splits = java_path.split("/")
			cs_file = cs_splits[8]
			java_file = java_splits[8]
			if len(cs_file.split(".")) == 2 and len(java_file.split(".")) == 2:
				if cs_file.split(".")[0] == java_file.split(".")[0]:
					print cs_path
					print java_path
					try: 
						cs_parent_map, cs_global_vars_mapping, cs_package_object_mapping, cs_object_method_mapping, cs_third_party_package_object_mapping_list, cs_third_party_object_method_mapping_list = get_necessary_information_to_process_source_code(cs_path, "cs", project)

						java_parent_map, java_global_vars_mapping, java_package_object_mapping, java_object_method_mapping, java_third_party_package_object_mapping_list, java_third_party_object_method_mapping_list = get_necessary_information_to_process_source_code(java_path, "java", project)
					
						cs_tree = parse_tree(cs_path)
						cs_parent_map = get_parent_map(cs_tree)
						cs_tree_str = ""
						cs_root  = cs_tree.getroot()

						java_tree = parse_tree(java_path)
						java_parent_map = get_parent_map(java_tree)
						java_tree_str = ""
						java_root  = java_tree.getroot()

						cs_class_node = get_class_node_cs(cs_root)
						java_class_node = get_class_node_java(java_root)
						
						biggest_block_cs = None
						biggest_block_java = None

						for c in cs_class_node.getchildren():
							tag = c.tag.replace(STUPID_URL,"")
							if tag == "block":
								biggest_block_cs = c
						for j in java_class_node.getchildren():
							tag = j.tag.replace(STUPID_URL,"")
							if tag == "block":
								biggest_block_java = j

						for block_cs_node in biggest_block_cs.getchildren():
							tag = block_cs_node.tag.replace(STUPID_URL,"")
							if tag == "function":
								for node in block_cs_node:
									cs_tree_str = ""
									tag1 = node.tag.replace(STUPID_URL,"")
									if tag1 == "name":
										cs_function_name_origin = node.text
										cs_function_name = node.text.lower()
									
										for block_java_node in biggest_block_java.getchildren():
											tag2 = block_java_node.tag.replace(STUPID_URL,"")
											if tag2 == "function":
												for node2 in block_java_node:
													java_tree_str = ""
													tag3 = node2.tag.replace(STUPID_URL,"")
													if tag3 == "name":
														java_function_name_origin = node2.text
														java_function_name = node2.text.lower()
														
														if cs_function_name == java_function_name:

															processed_cs_code = ""
															processed_java_code = ""


															cs_function_block = find_biggest_block(block_cs_node)
															cs_decl_stmt_locals = list()
															cs_decl_stmt_locals = iterate_to_get_node_with_type(cs_function_block,"decl_stmt",cs_decl_stmt_locals)	
															cs_local_vars_mapping = get_information_of_decl_stmts(cs_decl_stmt_locals)
															processed_cs_code = iterate_function_node_to_get_text("cs",block_cs_node,processed_cs_code,cs_parent_map,cs_local_vars_mapping,cs_global_vars_mapping,cs_object_method_mapping,cs_package_object_mapping,cs_third_party_object_method_mapping_list,cs_third_party_package_object_mapping_list)
															processed_cs_code = processed_cs_code.replace("@","")
															processed_cs_code = remove_empty_intext(processed_cs_code)
															
															java_function_block = find_biggest_block(block_java_node)
															java_decl_stmt_locals = list()
															java_decl_stmt_locals = iterate_to_get_node_with_type(java_function_block,"decl_stmt",java_decl_stmt_locals)					
															java_local_vars_mapping = get_information_of_decl_stmts(java_decl_stmt_locals)
															processed_java_code = iterate_function_node_to_get_text("java",block_java_node,processed_java_code,java_parent_map,java_local_vars_mapping,java_global_vars_mapping,java_object_method_mapping,java_package_object_mapping,java_third_party_object_method_mapping_list,java_third_party_package_object_mapping_list)
															processed_java_code = processed_java_code.replace("@","")
															processed_java_code = remove_empty_intext(processed_java_code)

															divide_1 = float(len(processed_cs_code))/float(len(processed_java_code))
															divide_2 = float(len(processed_java_code))/float(len(processed_cs_code))

															
															if (divide_1 > 0.6 and divide_1 < 1) or (divide_2 > 0.6 and divide_2 < 1):
																print "Because cs/java = " + str(divide_1) + " and java/cs = " + str(divide_2)
																# line = project + "," + cs_file.split(".")[0] + "," + package_name_cs + "," + processed_cs_code + "," + package_name_java + "," + processed_java_code
																# with open("./evaluation_data/functions/functions_" + project + "_new" + ".csv","a") as out:
																# 	out.write(line + "\n")

																with open("./sentences/sentences_function_cs_1906.csv","a") as out:
																	out.write(processed_cs_code + "\n")
																with open("./sentences/sentences_function_java_1906.csv","a") as out:
																	out.write(processed_java_code + "\n")
					except Exception as e:
						print e

