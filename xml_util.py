import xml.etree.ElementTree as ET
import re
import sys
import resource
resource.setrlimit(resource.RLIMIT_STACK,(2**29,-1))
sys.setrecursionlimit(10**6)
# tree = ET.parse("./sample/java/FlagResponse.xml")

# tree = ET.parse("/home/quocnghi/codes/code_clone_w2v/SRCML_DATA/lucene/cs/HyphenationException.xml")
# root  = tree.getroot()

# parent_map = dict((c, p) for p in tree.getiterator() for c in p)



ignore_elems = ["comment"]
ignore_symbols = ["[","]","{","}","(",")","#","%"]
data_types = ["int","long","float","double","uint","ushort","string","bool","boolean","char"]
ignore_operators = ["."]
STUPID_URL = "{http://www.srcML.org/srcML/src}"
primitive_types_java = ["boolean","byte","char","short","int","long","float","double"]
primitive_types_cs = ["byte","sbyte","int","uint","short","ushort","long","ulong","float","double","char","bool","object","string","decimal"]
important_tags = ["continue", "super","argument_list", "parameter_list", "constructor", "destructor", "enum", "throw", "try", "catch", "call", "for", "foreach", "decl","decl_stml","expr","expr_stmt","function","function_decl","interface","do","while","switch","using","lambda"]
def parse_tree(source_url):
	return ET.parse(source_url)

def get_parent_map(tree):
	return dict((c, p) for p in tree.getiterator() for c in p)

def find_class(root):
	for child_of_root in root:
		tag = child_of_root.tag.replace(STUPID_URL,"")
		if tag == "class":
			return child_of_root
	return None


def find_name_space(node):
	for child_of_root in node:
		tag = child_of_root.tag.replace(STUPID_URL,"")
		if tag == "namespace":
			return child_of_root
	return None

def has_children(node):
	return len(node) > 0 and True or False

def find_biggest_block(class_node):
	for child in class_node:
		tag = child.tag.replace(STUPID_URL,"")
		if tag == "block":
			return child
	return None

def iterate_block(block,file_str):
	
	recursive_str = file_str
	if has_children(block) == False:
		tag = block.tag.replace(STUPID_URL,"")
		if tag != "comment":
			recursive_str += child.text
		
		return file_str

	for child in block:
		tag = child.tag.replace(STUPID_URL,"")
		if tag != "comment":
			if tag == "class":
				recursive_str += "class "
			if tag == "specifier":
				recursive_str += child.text  + " "
			if tag == "specifier":
				recursive_str += child.text + " "
			if tag == "name":
				recursive_str += child.text + " "

def get_parent_node(child,parent_map):
	parent = parent_map[child]
	return parent

def get_parent_node_type(child,parent_map):
	parent = parent_map[child]
	tag = parent.tag.replace(STUPID_URL,"")
	return tag

def iterate_recursive(root,tree_str,parent_map):
	
	tag = root.tag.replace(STUPID_URL,"")

	text = ""
	if root.text != None:
		text = root.text.replace(";","").replace(" ","") + " "
		for symbol in ignore_symbols:
			text = text.replace(symbol,"")
		if text in ignore_symbols:
			text = ""

	if tag == "comment":
		tree_str = ""
	else:	
		if tag == "class":
			tree_str = tag + " "
		elif tag == "block":
			if root.text != "{" and root.text != "}":
				tree_str = ""
			else:
				tree_str = text
		elif tag == "operator":
			if root.text in ignore_operators:
				tree_str = ""
			else:
				tree_str = text
		elif tag == "specifier":
			tree_str = text
		elif tag == "condition":
			tree_str = "condition" + " "
		elif tag == "continue":
			tree_str = "continue" + " "
		elif tag == "break":
			tree_str = "break" + " "
		elif tag == "super":
			tree_str = "super" + " "
		elif tag == "argument_list":
			tree_str = "argument_list" + " "
		elif tag == "parameter_list":
			tree_str = "parameter_list" + " "
		elif tag == "constructor":
			tree_str = "constructor" + " "
		elif tag == "destructor":
			tree_str = "destructor" + " "
		elif tag == "enum":
			tree_str = "enum" + " "
		elif tag == "throw":
			tree_str = "throw" + " "
		elif tag == "try":
			tree_str = "try" + " "
		elif tag == "catch":
			tree_str = "catch" + " "
		elif tag == "call":
			tree_str = "call" + " "
		elif tag == "for":
			tree_str = "for" + " "
		elif tag == "foreach":
			tree_str = "foreach" + " "
		elif tag == "decl":
			tree_str = "decl" + " "
		elif tag == "decl_stmt":
			tree_str = "decl_stmt" + " "
		elif tag == "expr":
			tree_str = "expr" + " "
		elif tag == "expr_stmt":
			tree_str = "expr_stmt" + " "
		elif tag == "function":
			tree_str = "function" + " "
		elif tag == "interface":
			tree_str = "interface" + " "
		elif tag == "function_decl":
			tree_str = "function_decl" + " "
		elif tag == "do":
			tree_str = "do" + " "
		elif tag == "while":
			tree_str = "while" + " "
		elif tag == "switch":
			tree_str = "switch" + " "
		elif tag == "using":
			tree_str = "using" + " "
		elif tag == "lambda":
			tree_str = "lambda" + " "
		elif tag == "name":
			if get_parent_node_type(root,parent_map) == "name":
				if get_parent_node_type(get_parent_node(root,parent_map),parent_map) == "argument":
					if root.text != None:
						tree_str = text
					else:
						tree_str = ""
				else:
					tree_str = ""
			# elif get_parent_node_type(root) == "decl":
			# 	tree_str = "identifier" + " "
			elif get_parent_node_type(root,parent_map) == "expr" or get_parent_node_type(root,parent_map) == "decl":
				if root.text in data_types:
					tree_str = text
				else:
					tree_str = "identifier" + " "
			elif get_parent_node_type(root,parent_map) == "type":
				tree_str = text
			elif get_parent_node_type(root,parent_map) == "function":
				tree_str = text
			elif get_parent_node_type(root,parent_map) == "call":
				tree_str = text
			else:
				if root.text != None:
					tree_str = text
				else:
					tree_str = ""
		elif tag == "index":
			if root.text == "[]":		
				tree_str = "array" + " "
			else:
				tree_str = ""
		elif tag == "literal":
			tree_str = "literal " + root.attrib["type"]
		
		elif root.text != None:
			
			if text in ignore_symbols:
				tree_str = " "
			else:
				tree_str = text
		else:
			tree_str = " "
	for elem in root.getchildren():
		tree_str += iterate_recursive(elem,tree_str,parent_map) + " "

	return tree_str

