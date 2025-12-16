#!/usr/bin/env python
import argparse
import re
########################################################## {COPYRIGHT-TOP} ###
# Copyright 2023 IBM Corporation
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the MIT License
# which accompanies this distribution, and is available at
# http://opensource.org/licenses/MIT
########################################################## {COPYRIGHT-END} ###
#
################################################
# Linear logging statistics script
# Takes a QM error log as it's argument and prints out the 
# timestamped log use counts, reporting totals at the end
# and the timestamp of the first log extent deletions
# (if they occurred).
#
# Media images that updated the oldest media image required
# are also reported.
#
# Paul Harris - Nov 2025
################################################
parser = argparse.ArgumentParser()
parser.add_argument("inFile", help="MQ Queue Manager Error Log File",nargs=1)

args = parser.parse_args()
inFile = args.inFile[0]

create_count_cum = 0
delete_count_cum = 0
reuse_count_cum = 0

timestamp = ""
first_delete_msg = "No log extents deleted"
image_copy_file=""

print ("Parsing file %s" %inFile)

regex_dict = {
    'timestamp': re.compile(r'([0-9]{2}\/[0-9]{2}\/[0-9]{2,4} [0-9]{2}:[0-9]{2}:[0-9]{2}).*Process'),
    'log_stats' : re.compile(r'AMQ7490I\D*(\d+) created\D*(\d+) reused\D*(\d+) deleted')
}

with open(inFile) as file:
   line = file.readline()
   while line:
      if line.startswith("AMQ7468I"):
        line = file.readline()
        new_image_copy_file = line.split()[3]
        if(image_copy_file != "" and image_copy_file != new_image_copy_file):
            print("{} ===> Media image has updated media recovery file to {}".format(timestamp,new_image_copy_file))
        image_copy_file = new_image_copy_file

      if line.startswith("AMQ7467I"):
        oldest_log_required = file.readline().strip()
  
      match = regex_dict['timestamp'].search(line)
      if match:
         timestamp = match.group(1)
      else:
         match = regex_dict['log_stats'].search(line)
         if match:
             create_count = int(match.group(1)) 
             reuse_count = int(match.group(2)) 
             delete_count = int(match.group(3)) 
             print("{} \tcreated:{} \treused:{} \tdeleted:{} \tRestart log: {}".format(timestamp,create_count,reuse_count,delete_count,oldest_log_required))
             if(delete_count_cum == 0 and delete_count > 0) :
                first_delete_msg = "First log extents deleted at {} ({})".format(timestamp,delete_count)
             create_count_cum = create_count_cum + create_count
             delete_count_cum = delete_count_cum + delete_count
             reuse_count_cum = reuse_count_cum + reuse_count
      line = file.readline()

print()
print(first_delete_msg)
print("Totals -  \t\tcreated:{} \treused:{} \tdeleted:{}".format(create_count_cum, reuse_count_cum, delete_count_cum))
            
