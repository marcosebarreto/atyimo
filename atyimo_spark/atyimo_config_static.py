#!/bin/env python
# coding: utf-8

## FEDERAL UNIVERSITY OF BAHIA (UFBA)
## ATYIMOLAB (www.atyimolab.ufba.br)
## University College London
## Denaxas Lab (www.denaxaslab.org)

# File:           $atyimo_config_static.py$
# Version:        $v1$
# Last changed:   $Date: 2017/12/04 12:00:00 $
# Purpose:        Static configuration for AtyImo
# Author:         Robespierre Pita and Clicia Pinto and Marcos Barreto and Spiros Denaxas

# Usage:  /path/to/python/atyimo_config_static.py

# Comments:

import config
from pyspark import SparkContext, SparkConf
from pyspark import SparkFiles

##----##----##----##----##----##----##----##----##----##----##----##----##----##--------##----##----##----##----##----##----
# Set parameters used in the preprocessing module (01_preprocessing.py)
# Destination folder for standardized files
pp_directory_padronized_files =	str(config.default_folder)+"standardized/"

# Larger data set after standardization
pp_larger_output_file = str(pp_directory_padronized_files)+"larger_file_final.csv"

# Smaller data set after standardization
pp_smaller_output_file = str(pp_directory_padronized_files)+"smaller_file_final.csv"

# Boolean indicating the existence of these variables in the larger data set
pp_larger_status_index = 1		# Index
# Boolean indicating the existence of these variables in the smaller data set
pp_smaller_status_index = 1		# Index

# Position of index column in the larger data set
pp_larger_col_i = 0		# Index
# Position of index column in the smaller data set
pp_smaller_col_i = 0    # Index

##----##----##----##----##----##----##----##----##----##----##----##----##----##--------##----##----##----##----##----##----
# Set parameters used in the encoding module (04_encoding_blocking.py)
# Larger input file to the encoding module
e_largest_input_file = str(pp_larger_output_file)
# Smaller input file to the encoding module
e_smaller_input_file = str(pp_smaller_output_file)

# Folder name to Bloom files
e_directory_blocks = config.default_folder + "blocks/"
# Folder location for keys used for blocking (if e_status_blocking is set)
e_directory_key_folder = config.default_folder + "blocks/keys/"
# Folder name to Bloom files related to the larger data set
e_directory_block_larger =  e_directory_blocks + "block_larger/"
# Folder name to Bloom files related to the smaller data set
e_directory_block_smaller =  e_directory_blocks + "block_smaller/"
# File name for blocking keys
e_file_key_blocking = "keyBloking.txt"

# Items position in the standardized files
e_col_i = 0     # Index
e_col_n = 2     # Name
e_col_mn = 3    # Mother's name
e_col_bd =4     # Date of birth
e_col_g = 7     # Gender
e_col_mr = 6    # Municipality of residence
e_col_st = -1   # State (not used)

##----##----##----##----##----##----##----##----##----##----##----##----##----##--------##----##----##----##----##----##----
# Set parameters used in the correlation module (05_correlation.py)
# Size of Bloom filter
c_size_bloom_vector = int(config.e_size_bloom_col_n) + int(config.e_size_bloom_col_mn) + int(config.e_size_bloom_col_bd) + int(config.e_size_bloom_col_mr)
# Folder name to linkage results
c_directory_results = config.default_folder + "linkage_results/"
# Name of linkage file with Dice higher than the main cutoff (c_cutoff_result)
c_file_result = c_directory_results + "result.linkage"
# Name of linkage file with Dice higher than the secondary cutoff and below the main cutoff
c_file_result_rescue = c_directory_results + "result-Rescue.linkage"
# Secondery cutoff (Dice)
c_cutoff_result_rescue = 7000
# Boolean indicating the existence of a rescue linkage file below the c_cutoff_result
c_status_rescue = 0

##----##----##----##----##----##----##----##----##----##----##----##----##----##--------##----##----##----##----##----##----
# Set parameters used in the deduplication module (06_dedupByKey.py)
# Column used in the deduplication module step 1
d_key_col_step1 = 1
# Column used in the deduplication module step 1
d_key_col_step2 = 2
# Input file to the deduplication module
d_input_file = c_file_result
# Temporary output file to the deduplication module - step1
d_tmp_step1_output_file = c_directory_results +"result_and_rescue_sort_tmp_step1.linkage"
# Temporary output file to the deduplication module - step2
d_tmp_step2_output_file = c_directory_results +"result_and_rescue_sort_tmp_step2.linkage"
# Final output file to the deduplication module - step1
d_output_file_step1 = c_directory_results +"result_and_rescue_dedup_tmp_step1.linkage"
# Final output file (oficial result)
d_output_file_step2 = c_directory_results +"result_dedup.linkage"
# Final output file for rescue
d_output_file_step2_rescue = c_directory_results +"rescue_dedup.linkage"

##----##----##----##----##----##----##----##----##----##----##----##----##----##--------##----##----##----##----##----##----
# Set parameters used in the dataMart module (07_geraDataMart.py)
# Folder name to datamart files
dm_directory_datamarts = config.default_folder + "dataMarts/"
# Input file to the dataMart module
dm_input_file = c_directory_results +"result_dedup.linkage"
# Output file to the dataMart module
dm_output_file1 = dm_directory_datamarts +"dataMart_type1.csv"
dm_output_file2 = dm_directory_datamarts +"dataMart_type2.csv"
dm_output_file3 = dm_directory_datamarts +"dataMart_type3.csv"
dm_output_file4 = dm_directory_datamarts +"dataMart_type4.csv"
# Larger base file used to retrieve the tuples to the datamart
dm_larger_base_for_merge = pp_directory_padronized_files +"larger_file_with_index.csv"
# Smaller base file used to retrieve the tuples to the datamart
dm_smaller_base_for_merge = pp_directory_padronized_files +"smaller_file_with_index.csv"