def get_variable_and_method_call(call_node):
	object_list = list()
	method_list = list()
	count = 0	
	data = ""
	for elem in call_node.getchildren():
		tag = elem.tag.replace(STUPID_URL,"")

		if tag == "name":
			for elem2 in elem.getchildren():
				tag2 = elem2.tag.replace(STUPID_URL,"")
				if tag2 == "name":
					count += 1
					if count == 1:
						# object_list.append(elem.text.strip())
						if elem2.text != None:
							data += elem2.text.strip() + "."
					if count == 2:
						# method_list.append(elem.text.strip())
						if elem2.text != None:
							data += elem2.text.strip()
	if len(data.split(".")) == 2 and data.split(".")[1] != "":
	# return dict(*zip(object_list,method_list))
		return data
	return ""

def check_if_variable_method_is_static_call(variable_method):
	check = False
	if variable_method[0].isupper():
		check = True
	return check

# The name should be get_full_signature_from_call_node
def get_information_of_call_node(call_node,local_vars_mapping,global_vars_mapping,object_method_mapping,package_object_mapping,third_party_object_method_mapping_list,third_party_package_object_mapping_list,candidate_packages):
	final_signature = None
	variable_method = get_variable_and_method_call(call_node)
	
	
	if variable_method:
		
		if not check_if_variable_method_is_static_call(variable_method):

			# print("variable method : " + str(variable_method))
			# print "variable method : " + variable_method
		
			try:
				if variable_method:
					original_object_method = convert_to_original_object_of_method_call(variable_method,local_vars_mapping,global_vars_mapping,object_method_mapping)
					
					# print("original object method : " + str(original_object_method))
					if original_object_method != None:
						# full_signature = get_full_signature_of_object_method(original_object_method,package_object_mapping,object_method_mapping)

						# if full_signature != None:	
						# 	final_signature = full_signature
						# else:
						full_signature = get_full_signature_of_object_method(original_object_method,third_party_package_object_mapping_list[0],third_party_object_method_mapping_list[0],candidate_packages)
						if full_signature != None:
							final_signature = full_signature
						else:
							final_signature = original_object_method + "()"
						# print("full signature : " + str(full_signature))
			except Exception as e:
				print("get_information_of_call_node has error : " + str(e))

			if final_signature != None:
				if "(" not in final_signature or ")" not in final_signature:
					final_signature = final_signature + "()"
		else:
			full_signature = None
			try:
				full_signature = get_full_signature_of_object_method(variable_method,third_party_package_object_mapping_list[0],third_party_object_method_mapping_list[0],candidate_packages)
			except Exception as e:
				print("get_information_of_call_node part 2 has error : " + str(e))
			if full_signature != None:
				final_signature = full_signature + "()"

	# print("final signature here : " + str(final_signature))
	return final_signature
					
def get_full_signature_of_object_identifier(identifier, global_vars_mapping, local_vars_mapping,package_object_mapping,third_party_package_object_mapping_list):
	full_signature = None
	if identifier in local_vars_mapping:
		object_of_identifier = local_vars_mapping[identifier]
	elif identifier in global_vars_mapping:
		object_of_identifier = global_vars_mapping[identifier]
	
	for key, value in package_object_mapping.items():
		if object_of_identifier in value:
			full_signature = key + "." + object_of_identifier
	if full_signature == None:
		for third_party_package_object_mapping in third_party_package_object_mapping_list:
			for key2, value2 in third_party_package_object_mapping.items():
				if object_of_identifier in value2:
					full_signature = key2 + "." + object_of_identifier
	
	return full_signature

