
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

# from django.test import TestCase
import csv
from R_to_V import *
import numpy as np
from clustering_tree import get_tree
from ete2 import Tree,TreeStyle
from clustering_funcs import cluster_spectral_k_means
import random
import json
import math
import collections
import matplotlib
# matplotlib.use('Agg')
import matplotlib.pyplot as plt
from gensim import corpora, models, similarities
from gensim.models import ldamodel

FILENAME='CRC_Survey Monkey_Data.csv'
SHANNON_FILENAME='shannon.txt'
RANK_FILENAME='rank.txt'
TREE_IMG_FILENAME='temptree.png'
NODE_DICT_FILENAME='tempnodedict.json'
LOST_DICT_FILENAME='templostdict.json'

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

def test_tree_clustering():
	result_file=open(TREE_IMG_FILENAME,'wb')
	p=16.0/600.0
	with open(FILENAME,'rb') as csvfile:
		reader=csv.reader(csvfile,delimiter=',',quotechar='"')
		i=0
		row_list=[]
		for row in reader:
			# if random.random()<=p:
			#  	row_string=' '.join(row)
			#  	row_list.append(row_string)
			#  	i+=1
			#  	if i==16:
			#  		break
			i+=1
			# if i>256:
			# 	break
			if i<3:
				continue
			row_string=" ".join(row)
			row_list.append(row_string)
	our_tree,node_dict,lost_dict=get_tree(row_list,cluster_spectral_k_means)
	# our_tree.save_tree_to_file(TREE_IMG_FILENAME)
	with open(NODE_DICT_FILENAME,'w') as f:
		json.dump(node_dict,f)
		f.close()

	with open(LOST_DICT_FILENAME,'w') as f:
		json.dump(lost_dict,f)
		f.close()
	our_tree.render_tree()

def get_tree_json(filename=FILENAME,cutoff='lambda x:len(x)<=1',threshold='lambda x:x<=0',gf='lambda groups:int(-(-len(groups)//4.0))'):
	with open(filename,'rb') as f:
		reader=csv.reader(f,delimiter=',',quotechar='"')
		i=0
		row_list=[]
		for row in reader:
			if i==0 or i==1:
				i+=1
				continue
			if row[16]=='':
				continue
			row_string=' '.join(row[16])
			row_list.append(row[16])
	our_tree,node_dict,lost_dict=get_tree(row_list,cluster_spectral_k_means,threshold=eval(threshold),cutoff=eval(cutoff),num_groups=eval(gf))
	json_=our_tree.return_json()	
	tempdict={}
	# tempdict['lost']=lost_dict
	# tempdict['tree']=json_
	with open(LOST_DICT_FILENAME,'w') as f:
		json.dump(lost_dict,f)
		f.close()
	with open('THE_TREE.json','w') as f:
		json.dump(json_,f)
		f.close()
	# return json.dumps(tempdict)

def introduce_error(data,error_dict):
	return_data=[]
	for data_point in data:
		temp_data=''
		for word in delimit_source(data_point,''):
			if word in error_dict and random.Random()<error_dict[word][0]:
				temp_data+=error_dict[word][1]
			else:
				temp_data+=word+' '
		return_data.append(temp_data.rstrip())
	return return_data

def tag(tree_):
	rtn_={}
	forest=[tree_]
	i=0
	while forest!=[]:
		i+=1
		# rtn_[i]={}
		templist=[]
		for shrub in forest:
			if not shrub.subtrees:
				continue
			templist+=shrub.subtrees
			# rtn_[i][shrub]=perform_lda(shrub)
		rtn_[i]=perform_lda(templist)
		forest=templist
	return rtn_


def perform_lda(tree_list):
	documents=[]
	rtn_={}
	for tree_ in tree_list:
		rtn_[tree_]={}
		if not tree_.item:
			continue
		documents.append(tree_.item)

	if documents==[]:
		return rtn_
	texts = [[word for word in document.lower().split()] for document in documents]
	texts = [[word for word in text] for text in texts]
	dictionary = corpora.Dictionary(texts)
	# corpus=[dictionary.doc2bow(text) for text in texts]
	corpus=[]

	id2word = {}
	for word in dictionary.token2id:    
		id2word[dictionary.token2id[word]] = word	

	test_lda = ldamodel.LdaModel(corpus,num_topics=20, id2word=id2word,minimum_probability=0)
	# test_lda[dictionary.doc2bow('human system')]
	for tree_ in tree_list:
		t_list=test_lda[dictionary.doc2bow([word for word in tree_.item.lower().split()])]
		# rtn_[tree_]=
		for tag,prob in t_list:
			rtn_[tree_][tag]=prob
	# content=tree_.item
	# R=gen_R(content)
	return rtn_

