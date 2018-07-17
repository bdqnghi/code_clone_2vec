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
from xml_util import get_all_decl_stmt_from_block_global
from xml_util import extract_all_import
from xml_util import get_candidate_sdk_packages_from_import_list
from util import remove_empty_intext
from util import keep_only_java_sdk_method_api
from xml_util import get_necessary_library_information
from util import keep_only_cs_sdk_method_api
from xml_util import get_information_of_decl
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

java_path = "/home/nghibui/codes/java_cs_new_data/SRCML_DATA_JAVA_2/java/peggy/Buck2.xml"
# java_path = "/home/nghibui/codes/java_cs_new_data/Sample.xml"
project = "spring"
lang = "java"
java_package_object_mapping, java_object_method_mapping, java_third_party_package_object_mapping_list, java_third_party_object_method_mapping_list = get_necessary_library_information(lang,project)

try:
	print("--------------------------------------------------------------------------------------------")
	print(java_path)
	java_splits = java_path.split("/")
	# java_file = java_splits[8]
	java_parent_map, java_global_vars_mapping= get_necessary_information_to_process_source_code(java_path, lang, project)
	java_tree = parse_tree(java_path)
	java_parent_map = get_parent_map(java_tree)
	java_tree_str = ""
	java_root  = java_tree.getroot()

	
	imports = extract_all_import(java_root,lang)
	print(imports)

	candidate_sdk_packages = get_candidate_sdk_packages_from_import_list(imports,lang)
	print(candidate_sdk_packages)
	java_class_node = get_class_node_java(java_root)
	biggest_block_java = None
	for j in java_class_node.getchildren():
		tag = j.tag.replace(STUPID_URL,"")
		if tag == "block":
			biggest_block_java = j
	biggest_block = find_biggest_block(java_class_node)
	decl_stmts_global = get_all_decl_stmt_from_block_global(biggest_block)
	# global_vars_mapping = get_information_of_decl_stmts(decl_stmts_global)

	for block_java_node in biggest_block_java.getchildren():
		tag2 = block_java_node.tag.replace(STUPID_URL,"")
		if tag2 == "function":

			parameter_list_node = None
			for node2 in block_java_node:
				tag3 = node2.tag.replace(STUPID_URL,"")
				if tag3 == "parameter_list":
					parameter_list_node = node2

			for node2 in block_java_node:
				java_tree_str = ""
				tag3 = node2.tag.replace(STUPID_URL,"")

				if tag3 == "name":

					java_function_name_origin = node2.text
					print("Original method : " + java_function_name_origin + "-------------------")
					# print(parameter_list_node)
					java_function_name = node2.text.lower()
					if java_function_name == "updatejeu":
						processed_java_code = ""
						java_function_block = find_biggest_block(block_java_node)
						java_decl_stmt_locals = list()
						java_decl_stmt_locals = iterate_to_get_node_with_type(java_function_block,"decl_stmt",java_decl_stmt_locals)
						global_vars_mapping = get_information_of_decl_stmts(decl_stmts_global)
						java_local_vars_mapping = get_information_of_decl_stmts(java_decl_stmt_locals)
						# print(java_local_vars_mapping)
						java_decl_params = list()
						java_decl_params = iterate_to_get_node_with_type(parameter_list_node, "decl", java_decl_params)
						java_param_function_vars_mapping = get_information_of_decl(java_decl_params)

						# print(java_param_function_vars_mapping)
						java_local_vars_mapping = {**java_local_vars_mapping,**java_param_function_vars_mapping}
						java_local_vars_mapping = {**java_local_vars_mapping,**global_vars_mapping}
						
						# print(java_local_vars_mapping)
						processed_java_code = iterate_function_node_to_get_text("java",block_java_node,processed_java_code,java_parent_map,java_local_vars_mapping,java_global_vars_mapping,java_object_method_mapping,java_package_object_mapping,java_third_party_object_method_mapping_list,java_third_party_package_object_mapping_list,candidate_sdk_packages)
						
						processed_java_code = processed_java_code.replace("@","")
						processed_java_code = remove_empty_intext(processed_java_code)
						# processed_java_code = keep_only_method_api(processed_java_code)
						# processed_java_code = keep_only_java_sdk_method_api(processed_java_code)

						if processed_java_code:
							print(java_function_name + "-----------" + processed_java_code)
					