def iterate_function_node_to_get_function_signature(lang, function_node,input_tree_str,parent_map,local_vars_mapping,global_vars_mapping,object_method_mapping,package_object_mapping,third_party_object_method_mapping_list,third_party_package_object_mapping_list):
	tree_str = input_tree_str
	try:
		tag = function_node.tag.replace(STUPID_URL,"")

		# text = ""
		# if function_node.text != None:
		# 	text = function_node.text.replace(";","").replace(" ","").replace(".","").replace("{","").replace("}","") + " "
		# 	for symbol in ignore_symbols:
		# 		text = text.replace(symbol,"")
		# 	if text in ignore_symbols:
		# 		text = ""

		if tag == "comment":
			tree_str = ""
		else:
			if tag == "call":
				call_node_data = get_information_of_call_node(function_node,local_vars_mapping,global_vars_mapping,object_method_mapping,package_object_mapping,third_party_object_method_mapping_list,third_party_package_object_mapping_list)
				if call_node_data != None:
					tree_str = call_node_data + " "
				else:
					tree_str = " "
			elif tag == "name":
				
				if get_parent_node_type(function_node,parent_map) == "expr" or get_parent_node_type(function_node,parent_map) == "decl":	
					tree_str = " "
			elif tag == "literal":
				tree_str = " "
			elif tag == "decl_stmt":
				full_signature_of_variable_type_declaration = get_full_signature_of_variable_type_declaration(function_node, global_vars_mapping, local_vars_mapping,package_object_mapping,third_party_package_object_mapping_list)
				if full_signature_of_variable_type_declaration != None:
					tree_str = full_signature_of_variable_type_declaration + " "
			else:
				tree_str = " "

		for elem in function_node.getchildren():
			temp = iterate_function_node_to_get_function_signature(lang, elem,tree_str,parent_map,local_vars_mapping,global_vars_mapping,object_method_mapping,package_object_mapping,third_party_object_method_mapping_list,third_party_package_object_mapping_list) + " "
			if temp != None:
				tree_str += temp
			else:
				tree_str += ""				
	except Exception as e:
		print("iterate_function_node_to_get_function_signature has error: " + str(e))

	return tree_str


def iterate_function_node_to_get_text(lang, function_node,tree_str,parent_map,local_vars_mapping,global_vars_mapping,object_method_mapping,package_object_mapping,third_party_object_method_mapping_list,third_party_package_object_mapping_list, candidate_packages):
	try:
		tag = function_node.tag.replace(STUPID_URL,"")

		text = ""
		if function_node.text != None:
			text = function_node.text.replace(";","").replace(" ","").replace(".","").replace("{","").replace("}","") + " "
			for symbol in ignore_symbols:
				text = text.replace(symbol,"")
			if text in ignore_symbols:
				text = ""

		if tag == "comment":
			tree_str = ""
		else:
			if tag == "call":
				try:
					call_node_data = get_information_of_call_node(function_node,local_vars_mapping,global_vars_mapping,object_method_mapping,package_object_mapping,third_party_object_method_mapping_list,third_party_package_object_mapping_list,candidate_packages)
					

					if call_node_data != None:
						tree_str = "call " + call_node_data + " "
					else:
						tree_str = " "

				except Exception as e:
					print("get_information_of_call_node in iterate_function_node_to_get_text has error : " + str(e))

			# May comment this part for cross language setting, now comment out because we only want to get the API sequences
			elif tag == "name":
				
				if get_parent_node_type(function_node,parent_map) == "expr" or get_parent_node_type(function_node,parent_map) == "decl":
					if lang == "cs":
						if function_node.text in primitive_types_cs:
							tree_str = text + " "
						else:	
							tree_str = " "
					else:
						if function_node.text in primitive_types_java:
							tree_str = text + " "
						else:					
							tree_str = " "
			elif tag == "literal":
				tree_str = " "
			elif tag == "decl_stmt":
				full_signature_of_variable_type_declaration = "decl_stmt " + get_full_signature_of_variable_type_declaration(function_node, global_vars_mapping, local_vars_mapping,package_object_mapping,third_party_package_object_mapping_list)
				if full_signature_of_variable_type_declaration != None:
					tree_str = full_signature_of_variable_type_declaration + " "
			else:
				tree_str = text + " "

		for elem in function_node.getchildren():
			temp = iterate_function_node_to_get_text(lang, elem,tree_str,parent_map,local_vars_mapping,global_vars_mapping,object_method_mapping,package_object_mapping,third_party_object_method_mapping_list,third_party_package_object_mapping_list,candidate_packages) + " "
			if temp != None:
				tree_str += temp
			else:
				tree_str += ""
	except Exception as e:
		print("iterate_function_node_to_get_text has error: " + str(e))
	
	return tree_str

def iterate_to_get_original_code(root,tree_str):
	
	tag = root.tag.replace(STUPID_URL,"")

	text = ""
	if root.text != None:
		text = root.text


	if tag == "comment":
		tree_str = ""

	else:
		tree_str = text
	
	for elem in root.getchildren():
		
		tree_str += iterate_to_get_original_code(elem,tree_str) + " "

	return tree_str



