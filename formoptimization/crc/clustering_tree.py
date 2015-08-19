

def get_tree(data,clustering_func):
	curr_trees=[]
	for datum in data:
		new_data_list.append(Tree(datum))
	while len(curr_trees)>1:
		clustered=perform_clustering(curr_trees,clustering_func)
		curr_trees=[]
		for group in clustered:
			subtrees=[]
			for doc in group:
				subtrees.append(doc)

			intersect=intersection(group)
			curr_trees.append(Tree(intersect,subtrees))
	return curr_trees[0]



def perform_clustering(groups,clustering_func):
	return clustering_func(groups)


def intersection(group):
	temp_dict={}
	for item in group:
		for word in item.item:
			if word not in temp_dict:
				temp_dict[word]=0
			temp_dict[word]+=1
			group_size=len(group)
	return [item  for item in temp_dict if temp_dict[item]>=group_size]

class Tree:
	def __init__(self,entry,subtree=None):
		if isinstance(entry,Tree):
			self=entry
		else:
			self.item=entry
			self.subtrees=subtree

	def __str__(self):	
		tempstring=''
		printlist=[self]
		while printlist!=[]:
			to_add=[]
			for item in printlist:
				to_add.extend(item.subtrees)
				tempstring+=item.item+','
			tempstring+='\n'
			printlist=to_add
		return tempstring

	def __repr__(self):
		tempstring=''
		printlist=[self]
		while printlist!=[]:
			to_add=[]
			for item in printlist:
				to_add.extend(item.subtrees)
				tempstring+=item.item+','
			tempstring+='\n'
			printlist=to_add
		return tempstring


