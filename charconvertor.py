#!/usr/bin/python
# HTML Character Convertor
# Replaces HTML entities in a given string - with their correct character.
import os
import html
import xml.etree.ElementTree as ET

def extract_key_value_to_dict(filename):

	allLines = open(filename, 'r').readlines()
	dictionary = {}
	for line in allLines:
		key,value=line.split(':')
		dictionary[key]=value.strip()

	return dictionary


def string_to_convert(string):

	htmlspecialchar = extract_key_value_to_dict("spcharhtml")
	for k,v in htmlspecialchar.items():
		if string.find(v) != -1:
			print(string.replace(v, k))


string_to_convert("Hello world &iacute;")
string_to_convert("Hello world &quot;")
string_to_convert("Hello world &ndash;&quot;")

path_to_file = os.path.join('xml_test', 'cig.gov.pt.xml')
contents = open(path_to_file).read()
myStrLen = len(contents)
a = html.unescape(contents)

f = open('output.xml', 'wt', encoding='utf-8')
f.write(a)