def get_package_name_of_file(root,language,tree_str):
	if language == "cs":
		package_name = "namespace"
	else:
		package_name = "package"

	tag = root.tag.replace(STUPID_URL,"")
	tree_str = ""
	for elem in root.getchildren():
		child_tag = elem.tag.replace(STUPID_URL,"")

		if child_tag == package_name:
			for elem2 in elem.getchildren():
				child_tag = elem2.tag.replace(STUPID_URL,"")
				if child_tag == "name":
					nodes = list()
					nodes_new = iterate_to_get_node_with_types(elem2,"name",nodes)
				
					for node in nodes_new:
						if node.text != None: 
			
							tree_str = tree_str + "." + node.text

	return tree_str[1:]

def get_parameter_type_of_method(method_node):
	names = list()

	for elem in method_node.getchildren():
		child_tag =  elem.tag.replace(STUPID_URL,"")
		if child_tag == "parameter_list":
			for elem2 in elem.getchildren():
				child_tag2 = elem2.tag.replace(STUPID_URL,"")
				if child_tag2 == "parameter":
					for elem3 in elem2.getchildren():
						child_tag3 = elem3.tag.replace(STUPID_URL,"")
						if child_tag3 == "decl":
							for elem4 in elem3.getchildren():
								child_tag4 = elem4.tag.replace(STUPID_URL,"")
								if child_tag4 == "type":
									
									for elem5 in elem4.getchildren():
										child_tag5 = elem5.tag.replace(STUPID_URL,"")
										if child_tag5 == "name":
											if elem5.text != None:
												names.append(elem5.text)
											else:
												for elem6 in elem5.getchildren():
													child_tag6 = elem6.tag.replace(STUPID_URL,"")
													if child_tag6 == "name":
														names.append(elem6.text)
	return names


def iterate_to_get_node_with_type(root,node_type,nodes):
	
	tag = root.tag.replace(STUPID_URL,"")

	node = None
	if tag == node_type:	
		nodes.append(root)

	for elem in root.getchildren():
		iterate_to_get_node_with_type(elem,node_type,nodes)

	return nodes
	
def iterate_to_get_node_with_types(root,node_types,nodes):
	
	tag = root.tag.replace(STUPID_URL,"")

	node = None
	if tag in node_types:
		nodes.append(root)

	for elem in root.getchildren():
	
		iterate_to_get_node_with_types(elem,node_types,nodes)

	return nodes
# C#
# namespace = find_name_space(root)
# biggest_block = find_block(namespace)

# print iterate_recursive(root,tree_str,parent_map)


# Java
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

# 1 means source code, 0 means diff
def process_srcml_source_code(data,is_source=1):
	if is_source == 0:
		data = data.replace("shuangyinhao","")

	data = data.replace("\r"," ").replace("\n"," ").replace("\t"," ")
	data = data.lstrip()
	data = data.replace("("," ").replace(")"," ").replace("{","").replace("}","").replace("@","")

	splitted = data.split(" ")
	
	# Removed all empty string
	removed_empty = [x.strip() for x in splitted if x.strip()]
	data = " ".join(removed_empty)

	# Split all camel case
	tokens = data.split(" ")
	tokens = [x.strip() for x in tokens if x.strip()]
	splitted = list()
	for token in tokens:
		# if token[0].islower():
		temp = re.sub('(?!^)([A-Z][a-z]+)', r' \1', token).split()
		splitted.extend(temp)
		# else:
			# splitted.append(token)
	
	splitted2 = [x for x in splitted if len(x)>=1]

	data = " ".join(splitted2)	
	data = data.lower()	
	return data


# def extract_full_signature_of_methods(nodes):
# 	for node in nodes:
		
def extract_type_of_variable(nodes):
	for node in nodes:

		for elem in node.getchildren():
			child_tag = elem.tag.replace(STUPID_URL,"")
			
			if child_tag == "decl":

				for elem2 in elem.getchildren():
					child_tag2 = elem2.tag.replace(STUPID_URL,"")
			
					if child_tag2 == "type":

						for elem3 in elem2.getchildren():
							child_tag3 = elem3.tag.replace(STUPID_URL,"")
							if child_tag3 == "name":

								print("Found the type : " + str(elem3.text))
					if child_tag2 == "name":
						print("Found the variable name : " + str(elem2.text))


def get_data_from_class_node(class_node, package_name):
	data = ""
	excludes = ["block","specifier","name"]
	data += class_node.tag.replace(STUPID_URL,"") + " "
	for elem in class_node.getchildren():
		tag = elem.tag.replace(STUPID_URL,"")
		if tag not in excludes:
			data += tag + " "
		if tag == "name":
			if elem.text != None:
				data += package_name + "." + elem.text.strip() + " "
		if tag == "super":
			for elem2 in elem.getchildren():
				if elem2.text != None:
					data += "super" + " " + elem2.text + " "
		# if elem.text != None:
		# 	data += elem.text + " " 
	return data

def get_data_from_import_node(node,data):
	# tag = node.tag.replace(STUPID_URL,"")
	text = ""

	if node.text != None:
		text = node.text
		data = text

	for elem in node.getchildren():
		data += get_data_from_import_node(elem,data)

	return data

