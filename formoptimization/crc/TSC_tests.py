import pickle
import clustering_tree as tree_gen
import clustering_funcs as funcs
import random
import json

TSC_PICKLE='tscdl_data.p'

def test_option_1a():

	data = pickle.load(open(TSC_PICKLE, "rb"))
	keys=data.keys()
	all_demos=[]
	for key in keys:
		LOOCV_demo=data[key]
		demo=random.choice(LOOCV_demo)
		demo=map(lambda x:x[-1],demo)
		all_demos.append(demo)

	bin_intersect=lambda x,y:tree_gen.LCS_binary_intersect(x,y)
	our_tree,node_dict,lost_dict=tree_gen.get_tree(all_demos,funcs.binary_segmentation_cluster,intersect_meth=bin_intersect)
	
	with open('1a.json','w') as f:
		json.dump(node_dict,f)
		f.close()

	our_tree.render_tree()

def test_ed_tsc():
	data = pickle.load(open(TSC_PICKLE, "rb"))
	keys=data.keys()
	all_demos=[]
	for key in keys:
		LOOCV_demo=data[key]
		demo=random.choice(LOOCV_demo)
		demo=map(lambda x:x[-1],demo)
		all_demos.append(demo)

	intersect=lambda x,y:tree_gen.LCS_intersect(x,y)
	our_tree,node_dict,lost_dict=tree_gen.get_tree(all_demos,funcs.relational_cluster,intersect_meth=intersect)
	
	with open('1a.json','w') as f:
		json.dump(node_dict,f)
		f.close()

	our_tree.render_tree()

if __name__=='__main__':
	test_ed_tsc()