import re
import string
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import defaultdict
import subprocess
import os
from xml_util import iterate_recursive
import xml.etree.ElementTree as ET

from xml_util import get_parent_map
from xml_util import find_name_space
from xml_util import parse_tree
# from xml_util import find_block


def normalize(word_vec):
	norm = np.linalg.norm(word_vec)
	if norm == 0:
		return word_vec
	return word_vec/norm
	
def stripcomments(text):
	return re.sub('//.*?\n|/\*.*?\*/', ' ', text, flags=re.S)

# def remove_noise_keywords(data):
# 	keywords = ["package","namespace"]
# 	for word in data:
# 		if word not 
def check_if_token_is_method_signature(token):
	splits = token.split(".")
	is_signature = False
	if len(splits) >= 2 and "(" in token and "*" not in token:
		is_signature = True
	return is_signature

def check_if_token_is_object_signature(token):
	# with open("cs_keywords.txt") as cs_f:
	# 	data = cs_f.readlines()
	# splits = token.split(".")
	ignore_symbols = ["[","]","{","}","(",")","#","%","!=","=","+=","+","-","!","&&","||","!!","-=","*","&","|","<>","<",">"]
	is_signature = False
	# if len(splits) >= 2 and splits[len(splits)-1] != "" and ("(" not in token and ")" not in token) and "*" not in token:
	# 	is_signature = True
	# return is_signature

	if "(" not in token and ")" not in token and token not in ignore_symbols and token[0] != ".":
		is_signature = True
	return is_signature

def remove_empty_intext(text):
	text = text.split(" ")
	removed_empty = [x.strip() for x in text if x.strip()]
	text = " ".join(removed_empty)
	# return re.sub(' +',' ',text)
	return text
	
def vector_summing(sentence,code2vec,dimension):
	mean = np.sum([code2vec[w] for w in sentence if w in code2vec] or [np.zeros(dimension)],axis=0)
	return mean.reshape(1,-1)


def vector_summing_with_tfidf(sentence,code2vec,word2weight,dimension):
	mean = np.sum([code2vec[w] * word2weight[w] for w in sentence if w in code2vec] or [np.zeros(dimension)],axis=0)
	return mean.reshape(1,-1)


def vector_averaging(sentence,code2vec,dimension):
	mean = np.nanmean([code2vec[w] for w in sentence if w in code2vec] or [np.zeros(dimension)],axis=0)
	return mean.reshape(1,-1)

def vector_averaging_with_tfidf(sentence,code2vec,word2weight,dimension):
	mean = np.nanmean([code2vec[w] * word2weight[w] for w in sentence if w in code2vec] or [np.zeros(dimension)],axis=0)
	return mean.reshape(1,-1)

def word2weight(documents):
	vectorizer = TfidfVectorizer(min_df=1)
	vectorizer.fit(documents)
	max_idf = max(vectorizer.idf_)
	word2weight = defaultdict(lambda:max_idf,[(w,vectorizer.idf_[i]) for w,i in vectorizer.vocabulary_.items()])
	return word2weight

def has_number(data):
	return bool(re.search(r'\d', data))

def remove_hex(data):
	return re.sub(r'[^\w]', ' ', data)



# 1 means source code, 0 means diff
def process_srcml_source_code(data,is_source=1):
	if is_source == 0:
		data = data.replace("shuangyinhao","")
	non_ignore_symbols = [">","<","?","!","&","/","%","=","|","*","+","-","~","^",":"]
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
	splitted2 = list()

	for x in splitted:
		if (len(x) == 1) and (x in non_ignore_symbols):
			splitted2.append(x)

	splitted2 = [x for x in splitted if len(x)>=1]

	data = " ".join(splitted2)	
	data = data.lower()	
	return data

def process_expression(data,type):
	if type == 1:
		lang = "cs"
	else:
		lang = "java"
	name = "Temp." + lang
	with open(name,"w") as f:
		f.write(data)


	command = "srcml " + name + " > Temp.xml"
	os.system(command)

	tree = parse_tree("Temp.xml")
	root  = tree.getroot()
	parent_map = get_parent_map(tree)
	tree_str = ""
	processed_code = iterate_recursive(root,tree_str,parent_map)
	processed_code = processed_code.split(" ")
	removed_empty = [x.strip() for x in processed_code if x.strip()]

	processed_code = " ".join(removed_empty)
	return processed_code

def process_diff_srcml(data,type):
	
	data = data.replace("shuangyinhao","")
	splits = data.split("\n")
	del splits[0]
	new_splits = list()
	for split in splits:
		if split:
			if split[0] == "+" or split[0] == "-":
				new_splits.append(split[1:])
			else:
				new_splits.append(split)
	new_data = "\n".join(new_splits)
	if type == 1:
		lang = "cs"
	else:
		lang = "java"
	name = "Temp." + lang
	with open(name,"w") as f:
		f.write(new_data)


	command = "srcml " + name + " > Temp.xml"
	os.system(command)

	tree = parse_tree("Temp.xml")
	root  = tree.getroot()
	parent_map = get_parent_map(tree)
	tree_str = ""
	processed_code = iterate_recursive(root,tree_str,parent_map)

	processed_code = process_srcml_source_code(processed_code)
	return processed_code

	