def extract_all_import(root,lang):
	if lang == "cs":
		keyword = "using"
	else:
		keyword = "import"
	import_nodes = list()
	import_nodes = iterate_to_get_node_with_type(root,keyword,import_nodes)
	import_list = list()
	
	for node in import_nodes:
		data = ""
		data = get_data_from_import_node(node,data)
		
		if lang == "cs":
			if "=" in data:
				splits = data.split("= ")
				import_list.append(splits[len(splits)-1])
			else:
				data = data.replace("using","")
				# data = data + " using "
				
				import_list.append(data)
		else:
			data = data.replace("import","")
			# data = data + " import "
			# print(data)
			import_list.append(data)

	return import_list

# def extract_all_global_variable():

def get_all_decl_stmt_from_block_global(block):
	decl_stmts = list()
	for elem in block.getchildren():
		tag = elem.tag.replace(STUPID_URL,"")
		if tag == "decl_stmt":
			decl_stmts.append(elem)
	return decl_stmts

	
def get_full_signature_of_variable_type_declaration(decl_stmt_node, global_vars_mapping, local_vars_mapping,package_object_mapping,third_party_package_object_mapping_list):
	
	variable_type = None
	full_signature = None
	try:
		for elem in decl_stmt_node.getchildren():
			tag = elem.tag.replace(STUPID_URL,"")
			if tag == "decl":
				for elem2 in elem.getchildren():
					tag2 = elem2.tag.replace(STUPID_URL,"")
					if tag2 == "type":
						for elem3 in elem2.getchildren():
							tag3 = elem3.tag.replace(STUPID_URL,"")
							if tag3 == "name":
								if elem3.text != None:
									variable_type = elem3.text
								else:
									for elem4 in elem3.getchildren():
										tag4 = elem4.tag.replace(STUPID_URL,"")
										if tag4 == "name":
											if elem4.text != None:
												variable_type = elem4.text
		
		if variable_type != None:
			for key, value in package_object_mapping.items():
				if variable_type in value:
					full_signature = key + "." + variable_type
		if full_signature == None:
			for third_party_package_object_mapping in third_party_package_object_mapping_list:
				for key2, value2 in third_party_package_object_mapping.items():
					if variable_type in value2:
						full_signature = key2 + "." + variable_type
		if full_signature == None:
			full_signature = variable_type

		# print full_signature
	except Exception as e:
		print("get_full_signature_of_variable_type_declaration has error : " + str(e))
	return full_signature

def get_information_of_decl(decl_nodes):
	variable_type_list = list()
	variable_name_list = list()
	for decl_node in decl_nodes:
		for elem in decl_node.getchildren():
			tag = elem.tag.replace(STUPID_URL,"")
		
			if tag == "type":
				for elem1 in elem.getchildren():
					tag1 = elem1.tag.replace(STUPID_URL,"")
					if tag1 == "name":
						if elem1.text != None:
							variable_type_list.append(elem1.text)

					package_parts = list()

					for elem2 in elem1.getchildren():
						tag2 = elem2.tag.replace(STUPID_URL,"")
						# If there is a name here, which mean the parameter is declared by the whole package
						if tag2 == "name":
							# print(elem2.text)
							package_parts.append(elem2.text.strip())
					if len(package_parts) != 0:
						variable_type_list.append(".".join(package_parts))		
			if tag == "name":
				
				variable_name_list.append(elem.text)
	# print(variable_type_list)
	# print(variable_name_list)
	return dict(zip(variable_name_list,variable_type_list))


def get_information_of_decl_stmts(decl_stmt_nodes):
	variable_type_list = list()
	variable_name_list = list()
	for decl_stmt_node in decl_stmt_nodes:
		for elem in decl_stmt_node.getchildren():
			tag = elem.tag.replace(STUPID_URL,"")
			if tag == "decl":
				for elem2 in elem.getchildren():
					tag2 = elem2.tag.replace(STUPID_URL,"")

					if tag2 == "type":
						for elem3 in elem2.getchildren():
							tag3 = elem3.tag.replace(STUPID_URL,"")

							if tag3 == "name":

								if elem3.text != None:
									variable_type_list.append(elem3.text)
								else:
									package_parts = list()
									for elem4 in elem3.getchildren():
										tag4 = elem4.tag.replace(STUPID_URL,"")

										if tag4 == "name":
											if elem4.text != None:
												# variable_type_list.append("decl" + " " + elem4.text)
												package_parts.append(elem4.text.strip())
												# variable_type_list.append(elem4.text)
									if len(package_parts) == 1:
										variable_type_list.append(package_parts[0])
									else:
										variable_type_list.append(".".join(package_parts))	

							# package_parts = list()		
							# for elem5 in elem3.getchildren():
							# 	tag5 = elem3.tag.replace(STUPID_URL,"")
							# 	# If there is a name here, which mean the parameter is declared by the whole package
							# 	if tag5 == "name":

							# 		# print(elem2.text)
							# 		package_parts.append(elem3.text.strip())
							# variable_type_list.append(".".join(package_parts))	

					if tag2 == "name":

						variable_name_list.append(elem2.text)

	return dict(zip(variable_name_list,variable_type_list))

