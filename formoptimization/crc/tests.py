"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

# from django.test import TestCase
import csv
from R_to_V import *
import numpy as np

FILENAME='CRC_Survey Monkey_Data.csv'
SHANNON_FILENAME='shannon.txt'
RANK_FILENAME='rank.txt'
# class SimpleTest(TestCase):
#     def test_basic_addition(self):
#         """
#         Tests that 1 + 1 always equals 2.
#         """
#         self.assertEqual(1 + 1, 2)

def test_shannon_entropy():
	result_file=open(SHANNON_FILENAME,'wb')
	with open(FILENAME,'rb') as csvfile:
		print SHANNON_FILENAME
		reader=csv.reader(csvfile,delimiter=',',quotechar='"')
		i=0
		for row in reader:
			i+=1
			if i<3:
				continue
			row_string=" ".join(row)
			R=gen_R(row_string)
			V=gen_V_lda(R)
			HR=get_shannon_entropy(R)
			HV=get_shannon_entropy(V)
			Hx=np.sum(HR-HV)

			print Hx
			result_file.write(str(Hx)+"\n")

def test_rank():
	result_file=open(RANK_FILENAME,'wb')
	with open(FILENAME,'rb') as csvfile:
		reader=csv.reader(csvfile,delimiter=',',quotechar='"')
		i=0
		for row in reader:
			i+=1
			if i<3:
				continue
			row_string=" ".join(row)
			R=gen_R(row_string)
			V=gen_V_lda(R)
			rank_r=get_rank(R)
			rank_v=get_rank(V)
			rank=rank_r-rank_v
			
			result_file.write(str(rank)+"\n")




