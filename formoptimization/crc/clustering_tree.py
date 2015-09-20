import ete2
import math
from R_to_V import *
# import numpy as np

def get_tree(data,clustering_func,threshold=lambda x:x<=0,cutoff=lambda x:len(x)<=1,num_groups=lambda groups:int(math.ceil(len(groups)/4.0))):
	curr_trees=[]
	return_dict={}
	level_dict={}
	curr_char=chr(ord('A')-1)
	for datum in data:
		curr_char_val=ord(curr_char[-1])
		if curr_char_val==122:
			curr_char+='A'
		else:
			curr_char_val+=1
			curr_char=curr_char[:-1]+chr(curr_char_val)
		return_dict[curr_char]=datum
		curr_trees.append(Tree(datum,node_name=curr_char))
	level=0
	while not cutoff(curr_trees):#set stop depth with function
		clustered=perform_clustering(curr_trees,clustering_func,threshold,num_groups)
		curr_trees=[]
		#print clustered[0]
		removed_words=[]
		level_dict[level]=[]
		for group in clustered:
			subtrees=[]
			for doc in group:
				subtrees.append(doc)

			intersect=intersection(group,len(clustered))
			if intersect==None:
				continue
			lost=intersect[1]
			intersect=intersect[0]
			curr_char_val=ord(curr_char[-1])
			if curr_char_val==122:
				curr_char+='A'
			else:
				curr_char_val+=1
				curr_char=curr_char[:-1]+chr(curr_char_val)
			level_dict[level].append(lost)
			return_dict[curr_char]=intersect
			curr_trees.append(Tree(intersect,subtree=subtrees,node_name=curr_char,lost_vals=lost))
		level+=1
	return curr_trees[0],return_dict,level_dict


def perform_clustering(groups,clustering_func,threshold=lambda x:x<=0,num_groups=lambda groups:int(math.ceil(len(groups)/4.0))):
	return clustering_func(groups,threshold,num_groups=num_groups)


def intersection(group,cluster_size):
	temp_dict={}
	if len(group)==1 and cluster_size!=1:
		return None
	for item in group:
		if isinstance(item,Tree):
			for word in item.item:
				if word not in temp_dict:
					temp_dict[word]=0
				temp_dict[word]+=1
		else:
			for word in item:
				if word not in temp_dict:
					temp_dict[word]=0
				temp_dict[word]+=1
	group_size=len(group)
	intersection_words=[item  for item in temp_dict if temp_dict[item]>=group_size]
	lost_words=[item for item in temp_dict if temp_dict[item]<group_size]
	# return apply_update(group,intersection_words)
	return intersection_words,lost_words

def apply_update(group,words):
	new_group=[]
	for item in group:
		new_group.append(item.update(words))
	return new_group

def make_newick(treeobject):
	if treeobject.subtrees==None:
		i=0
		duplicate=str(treeobject.node_name)
		# while i<len(duplicate):
		# 	if duplicate[i]==')':
		# 		duplicate.insert(i,'\\')
		# 		i+=1
		# 	elif dublicate[i]=='(':
		# 		dublicate.insert(i,'\\')
		# 		i+=1
		# 	i+=1
		return duplicate
	tempstring=''
	first=True
	for treeobj in treeobject.subtrees:
		comma=','
		if first:
			comma=''
			first=False
		tempstring+=comma+make_newick(treeobj)

	return '('+tempstring+')'+str(treeobject.node_name)

class Tree:
	def __init__(self,entry,subtree=None,node_name='',lost_vals=None):
		if isinstance(entry,Tree):
			self=entry
		else:
			self.item=entry
			self.subtrees=subtree
			self.node_name=node_name
			self.lost_vals=lost_vals

	# def __str__(self):	
	# 	tempstring=''
	# 	printlist=[self]
	# 	while printlist!=[]:
	# 		to_add=[]
	# 		for item in printlist:
	# 			to_add.extend(item.subtrees)
	# 			tempstring+=item.item+','
	# 		tempstring+='\n'
	# 		printlist=to_add
	# 	return tempstring

	# def __repr__(self):
	# 	tempstring=''
	# 	printlist=[self]
	# 	while printlist!=[]:
	# 		to_add=[]
	# 		for item in printlist:
	# 			to_add.extend(item.subtrees)
	# 			tempstring+=item.item+','
	# 		tempstring+='\n'
	# 		printlist=to_add
	# 	return tempstring

	def __str__(self):
		return str(self.item)

	def __repr__(self):
		return str(self.item)

	def visualize(self,savepath='tree.txt',write_perm='False'):
		newick=make_newick(self)+';'
		self.newick=ete2.Tree(newick,format=8)
		print self.newick
		if write_perm:
			f=open(savepath,'w')
			f.write(str(self.newick))
			f.close()

	def save_tree_to_file(self,filepath):
		newick=make_newick(self)+';'
		# countleft=0
		# countright=0
		# for char in newick:
		# 	if char=='(':
		# 		countleft+=1
		# 	elif char==')':
		# 		countright+=1
		# print countleft,' ',countright
		print newick
		self.newick=ete2.Tree(newick,format=8)
		ts=ete2.TreeStyle()
		ts.rotation=90
		#self.newick.show(tree_style=ts)
		self.newick.render(filepath,w=500,tree_style=ts)
		print self.newick

	def render_tree(self):
		newick=make_newick(self)+';'
		# countleft=0
		# countright=0
		# for char in newick:
		# 	if char=='(':
		# 		countleft+=1
		# 	elif char==')':
		# 		countright+=1
		# print countleft,' ',countright
		# print newick
		self.newick=ete2.Tree(newick,format=8)
		ts=ete2.TreeStyle()
		ts.rotation=90
		#self.newick.show(tree_style=ts)
		self.newick.show(tree_style=ts)

	def update(self,words):
		toreturn=[]
		for word in words:
			i=0
			while i<len(self.item):
				if self.item[i:i+len(word)]==word:
					toreturn.append((i,word))
					i+=len(word)
				else:
					i+=1
		sorted_return=sorted(toreturn,key=lambda x:x[0])
		found_ones=[]
		i=0
		while i<len(sorted_return):
			indice=thing[0]
			x=1
			new_thing=thing[1]
			found=1
			while sorted_return[i+x][0]==indice:
				if len(sorted_return[i+x][1])>len(new_thing):
					new_thing=sorted_return[i+x][1]
					found=x
				x+=1
			found_ones.append(new_thing)
			i+=x
		self.item=' '.join([x[1] for x in found_ones])



	
	