def convert_to_original_object_of_method_call(variable_method,local_vars_mapping,global_vars_mapping,object_method_mapping):
	object_method = None
	try:
		var, method = variable_method.split(".")
		obj = None
		
		if var in local_vars_mapping:
			obj = local_vars_mapping[var]
		elif var in global_vars_mapping:
			obj = global_vars_mapping[var]
		
		if obj != None:
			object_method = obj + "." + method
	except Exception as e:
		print("convert_to_original_object_of_method_call has error : " + str(e))

	return object_method


def get_full_signature_of_object_method(object_method,package_object_mapping,object_method_mapping,candidate_packages):
	full_signature = None
	print(object_method)
	try:
		splits = object_method.split(".")
		if len(splits) > 2:
			full_signature = object_method
		else:
			target_obj, target_method = object_method.split(".")


			
			if target_obj and target_method:
				candidate_package_obj_mapping = {}
				candidate_package_objs = list()
				for package in candidate_packages:
					temp_package_obj = package + "." + target_obj
					candidate_package_objs.append(temp_package_obj)
				# if package in package_object_mapping.keys():
					# candidate_package_obj_mapping[package] = package_object_mapping[package]

			# for key,value in object_method_mapping.items():
			# 	splits = key2.split(".")
			# 	temp_obj[len(temp_obj)-1]

			# for obj, methods in object_method_mapping.items():
			# 	for package in candidate_packages:
			# 		candidate_signature.append
				
				if len(candidate_package_objs) > 0:
					for package_obj in candidate_package_objs:
						if package_obj in object_method_mapping.keys():
							candidate_methods = object_method_mapping[package_obj]
							
							for candidate_method in candidate_methods:
								original_candidate_method = candidate_method.split("(")[0]
								if target_method == original_candidate_method:
									# full_signature = package_obj + "." + candidate_method
									full_signature = package_obj + "." + original_candidate_method
									break;
				else:

				# if full_signature == None:
			# print(full_signature)\
					# temp_signature = None
					# temp_package = None
					# for package, objs in package_object_mapping.items():
					# 	if target_obj in objs:
					# 		temp_package = package
					# 		temp_signature = package + "." + target_obj
					# if temp_signature != None:	
					for key2,methods in object_method_mapping.items():
						splits = key2.split(".")
						object_part = splits[len(splits)-1]
						package_part = splits[:len(splits)-1]

						if target_obj == object_part:

							for m in methods:
								if target_method in m:				
									full_signature =  key2+ "." + target_method
									break
	except Exception as e:
		print("get_full_signature_of_object_method has error : " + str(e))		

	# print("full signature here : " + str(full_signature))

	return full_signature

def filter_method_call_node(call_nodes):
	return_nodes = list()
	for node in call_nodes:
		isMethodCall = True
		for elem in node.getchildren():
			tag = elem.tag.replace(STUPID_URL,"")
			if tag == "argument_list":
				return_nodes.append(node)
				break	

	return return_nodes

def get_necessary_library_information(lang,project):
	third_party_package_object_mapping_list = list()
	third_party_object_method_mapping_list = list()

	third_party_package_object_mapping_list.append(get_package_object_mapping("sdk",lang))
	third_party_object_method_mapping_list.append(get_object_method_mapping("sdk",lang))

	package_object_mapping = get_package_object_mapping(project,lang)
	object_method_mapping = get_object_method_mapping(project,lang)

	return package_object_mapping, object_method_mapping, third_party_package_object_mapping_list, third_party_object_method_mapping_list

def get_necessary_information_to_process_source_code(url, lang, project):
	tree = parse_tree(url)
	parent_map = get_parent_map(tree)
	tree_str = ""
	root  = tree.getroot()

	class_nodes = list()
	class_nodes = iterate_to_get_node_with_type(root,"class",class_nodes)
	
	biggest_block = find_biggest_block(class_nodes[0])

	decl_stmts_global = get_all_decl_stmt_from_block_global(biggest_block)

	global_vars_mapping = get_information_of_decl_stmts(decl_stmts_global)

	
	return parent_map, global_vars_mapping
def get_function_name_with_params(function_node):
	function_name = None
	type_list = list()
	for node in function_node.getchildren():
		tag = node.tag.replace(STUPID_URL,"")
		if tag == "name":
			function_name = node.text.strip()
		if tag == "parameter_list":
			for node2 in node.getchildren():
				tag2 = node2.tag.replace(STUPID_URL,"")
				if tag2 == "parameter":
					for node3 in node2.getchildren():
						tag3 = node3.tag.replace(STUPID_URL,"")
						if tag3 == "decl":
							for node4 in node3.getchildren():
								tag4 = node4.tag.replace(STUPID_URL,"")
								if tag4 == "type":
										for node5 in node4.getchildren():
											tag5 = node5.tag.replace(STUPID_URL,"")
											if tag5 == "name":
												if node5.text != None:
													type_list.append(node5.text.strip())

	return function_name + "(" + ",".join(type_list) + ")"

