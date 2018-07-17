import xml.etree.ElementTree as ET
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
from xml_util import find_block
from util import process_expression
# tree = ET.parse("./sample/java/FlagResponse.xml")

with open("./sample/Sample.cs") as f:
	data = f.read()
tree = ET.parse("./sample/Sample.xml")
root  = tree.getroot()


parent_map = get_parent_map(tree)
tree_str = ""
processed_code = process_expression(data,1)

print processed_code