#!/bin/env python
# coding: utf-8

## FEDERAL UNIVERSITY OF BAHIA (UFBA)
## ATYIMOLAB (www.atyimolab.ufba.br)
## University College London
## Denaxas Lab (www.denaxaslab.org)

# File:           $03_writeBlocks.py$
# Version:        $v1$
# Last changed:   $Date: 2017/12/04 12:00:00$
# Purpose:        $Write blocks following instructions of keys.txt file$
# Author:         Robespierre Pita and Clicia Pinto and Marcos Barreto and Spiros Denaxas

# Usage:  /path/to/python/03_writeBlocks.py
# IMPORTANT: if blocking is set, this file should be executed after 04_enconding_blocking.py

# Comments: generates several files under the folder blocks/tmp_/ if blocking is set.
# Each file corresponds to one block

from pyspark import SparkContext, SparkConf
from pyspark import SparkFiles
from unicodedata import normalize
from doctest import testmod
from operator import add
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import csv
import time
import hashlib
import os
import os.path
import commands
import config
import config_static
ini = time.time() # Initializing time couting

conf = config_static.en_conf
sc = SparkContext(conf=conf)
print "MAIN PROGRAM MESSAGE (writeBlocks):			 writeBlocks starting..."

def set_variables():
	print "MAIN PROGRAM MESSAGE (writeBlocks):			 In set_variables()"

	global status_larger_base
	status_larger_base = config.status_larger_base
	global status_smaller_base
	status_smaller_base = config.status_smaller_base
	global default_folder
	default_folder = config.default_folder

	global status_blocking
	status_blocking = config.e_status_blocking

	global size_bloom_col_n
	size_bloom_col_n = config.e_size_bloom_col_n
	global size_bloom_col_mn
	size_bloom_col_mn = config.e_size_bloom_col_mn
	global size_bloom_col_bd
	size_bloom_col_bd = config.e_size_bloom_col_bd
	global size_bloom_col_mr
	size_bloom_col_mr = config.e_size_bloom_col_mr
	global size_bloom_col_g
	size_bloom_col_g = config.e_size_bloom_col_g

	global status_name
	status_name = config.e_status_name
	global status_birth_date
	status_birth_date = config.e_status_birth_date
	global status_gender
	status_gender = config.e_status_gender
	global status_mother_name
	status_mother_name = config.e_status_mother_name
	global status_municipality_residence
	status_municipality_residence = config.e_status_municipality_residence
	global status_state
	status_state = config.e_status_state

	global col_i
	col_i = config_static.e_col_i
	global col_n
	col_n = config_static.e_col_n
	global col_mn
	col_mn = config_static.e_col_mn
	global col_bd
	col_bd = config_static.e_col_bd
	global col_g
	col_g = config_static.e_col_g
	global col_mr
	col_mr = config_static.e_col_mr
	global col_st
	col_st = config_static.e_col_st

def set_variables_larger():
	print "MAIN PROGRAM MESSAGE (writeBlocks):			 In set_variables_larger()"

	global partitioning
	partitioning = config_static.larger_partitioning
	global input_file
	input_file = config_static.e_largest_input_file
	print "MAIN PROGRAM MESSAGE (writeBlocks):			 Input File: " +input_file
	global outputFolder
	outputFolder = directory_block_larger

def set_variables_smaller():
	print "MAIN PROGRAM MESSAGE (writeBlocks):			 In set_variables_smaller()"

	global partitioning
	partitioning = config_static.smaller_partitioning
	global input_file
	input_file = config_static.e_smaller_input_file
	print "MAIN PROGRAM MESSAGE (writeBlocks):			 Input FIle: " +input_file
	global outputFolder
	outputFolder = directory_block_smaller

def create_path():
	print "MAIN PROGRAM MESSAGE (writeBlocks):			 In create_path()"
	global directory_main
	directory_main = config_static.e_directory_blocks
	global directory_block_larger
	directory_block_larger = config_static.e_directory_block_larger
	global directory_block_smaller
	directory_block_smaller = config_static.e_directory_block_smaller

	os.system("mkdir "+directory_main)
	os.system("mkdir "+directory_block_larger)
	os.system("mkdir "+directory_block_smaller)
	if(status_blocking):
		global keyFolder
		keyFolder = str(config_static.e_directory_key_folder)
		global pathFileKey
		pathFileKey = directory_main + str(config_static.e_file_key_blocking)
		os.system("touch "+pathFileKey)

def getKeys(line):
	line = line.split(";")
	for x in line[:6]:
		if os.path.isfile(outputFolder+"tmp_/"+x):
			os.system("cat " + outputFolder+"tmp_/"+x + " >> " + outputFolder+line[6])
			os.system("sort -u "+outputFolder+line[6]+" -o "+outputFolder+line[6])
	return 0

# Initializing functions

set_variables()
create_path()
flagl = 1
flags = 1

while(flagl or flags):

	if (status_larger_base and flagl):
		print "MAIN PROGRAM MESSAGE (writeBlocks):			 Starting round over larger base  (1)"
		set_variables_larger()
		flagl = 0
		rounds = 0
		if (status_smaller_base == 0):
			flags = 0

	elif(status_smaller_base and flags):
		print "MAIN PROGRAM MESSAGE (writeBlocks):			 Starting round over smaller base  (2)"
		set_variables_smaller()
		flags = 0
		flagl = 0
	rounds = 1
	if(status_blocking):
		keysRDD = sc.textFile(keyFolder+"keys.txt", partitioning).cache().map(getKeys).collect()
	else:
		fim = time.time()
		approx_time = fim - ini
		print "MAIN PROGRAM MESSAGE (writeBlocks):          Nothing to do. WriteBlocks completed in: " + str(approx_time)


fim = time.time()
approx_time = fim - ini
print "MAIN PROGRAM MESSAGE (writeBlocks):          writeBlocks completed in: " + str(approx_time)