def get_candidate_sdk_packages_from_import_list(import_list,lang):
	packages = []
	for im in import_list:
		im = im.strip()
		splits = im.split(".")

		if lang == "java":
			package = splits[:len(splits)-1]
			package = ".".join(package)
			
			if "java." in package or "javax." in package or "sun." in package or "w3c." in package or "jdk." in package or "junit." in package:
				packages.append(package)
		else:
			package = splits[:len(splits)]
			package = ".".join(package)
			
			if package.startswith("System") or "NUnit." in package or "Microsoft." in package:
				packages.append(package)

	return list(set(packages))

def get_global_part_of_root(root, lang, package_object_mapping, third_party_package_object_mapping_list):

	transformed_code = ""
	package_name = ""
	package_name = get_package_name_of_file(root,lang,package_name)

	imports = extract_all_import(root,lang)

	decorations = ["class","interface"]

	class_nodes = list()
	class_nodes = iterate_to_get_node_with_types(root,decorations,class_nodes)

	if len(class_nodes) != 0:
		try:
			class_data = get_data_from_class_node(class_nodes[0], package_name)
			class_name = None
			for node in class_nodes[0].getchildren():
				tag = node.tag.replace(STUPID_URL,"")
				if tag == "name":
					class_name = node.text.strip()

			biggest_block = find_biggest_block(class_nodes[0])

			decl_stmts_global = get_all_decl_stmt_from_block_global(biggest_block)

			global_vars_mapping = get_information_of_decl_stmts(decl_stmts_global)

			transformed_code = package_name + " " + " ".join(imports) + " " + class_data + " "

			for decl_stmt in decl_stmts_global:
				full_signature_of_variable_type_declaration = get_full_signature_of_variable_type_declaration(decl_stmt, global_vars_mapping, global_vars_mapping,package_object_mapping,third_party_package_object_mapping_list)
			
				transformed_code += full_signature_of_variable_type_declaration + " "

			function_nodes = list()
			function_nodes = iterate_to_get_node_with_type(biggest_block,"function",function_nodes)
			
			for function_node in function_nodes:
				full_function_name = package_name + "." + class_name + "." + get_function_name_with_params(function_node) + " "
				transformed_code += full_function_name

			
		except Exception as e:
			print(e)
	return transformed_code

def transform_source_code_to_extract_only_api_sequence(url, lang, project):
	tree = parse_tree(url)
	parent_map = get_parent_map(tree)
	tree_str = ""
	root  = tree.getroot()

	transformed_code = ""
	package_name = ""
	package_name = get_package_name_of_file(root,lang,package_name)

	imports = extract_all_import(root,lang)

	decorations = ["class","interface"]

	class_nodes = list()
	class_nodes = iterate_to_get_node_with_types(root,decorations,class_nodes)


	if len(class_nodes) != 0:
		try:
			# class_data = get_data_from_class_node(class_nodes[0], package_name)

			# transformed_code = package_name + " " + " ".join(imports) + " "

			biggest_block = find_biggest_block(class_nodes[0])

			decl_stmts_global = get_all_decl_stmt_from_block_global(biggest_block)

			global_vars_mapping = get_information_of_decl_stmts(decl_stmts_global)

			function_nodes = list()
			function_nodes = iterate_to_get_node_with_type(biggest_block,"function",function_nodes)

			package_object_mapping = get_package_object_mapping(project,lang)
			object_method_mapping = get_object_method_mapping(project,lang)

			third_party_package_object_mapping_list = list()
			third_party_object_method_mapping_list = list()

			third_party_package_object_mapping_list.append(get_package_object_mapping("sdk",lang))
			third_party_object_method_mapping_list.append(get_object_method_mapping("sdk",lang))

			for function_node in function_nodes:
				function_block = find_biggest_block(function_node)
			
				decl_stmt_locals = list()
				decl_stmt_locals = iterate_to_get_node_with_type(function_block,"decl_stmt",decl_stmt_locals)
				
				local_vars_mapping = get_information_of_decl_stmts(decl_stmt_locals)

				function_str = ""
				function_text = iterate_function_node_to_get_function_signature(lang,function_node,function_str,parent_map,local_vars_mapping,global_vars_mapping,object_method_mapping,package_object_mapping,third_party_object_method_mapping_list,third_party_package_object_mapping_list)
				if function_text != None:
					transformed_code += function_text + " "
		except Exception as e:
			print("File : " + url + " has exception : " + str(e))
	return transformed_code.strip()


