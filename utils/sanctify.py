# -*- coding: utf-8 -*-
# =============================================================================
# FOLDER STRUCTURE
# README.md
# utils/
#     sanctify.py
# Contents/
#     Dir1/
#         Subdir1
#     Dir2/
#         Subdir1
#         Subdir2/
#             file.ext
#
# =============================================================================

import re
import os
import sys
from functools import reduce
from operator import mul
import urllib.parse

# =============================================================================
#
# =============================================================================

def create_dir(path):
    if not os.path.isdir(path):
        os.mkdir(path)
    if os.listdir(path) == []:
        open(os.path.join(path, os.path.split(path)[-1]+'.md'), 'w').close()

def pathjoin(path):
    temp = ''
    for x in path:
        temp = os.path.join(temp, x)
    return temp

def reduction(rlist):
    return reduce(mul, rlist, 1)

tab = " "*4

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0])))
CONTENTS = "CONTENTS"
create_dir(os.path.join(ROOT,CONTENTS))

# =============================================================================
#
# =============================================================================

with open(os.path.join(ROOT, "README.md"), 'r') as f:
    file =  f.readlines()

contents_start = [file.index(x) for x in file if re.search("## contents", x, re.IGNORECASE)][0]
temp_file = file[contents_start+2:]
contents_end = [temp_file.index(x) for x in temp_file if re.search("^\n$", x, re.IGNORECASE)][0]

# =============================================================================
#
# =============================================================================

regex_patterns = {
        "level1":"^\d+\. ([a-zA-Z ]+)\(.*\)\\n",
        "level21":'^ +\d+\. \[.\] \[([a-zA-Z ]+)\]\(.*\)\\n',
        'level22':'^ +\d+\. ([a-zA-Z ]+)\(.*\)\\n'}

base_pattern = "|".join(regex_patterns.values())

path_list = [ROOT, CONTENTS]
repo_list = ['../master', CONTENTS]
previous_level = 0

temp_file = file[contents_start+2:contents_start+2+contents_end]
for ind, element in enumerate(temp_file):
    current_level = re.search('^({}+)'.format(tab), element)
    if current_level is None:
        current_level = 1
    else:
        current_level = int(re.search('^({}+)'.format(tab), element).span()[1]/len(tab)+1)
    if previous_level >= current_level:
        path_list = path_list[:-(previous_level-current_level+1)]
    path_list.append(reduction(re.search(base_pattern, element).groups(1)))
    previous_level = current_level
    create_dir(pathjoin(path_list))
    repo_link = pathjoin(path_list).replace(ROOT, '../master').replace('\\','/')
    temp_file[ind] = re.sub(r'\(.*\)','({})'.format( urllib.parse.quote(repo_link)), element)



file = file[:contents_start+2]+temp_file+file[contents_start+2+contents_end:]

with open(os.path.join(ROOT, "README.md"), 'w') as f:
    f.writelines(file)