def process_diff_srcml2(data):
	
	data = data.replace("shuangyinhao","")
	splits = data.split("\n")
	del splits[0]
	new_splits = list()
	for split in splits:
		if split:
			if split[0] == "+" or split[0] == "-":
				new_splits.append(split[1:])
			else:
				new_splits.append(split)
	new_data = "\n".join(new_splits)
	# For python3
	translator = str.maketrans('', '', string.punctuation)

	# Remove all comments
	data = stripcomments(data)

	# Remove all line breaks
	data = data.replace("\r"," ").replace("\n"," ")
	# Remove all curly brackets
	data = data.replace("{"," ").replace("}"," ").replace("(","").replace(")","").replace("[","").replace("]","")


	# Remove all punctuations
	data = data.translate(translator)

	# Remove all numbers
	splitted = data.split(" ")
	removed_number = [ x for x in splitted if not x.isdigit() ]

	# Removed all empty string
	removed_empty = [x.strip() for x in removed_number if x.strip()]

	data = " ".join(removed_empty)
	return data

def process_source_code_with_remove_line_break(data,is_source=1):
	# For python2 remove all punctuations
	# table = string.maketrans("","")
	# data = data.translate(table,string.punctuation)

	# For python3 remove all punctuations
	# translator = str.maketrans('', '', string.punctuation)
	# data = data.translate(translator)

	if is_source == 0:
		data = data.replace("shuangyinhao","")

	# Remove all hex
	data = remove_hex(data)

	# Remove all line breaks and tab
	data = data.replace("\r"," ").replace("\n"," ").replace("\t"," ")

	# Remove all numbers
	splitted = data.split(" ")
	removed_number = [ x for x in splitted if not x.isdigit() ]

	# Removed all empty string
	removed_empty = [x.strip() for x in removed_number if x.strip()]

	data = " ".join(removed_empty)
	return data


def process_source_code(data,is_source=1):
	# For python2 remove all punctuations
	# table = string.maketrans("","")
	# data = data.translate(table,string.punctuation)

	# For python3 remove all punctuations
	# translator = str.maketrans('', '', string.punctuation)
	# data = data.translate(translator)

	# Remove all comments
	data = stripcomments(data)

	if is_source == 0:
		data = data.replace("shuangyinhao","")

	# Remove all hex
	data = remove_hex(data)
	# # To lower case
	# data = data.lower()

	# Remove all line breaks
	data = data.replace("\r"," ").replace("\n"," ")

	# Remove all curly brackets
	data = data.replace("{"," ").replace("}"," ")

	# Remove all special character
	data = re.sub("[^a-zA-Z0-9-_*.]", " ", data)

	# print data
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
	
	# Remove all numbers
	removed_number = [ x for x in splitted if not x.isdigit() ]
	data = " ".join(removed_number)

	# Split all underscore case
	splitted = data.split("_")
	data = " ".join(splitted)

	# Split all underscore case
	splitted = data.split(".")
	data = " ".join(splitted)

	

	# Remove all numbers again
	splitted = data.split(" ")
	removed_number = [ x for x in splitted if not x.isdigit() ]

	# Removed all empty string
	removed_empty = [x.strip() for x in removed_number if x.strip()]

	removed_short_identifier = [ x for x in removed_empty if not len(x)==1 ]

	removed_all_number_in_phrase = [ x for x in removed_short_identifier if has_number(x)==False ]
	data = " ".join(removed_all_number_in_phrase)
	return data.lower()

def split_source_to_sequences(input,window=40,stride=10):
	splitted = input.splitlines()
	subs = list()
	for i in xrange(0,len(splitted),stride):
		subseq = splitted[i:(i+window)]
		subs.append(subseq)
	return subs


def get_all_subsequences(input,window=20,stride=4):
	splitted = input.split(" ")
	subs = list()
	for i in xrange(0,len(splitted),stride):
		subseq = splitted[i:(i+window)]
		subs.append(subseq)
	return subs


def mean_average_precision(rs):
    """Score is mean average precision
    Relevance is binary (nonzero is relevant).
    >>> rs = [[1, 1, 0, 1, 0, 1, 0, 0, 0, 1]]
    >>> mean_average_precision(rs)
    0.78333333333333333
    >>> rs = [[1, 1, 0, 1, 0, 1, 0, 0, 0, 1], [0]]
    >>> mean_average_precision(rs)
    0.39166666666666666
    Args:
        rs: Iterator of relevance scores (list or numpy) in rank order
            (first element is the first item)
    Returns:
        Mean average precision
    """
    return np.mean([average_precision(r) for r in rs])


def average_precision(r):
    r = np.asarray(r) != 0
    out = [precision_at_k(r, k + 1) for k in range(r.size) if r[k]]
    if not out:
        return 0.
    return np.mean(out)