def transform_source_code(url, lang, project):
	tree = parse_tree(url)
	parent_map = get_parent_map(tree)
	tree_str = ""
	root  = tree.getroot()

	transformed_code = ""
	package_name = ""
	package_name = get_package_name_of_file(root,lang,package_name)

	imports = extract_all_import(root,lang)

	decorations = ["class","interface"]

	class_nodes = list()
	class_nodes = iterate_to_get_node_with_types(root,decorations,class_nodes)


	if len(class_nodes) != 0:
		try:
			class_data = get_data_from_class_node(class_nodes[0], package_name)

			transformed_code = package_name + " " + " ".join(imports) + " " + class_data + " "

			biggest_block = find_biggest_block(class_nodes[0])

			decl_stmts_global = get_all_decl_stmt_from_block_global(biggest_block)

			global_vars_mapping = get_information_of_decl_stmts(decl_stmts_global)

			for k, v in global_vars_mapping.items():
				transformed_code += v + " "

			function_nodes = list()
			function_nodes = iterate_to_get_node_with_type(biggest_block,"function",function_nodes)

			package_object_mapping = get_package_object_mapping(project,lang)
			object_method_mapping = get_object_method_mapping(project,lang)

			third_party_package_object_mapping_list = list()
			third_party_object_method_mapping_list = list()

			third_party_package_object_mapping_list.append(get_package_object_mapping("sdk",lang))
			third_party_object_method_mapping_list.append(get_object_method_mapping("sdk",lang))

			for function_node in function_nodes:
				function_block = find_biggest_block(function_node)
			
				decl_stmt_locals = list()
				decl_stmt_locals = iterate_to_get_node_with_type(function_block,"decl_stmt",decl_stmt_locals)
				
				local_vars_mapping = get_information_of_decl_stmts(decl_stmt_locals)
				# print local_vars_mapping
				for k, v in local_vars_mapping.items():
					transformed_code += v + " "
				function_str = ""
				function_text = iterate_function_node_to_get_text(lang,function_node,function_str,parent_map,local_vars_mapping,global_vars_mapping,object_method_mapping,package_object_mapping,third_party_object_method_mapping_list,third_party_package_object_mapping_list)
				if function_text != None:
					transformed_code += function_text + " "
		except Exception as e:
			print("File : " + url + " has exception : " + str(e))
	return transformed_code.strip()


def get_object_method_mapping(project,lang):
	object_method_mapping = dict()
	with open("./SIGNATURE_DATA/" + project + "/signature_" + lang + ".txt") as f:
		data = f.readlines()

		for line in data:
		
			splits = line.strip().replace("\n","").split(".")
			obj = ".".join(splits[0:len(splits)-1])
			method = splits[len(splits)-1]
		
			if obj in object_method_mapping:
				method_arr = object_method_mapping[obj]
				method_arr.append(method)
				method_arr = set(method_arr)
				object_method_mapping[obj] = list(method_arr)
			else:
				method_arr = [method]
				object_method_mapping[obj] = method_arr

	return object_method_mapping


def get_package_object_mapping(project,lang):
	package_object_mapping = dict()
	try:
		with open("./SIGNATURE_DATA/" + project + "/signature_" + lang + ".txt") as f:
			data = f.readlines()

			for line in data:
				
				splits = line.strip().replace("\n","").split(".")
				package = ".".join(splits[0:len(splits)-2])
				obj = splits[len(splits)-2]
				
				if package in package_object_mapping:
					obj_arr = package_object_mapping[package]
					obj_arr.append(obj)
					obj_arr = set(obj_arr)
					package_object_mapping[package] = list(obj_arr)
				else:
					obj_arr = [obj]
					package_object_mapping[package] = obj_arr
	except Exception as e:
		print(e)
	return package_object_mapping

# print transform_source_code("/home/quocnghi/codes/code_clone_w2v/SRCML_DATA/datastax/java/AbstractArrayCodec.xml","java","datastax")
# print get_object_method_mapping("antlr","java")
# print get_package_object_mapping("antlr","java")
# transform_source_code("./SRCML_DATA/antlr/java/DFAState.xml","java")

# print iterate_recursive(root,tree_str,parent_map)
# cs_tree = parse_tree("./SRCML_DATA/antlr/cs/CommonToken.xml")
# # cs_tree = parse_tree("./SRCML_DATA/antlr/java/CommonTokenStream.xml")
# cs_parent_map = get_parent_map(cs_tree)
# cs_tree_str = ""
# cs_root  = cs_tree.getroot()


# print get_package_name_of_node(cs_root,"cs",cs_tree_str)


# cs_class_node = get_class_node_cs(cs_root)

# biggest_block_cs = None

# for c in cs_class_node.getchildren():
# 	tag = c.tag.replace(STUPID_URL,"")
# 	if tag == "block":
# 		biggest_block_cs = c
# 		# for block_cs_node in biggest_block_cs.getchildren():
# 		# 	tag = block_cs_node.tag.replace(STUPID_URL,"")

# 		# 	if tag == "function":
# 		# 		print tag 		
# 		# 		cs_tree_str = ""
# 		# 		raw_cs_code = iterate_to_get_original_code(block_cs_node,cs_tree_str)
# 		# 		print raw_cs_code
# 		# 		break

# decl_stmts = list()
# decl_stmts_cs = iterate_to_get_node_with_type(biggest_block_cs,"decl_stmt",decl_stmts)


# calls = list()
# calls_cs = iterate_to_get_node_with_type(biggest_block_cs,"call",calls)

# print calls_cs



# extract_type_of_variable(decl_stmts_cs)


# for cs_node in expr_nodes_cs:

# 	processed_cs_code = iterate_recursive(cs_node,cs_tree_str,cs_parent_map)
# 	processed_cs_code = process_srcml_source_code(processed_cs_code)
# 	print processed_cs_code