def get_tag_distritbution(tag_set):
	rtn_={}
	for k,v in tag_set.items():
		rtn_[k]=collections.defaultdict(float)
		for tree_ in v:
			distro=v[tree_]
			for tag in distro:
				rtn_[k][tag]+=distro[tag]
	for k,v in rtn_.items():
		sum_=0
		for tag in v:
			sum_+=v[tag]
		for tag in v:
			rtn_[k][tag]/=sum_
	return rtn_

def get_distro_error(clean,dirty):
	error_={}
	for k,distro in dirty.items():
		other_=clean[k]
		tags_=get_all(other_,distro)
		sum_=0
		for tag in tags_:
			sum_+=(other_[tag]-distro[tag])**2
		error_[k]=sum_
	return error_

def get_all(other_,distro):
	rtn=set()
	for key in other_:
		rtn.add(key)
	for key in distro:
		rtn.add(key)
	return rtn

def get_variance(distro,lvl1,lvl2):

	i=0
	v1=0
	v2=0
	while i<=max(lvl1,lvl2):
		if i==lvl1:
			L=[]
			x=0
			avg=0
			for k,v in distro[i].items():
				L.append(v)
				avg+=v*x
				x+=1
			for j,item in enumerate(L):
				v1+=item*(j-avg)**2
		elif i==lvl2:
			L=[]
			x=0
			avg=0
			for k,v in distro[i].items():
				L.append(v)
				avg+=v*x
				x+=1
		
			for j,item in enumerate(L):
				v2+=item*(j-avg)**2
		i+=1
	return v1,v2


def error_tests(filename,error_dict):
	filename=FILENAME
	with open(filename,'rb') as f:
		reader=csv.reader(f,delimiter=',',quotechar='"')
		i=0
		row_list=[]
		for row in reader:
			if i==0 or i==1:
				i+=1
				continue
			# # if row[16]=='':
			# # 	continue
			# row_string=' '.join(row)
			# row_list.append(row_string)
			if row[16]=='':
				continue
			row_string=' '.join(row[16])
			row_list.append(row[16])
	dirty_row_list=introduce_error(row_list,error_dict)
	print 'error added'
	our_tree,node_dict,lost_dict=get_tree(row_list,cluster_spectral_k_means)
	print 'made clean tree'
	dirty_tree,dirty_node_dict,dirty_lost_dict=get_tree(dirty_row_list,cluster_spectral_k_means)
	print 'made dirty tree'
	clean_tags=tag(our_tree)
	print 'tagged clean'
	dirty_tags=tag(dirty_tree)
	print 'tagged dirty'
	clean_distro=get_tag_distritbution(clean_tags)
	print 'clean distro finished'
	dirty_distro=get_tag_distritbution(dirty_tags)
	print 'dirty distro finished'
	error=get_distro_error(clean_distro,dirty_distro)
	print 'error distro finished'
	plot_error(error)
	print 'done'

def plot_error(distro):
	
	x=[]
	y=[]
	for k,v in distro.items():
		x.append((k))
		y.append(v)

	plt.plot(x,y)
	# plt.show()
	plt.savefig('no_error.png')


def find_error_propagation(tree,error_dict):
	error_list=[error_dict[k][1] for k in error_dict]
	curr_nodes=[tree]
	i=0
	rtn_dict={}
	while curr_nodes!=[]:
		new_level=[]
		for tree in curr_nodes:
			new_level+=tree.subtrees
			for item in error_list:
				if item in tree.item:
					rtn_dict[item]=i
					error_list.remove(item)
		curr_nodes=new_level
		i+=1
	return i,rtn_dict

if __name__=='__main__':
	# test_tree_clustering()
	# error_tests('',{'schools':(0.20,'scools'),'school':(0.20,'scool'),'water':(.3,'warte')})
	error_tests('',{})
	




