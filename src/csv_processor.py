import sys
import os
from pathlib import Path
import pandas as pd 
import numpy as np 
import sklearn
import csv
import random
import linecache
import matplotlib.pyplot as plt 
import time

def get_dataframe(filename):
	df = None

	try:
		df = pd.read_csv(filename)

	except:
		print("Error while loading file : "+filename)

	return df

def HUM_creator(e13_folder,tfp_folder,hum_folder):
	"""
	Very simple compilation of the HUM datasets merging E13 and TFP.
	E13 count: 1481
	TFP count: 469
	final accounts: 1950
	"""
	files = ["users.csv","followers.csv","friends.csv","tweets.csv"]
	for file in files:
		f1 = open(e13_folder+file,"r", errors="ignore")
		f2 = open(tfp_folder+file,"r", errors="ignore")
		f3 = open(hum_folder+file,"w", errors="ignore")
		for lines in f1.readlines():
			f3.write(lines)

		for lines in f2.readlines()[1:]:
			f3.write(lines)
	f1.close()
	f2.close()
	f3.close()

def FAK_creator(fsf_folder,int_folder,twt_folder,fak_folder):
	"""
	From the dataset of fake accounts, we undersample the dataset randomly to 
	reach the same amout as the HUM dataset.
	FSF count: 1169
	INT count: 1337
	TWT count: 845
	fake accounts count: 3351
	final accounts needed: 1950
	percent randomly selected from the fake sample: 0.5819 
	"""
	file_merging(fsf_folder,int_folder,twt_folder,fak_folder,0.5819)

def file_merging(folder1,folder2,folder3,result_folder,percent):
	# 3 folders with fake accounts
	# 
	# In each folder we start by randomly undersampling the users
	# Then we use the ids collected for the users and fetch the corresponding data
	# in the other files.
	folder_list = [folder1,folder2,folder3]
	files = ["users.csv","followers.csv","friends.csv","tweets.csv"]

	# flag to check if the header has already been added.
	# [users","followers","friends","tweets"]
	# 0 -> no header
	# 1 -> header already added
	head_flags = [0,0,0,0]

	for folder in folder_list:
		# List for the user's ids randomly picked (reset for each folder)
		list_of_ids = []

		for file in files:

			#with open(folder+file, newline='', encoding='utf-32') as fp:
			#	reader = csv.reader(fp, dialect='excel')
			#	for line in reader:
			#		print(str(line).encode("utf-8"))
			#fp.close()


			f = open(folder+file,"r", errors="ignore")
			r = open(result_folder+file,"a",errors="ignore")
			
			lines = f.readlines()

			len_file = len(lines)

			# choosing the number of lines we'll keep
			number_lines = int(percent*len_file)

			# This creates a random sub-sample of the lines of the files
			# 
			# This works to select the percent of users we are interested but 
			# for the other files we have to select the corresponding data.

			print("file: "+folder+file)

			if file == "users.csv":
				if head_flags[0] == 0:
					r.write(lines[0])
					head_flags[0] = 1

				for line in random.sample(range(1,len_file), number_lines):
					#print("list_of_ids: "+str((lines[line].split('","')[0].strip('"'))))
					list_of_ids.append(int(lines[line].split('","')[0].strip('"')))
					r.write(lines[line])
				#print("liste: "+str(list_of_ids))
				#time.sleep(1)
				# no need for conditional check, just make sure that the flag is at 1 after header added

			# So after selecting the percent of users we want, we have to fetch the ids 
			# and collect the corresponding data in the other files.
			# for tweets.csv the id is the [3] element
			# for friends.csv the id is the [0] element
			# and for followers.csv the id is the [1] element

			elif file == "followers.csv":
				# header check
				if head_flags[1] == 0:
					r.write(lines[0])
					head_flags[1] = 1
				# id check
				for line in lines[1:]:
					if int(line.split(",")[1].replace('"','')) in list_of_ids:
						r.write(line)

			elif file == "friends.csv":
				if head_flags[2] == 0:
					r.write(lines[0])
					head_flags[2] = 1
				for line in lines[1:]:
					if int(line.split(",")[0].strip('"')) in list_of_ids:
						r.write(line)

			elif file == "tweets.csv":
				if head_flags[3] == 0:
					r.write(lines[0])
					head_flags[3] = 1
				for line in lines[1:]:
					line = line.replace(',,',',"",') 
					if int(line.split('","')[4]) in list_of_ids:
						r.write(line)
			f.close()
			r.close()

if(__name__ == "__main__"):
	HUM_creator("../data/E13/","../data/TFP/","../data/HUM/")
	#FAK_creator("../data/FSF/","../data/INT/","../data/TWT/","../data/FAK/")
	#BAS_creator("../data/HUM/","../data/FAK/","../data/BAS/")