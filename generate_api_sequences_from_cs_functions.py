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
from util import remove_empty_intext
from util import keep_only_method_api
from xml_util import get_information_of_decl
from util import keep_only_cs_sdk_method_api

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
	
	for r,ds,files in os.walk(os.path.join(CURRENT_DIR,"SRCML_DATA",project)):
		for file in files:
			file_path = os.path.join(r,file)
			split = file_path.split("/")
			if split[7] == "cs":
				cs_paths.append(file_path)
		
	for cs_path in cs_paths:
		try:
			print("---------------------------------------------------------------------------------")
			print(cs_path)
			cs_splits = cs_path.split("/")
			cs_file = cs_splits[8]
			cs_parent_map, cs_global_vars_mapping, cs_package_object_mapping, cs_object_method_mapping, cs_third_party_package_object_mapping_list, cs_third_party_object_method_mapping_list = get_necessary_information_to_process_source_code(cs_path, "cs", project)
			cs_tree = parse_tree(cs_path)
			cs_parent_map = get_parent_map(cs_tree)
			cs_tree_str = ""
			cs_root  = cs_tree.getroot()
			cs_class_node = get_class_node_cs(cs_root)
			biggest_block_cs = None
			for c in cs_class_node.getchildren():
				tag = c.tag.replace(STUPID_URL,"")
				if tag == "block":
					biggest_block_cs = c


			biggest_block = find_biggest_block(cs_class_node)
			decl_stmts_global = get_all_decl_stmt_from_block_global(biggest_block)
			global_vars_mapping = get_information_of_decl_stmts(decl_stmts_global)


			for block_cs_node in biggest_block_cs.getchildren():
				tag = block_cs_node.tag.replace(STUPID_URL,"")
				if tag == "function":
					for node2 in block_cs_node:
						tag3 = node2.tag.replace(STUPID_URL,"")
						if tag3 == "parameter_list":
							parameter_list_node = node2

					for node in block_cs_node:
						cs_tree_str = ""
						tag1 = node.tag.replace(STUPID_URL,"")
						if tag1 == "name":
							cs_function_name_origin = node.text
							cs_function_name = node.text.lower()
							processed_cs_code = ""

							cs_function_block = find_biggest_block(block_cs_node)
							cs_decl_stmt_locals = list()
							cs_decl_stmt_locals = iterate_to_get_node_with_type(cs_function_block,"decl_stmt",cs_decl_stmt_locals)	
							cs_local_vars_mapping = get_information_of_decl_stmts(cs_decl_stmt_locals)

							cs_decl_params = list()
							cs_decl_params = iterate_to_get_node_with_type(parameter_list_node, "decl", cs_decl_params)
							cs_param_function_vars_mapping = get_information_of_decl(cs_decl_params)
							cs_local_vars_mapping = {**cs_local_vars_mapping,**cs_param_function_vars_mapping}
							cs_local_vars_mapping = {**cs_local_vars_mapping,**global_vars_mapping}

							processed_cs_code = iterate_function_node_to_get_text("cs",block_cs_node,processed_cs_code,cs_parent_map,cs_local_vars_mapping,cs_global_vars_mapping,cs_object_method_mapping,cs_package_object_mapping,cs_third_party_object_method_mapping_list,cs_third_party_package_object_mapping_list)
							processed_cs_code = processed_cs_code.replace("@","")
							processed_cs_code = remove_empty_intext(processed_cs_code)
							# processed_cs_code = keep_only_method_api(processed_cs_code)
							processed_cs_code = keep_only_cs_sdk_method_api(processed_cs_code)
							print(cs_function_name_origin + "-----------" + str(processed_cs_code))
							if processed_cs_code:
								with open("./sentences/cs_functions_sdk_api_sequences.txt","a") as out:
									out.write(processed_cs_code + "\n")

		except Exception as e:
			print("Excetion in cs part : " + str(e))