##----##----##----##----##----##----##----##----##----##----##----##----##----##--------##----##----##----##----##----##----
# Set configuration to drive executions over Spark Framework
# To see more about configuration alternatives: http://spark.apache.org/docs/latest/configuration.html
pp_conf = SparkConf().setMaster('local[4]').setAppName('01_preprocessing').set('spark.executor.cores','4').set('spark.executor.memory','3g').set('spark.driver.memory','3g').set('spark.driver.maxResultSize', '10g').set('spark.eventLog.enabled','false')
en_conf = SparkConf().setMaster('local[4]').setAppName('02_enconding_blocking').set('spark.executor.cores','4').set('spark.executor.memory','15g').set('spark.driver.memory','200g').set('spark.driver.maxResultSize', '40g').set('spark.eventLog.enabled','false')
co_conf = SparkConf().setMaster('local[4]').setAppName('03_correlation').set("spark.executor.extraJavaOptions", "-XX:+UseG1GC").set('spark.executor.cores','1').set('spark.executor.memory','2g').set('spark.driver.memory','500g').set('spark.driver.maxResultSize','60g').set('spark.eventLog.enabled','false').set('spark.executor.heartbeatInterval','4900s').set('spark.network.timeout','10000000s')#.set
dm_conf = SparkConf().setMaster('local[3]').setAppName('05_generatedm').set('spark.executor.cores','2').set('spark.executor.memory','3g').set('spark.driver.memory','3g').set('spark.driver.maxResultSize', '10g').set('spark.eventLog.enabled','false')

# Set how much the RDD's of larger/smaller databases must be partitioned and parallelized
larger_partitioning = 2048
smaller_partitioning = 2048

#----##----##----##----##----##----##----##----##----##----##----##----##----##--------##----##----##----##----##----##----
# Set parameters used in the extract step from second round
sr_ex_directory_padronized_files =	str(config.default_folder)+"second_round_standardized/"
# Larger file name after standardization
sr_ex_larger_output_file = str(sr_ex_directory_padronized_files)+"larger_file_standardized.csv"
# Smaller file name after standardization
sr_ex_smaller_output_file = str(sr_ex_directory_padronized_files)+"smaller_file_standardized.csv"

sr_e_status_name = 1					# Name
sr_e_status_mother_name = 1				# Mother's name
sr_e_status_birth_date = 1				# Date of birth
sr_e_status_gender = 1				    # Gender
sr_e_status_municipality_residence = 0	# Municipality of residence
sr_e_status_state = 0

# File result_dedup.linkage that is used as reference to collect the records in gray area
sr_ex_reference_file = c_file_result

#----##----##----##----##----##----##----##----##----##----##----##----##----##--------##----##----##----##----##----##----
# Set parameters used in the extract step of second round
# Folder name to transformed files in second round
sr_e_directory_blocks = config.default_folder + "second_round_blocks/"
# Folder name to transformed files of the larger data set in the second round
sr_e_directory_block_larger =  sr_e_directory_blocks + "block_larger/"
# Folder name to transformed files of the smaller data set in the second round
sr_e_directory_block_smaller =  sr_e_directory_blocks + "block_smaller/"
# File name of blocking keys in second round
sr_e_file_key_blocking = "keyBloking.txt"
# Size of Bloom vector in attributes that are transformed
sr_e_size_bloom_col = 100

sr_directory_results = config.default_folder + "second_round_linkage_results/"
sr_c_file_result = sr_directory_results + "result.linkage"
sr_c_file_result_rescue = sr_directory_results + "result-Rescue.linkage"
sr_c_file_result_final = sr_directory_results + "result_final.linkage"

sr_c_size_bloom_vector = 100
sr_c_boundary_name_1 = 9000
sr_c_boundary_name_2 = 8000
sr_c_boundary_name_3 = 7000
sr_c_boundary_name_4 = 6500
sr_c_boundary_birth = 7000
sr_c_number_of_attributes = 7
sr_c_size_in_bits = 100

# Folder name to datamart files
sr_dm_directory_datamarts = config.default_folder + "second_round_dataMarts/"

sr_dm_input_file = sr_c_file_result

# Output file to the dataMart module
sr_dm_output_file1 = sr_dm_directory_datamarts +"dataMart_type1.csv"
sr_dm_output_file2 = sr_dm_directory_datamarts +"dataMart_type2.csv"
sr_dm_output_file3 = sr_dm_directory_datamarts +"dataMart_type3.csv"
sr_dm_output_file4 = sr_dm_directory_datamarts +"dataMart_type4.csv"
sr_dm_output_file_final = sr_dm_directory_datamarts +"dataMart_type_final.csv"

# Larger base file used to retrieve the tuples to the datamart
sr_dm_larger_base_for_merge = pp_directory_padronized_files +"larger_file_with_index.csv"
# Smaller base file used to retrieve the tuples to the datamart
sr_dm_smaller_base_for_merge = pp_directory_padronized_files +"smaller_file_with_index.csv"