except Exception as e:
	print("Excetion in java part : " + str(e))


# with open("cs_keywords.txt","r") as f:
# 	data = f.readlines()
# 	cs_keywords = list()
# 	for line in data:
# 		line = line.replace("\n","")
# 		cs_keywords.append(line)

# # cs_path = "/home/nghibui/codes/code_clone_w2v/SRCML_DATA/lucene/cs/ArabicNormalizer.xml"
# cs_path = "/home/nghibui/codes/java_cs_new_data/MathCs.xml"
# project = "lucene"
# lang = "cs"
# cs_package_object_mapping, cs_object_method_mapping, cs_third_party_package_object_mapping_list, cs_third_party_object_method_mapping_list = get_necessary_library_information(lang,project)
# try:
# 	print("--------------------")
# 	print(cs_path)
# 	cs_splits = cs_path.split("/")
	
# 	cs_parent_map, cs_global_vars_mapping = get_necessary_information_to_process_source_code(cs_path, lang, project)
# 	cs_tree = parse_tree(cs_path)
# 	cs_parent_map = get_parent_map(cs_tree)
# 	cs_tree_str = ""
# 	cs_root  = cs_tree.getroot()

# 	imports = extract_all_import(cs_root,lang)
# 	print(imports)
# 	candidate_sdk_packages = get_candidate_sdk_packages_from_import_list(imports,lang)
# 	print(candidate_sdk_packages)

# 	cs_class_node = get_class_node_cs(cs_root)
# 	biggest_block_cs = None
# 	for c in cs_class_node.getchildren():
# 		tag = c.tag.replace(STUPID_URL,"")
# 		if tag == "block":
# 			biggest_block_cs = c

# 	biggest_block = find_biggest_block(cs_class_node)
# 	decl_stmts_global = get_all_decl_stmt_from_block_global(biggest_block)
# 	# global_vars_mapping = get_information_of_decl_stmts(decl_stmts_global)

# 	# print(global_vars_mapping)
# 	for block_cs_node in biggest_block_cs.getchildren():

# 		tag = block_cs_node.tag.replace(STUPID_URL,"")
# 		if tag == "function":
# 			for node2 in block_cs_node:
# 				tag3 = node2.tag.replace(STUPID_URL,"")
# 				if tag3 == "parameter_list":
# 					parameter_list_node = node2

# 			for node in block_cs_node:
# 				cs_tree_str = ""
# 				tag1 = node.tag.replace(STUPID_URL,"")
# 				if tag1 == "name":
# 					cs_function_name_origin = node.text
# 					cs_function_name = node.text.lower()
# 					processed_cs_code = ""

# 					cs_function_block = find_biggest_block(block_cs_node)
# 					cs_decl_stmt_locals = list()
# 					cs_decl_stmt_locals = iterate_to_get_node_with_type(cs_function_block,"decl_stmt",cs_decl_stmt_locals)	
# 					cs_local_vars_mapping = get_information_of_decl_stmts(cs_decl_stmt_locals)

				
# 					cs_decl_params = list()
# 					cs_decl_params = iterate_to_get_node_with_type(parameter_list_node, "decl", cs_decl_params)
# 					cs_param_function_vars_mapping = get_information_of_decl(cs_decl_params)
# 					cs_local_vars_mapping = {**cs_local_vars_mapping,**cs_param_function_vars_mapping}
# 					cs_local_vars_mapping = {**cs_global_vars_mapping, **cs_local_vars_mapping}
# 					# print(cs_local_vars_mapping)
# 					processed_cs_code = iterate_function_node_to_get_text("cs",block_cs_node,processed_cs_code,cs_parent_map,cs_local_vars_mapping,cs_global_vars_mapping,cs_object_method_mapping,cs_package_object_mapping,cs_third_party_object_method_mapping_list,cs_third_party_package_object_mapping_list,candidate_sdk_packages)
					
# 					processed_cs_code = processed_cs_code.replace("@","")
# 					processed_cs_code = remove_empty_intext(processed_cs_code)
# 					processed_cs_code = keep_only_cs_sdk_method_api(processed_cs_code,cs_keywords)
# 					print(cs_function_name_origin + "-----------" + str(processed_cs_code))

# except Exception as e:
# 	print("Excetion in cs part : " + str(e))