def precision_at_k(r, k):
    """Score is precision @ k
    Relevance is binary (nonzero is relevant).
    >>> r = [0, 0, 1]
    >>> precision_at_k(r, 1)
    0.0
    >>> precision_at_k(r, 2)
    0.0
    >>> precision_at_k(r, 3)
    0.33333333333333331
    >>> precision_at_k(r, 4)
    Traceback (most recent call last):
        File "<stdin>", line 1, in ?
    ValueError: Relevance score length < k
    Args:
        r: Relevance scores (list or numpy) in rank order
            (first element is the first item)
    Returns:
        Precision @ k
    Raises:
        ValueError: len(r) must be >= k
    """
    assert k >= 1
    r = np.asarray(r)[:k] != 0
    if r.size != k:
        raise ValueError('Relevance score length < k')
    return np.mean(r)

def mean_reciprocal_rank(rs):
    """Score is reciprocal of the rank of the first relevant item
    First element is 'rank 1'.  Relevance is binary (nonzero is relevant).
    Example from http://en.wikipedia.org/wiki/Mean_reciprocal_rank
    >>> rs = [[0, 0, 1], [0, 1, 0], [1, 0, 0]]
    >>> mean_reciprocal_rank(rs)
    0.61111111111111105
    >>> rs = np.array([[0, 0, 0], [0, 1, 0], [1, 0, 0]])
    >>> mean_reciprocal_rank(rs)
    0.5
    >>> rs = [[0, 0, 0, 1], [1, 0, 0], [1, 0, 0]]
    >>> mean_reciprocal_rank(rs)
    0.75
    Args:
        rs: Iterator of relevance scores (list or numpy) in rank order
            (first element is the first item)
    Returns:
        Mean reciprocal rank
    """
    rs = (np.asarray(r).nonzero()[0] for r in rs)
    return np.mean([1. / (r[0] + 1) if r.size else 0. for r in rs])
    
# def main():
# 	print get_all_subsequences("namespace Antlr3 Analysis using Grammar Antlr3 Tool Grammar using GrammarAST Antlr3 Tool GrammarAST public class Action Label Label private readonly GrammarAST actionAST public Action Label GrammarAST actionAST base ACTION actionAST actionAST public override bool Is Epsilon get return true public override bool Is Action get return true public override string To String return actionAST public override string To String Grammar return To String")

# if __name__ == "__main__":
# 	main()

def keep_only_method_api(text):
	splits = text.split(" ")
	processed = list()
	processed_text = None
	for s in splits:
		if "." in s and "(" in s:
			processed.append(s)
	if len(processed) > 1:
		processed_text = " ".join(processed)
	return processed_text

def only_contains_keywords(splits,keywords):
	count = 0
	check = False
	for s in splits:
		if s in keywords:
			count = count + 1
	# print("Count : " + str(count))
	# print("Len splits : " + str(len(splits)))
	if count == len(splits):
		check = True
	return check

def is_an_api_call_token(token):
	check = False
	splits = token.split(".")
	if len(splits) >= 2:
		check = True
	return check

def remove_uncessary_tokens(text):
	# splits = re.split(" ",text)
	# processed = list()
	# processed_text = None

	unness = ["public","private","protected","return"]
	for u in unness:
		text = text.replace(u,"")
	return text
def keep_only_java_sdk_method_api(text,java_keywords):
	# splits = text.split(" ")
	splits = re.split(" ",text)
	processed = list()
	processed_text = None

	
	for s in splits:
		if "." in s and "(" in s:
		# if is_an_api_call_token(s):
			# if "java." in s or "javax." in s or "w3c." in s or "junit." in s:
			if "java." in s or "javax." in s or "w3c." in s:
				processed.append(s)
		# if s in java_keywords:
		# 	processed.append(s)
	# if not only_contains_keywords(processed, java_keywords):
	if len(processed) > 1:
		processed_text = " ".join(processed)

	return processed_text

# def primitive_type_check_cs(s):
# 	primitive_types_cs = ["byte","sbyte","int","uint","short","ushort","long","ulong","float","double","char","bool","string","decimal"]
# 	check = False
# 	for t in primitive_types_cs:
# 		line = t + "."
# 		if line in s:
# 			check = True
# 			break
# 	return check

def keep_only_cs_sdk_method_api(text,cs_keywords):
	# splits = text.split(" ")
	splits = re.split(" ",text)
	processed = list()
	processed_text = None

	
	for s in splits:
		if "." in s and "(" in s:	
		# if is_an_api_call_token(s):
			# if s.startswith("System") or "NUnit." in s:
			if s.startswith("System."):
				# if "string." in s and "System" not in s:
				# 	s = "System." + s
				
				processed.append(s)
		# if s in cs_keywords:
		# 	processed.append(s)
	# if not only_contains_keywords(processed, cs_keywords):
	if len(processed) > 1:
		processed_text = " ".join(processed)
	
		# processed == None
	return processed_text