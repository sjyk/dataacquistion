import pickle
import clustering_tree as tree_gen
import clustering_funcs as funcs
import random
import json
import matplotlib.pyplot as plt
import pickle
import numpy as np
import os
import IPython
import sys
sys.path.insert(0,'../../../sim/consumable-irl/tsc/')
import tsc

BASE_PATH='../../../sim/consumable-irl/Results/gridworld2/'
TSC_PICKLE='tscdl_data.p'
true_seq=["start->1","1->5","5->2","2->3","3->6","6->4","4->2","3->6","6->4","4->2","3->6","6->4","4->2",
			"3->6","6->4","4->2","2->3","3->6","6->11","11->end"]

def test_option_1a():

	data = pickle.load(open(TSC_PICKLE, "rb"))
	keys=data.keys()
	all_demos=[]
	for key in keys:
		LOOCV_demo=data[key]
		# demo=random.choice(LOOCV_demo)
		demo=LOOCV_demo[0]
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
	
	with open('ed_tsc.json','w') as f:
		json.dump(node_dict,f)
		f.close()

	our_tree.render_tree()


def test_ed_tsc_on_params(gthresh,ethresh):
	data = pickle.load(open(TSC_PICKLE, "rb"))
	keys=data.keys()
	# all_demos=[]
	# name_list=[]
	# kinematics={}
	# for key in keys:
	# 	LOOCV_demo=data[key]
	# 	demo=random.choice(LOOCV_demo)
	# 	demo=map(lambda x:x[-1],demo)
	# 	all_demos.append(demo)
	# 	name_list.append(str(key))
	# 	kinematics[key]=(parse_kinematics(key))
	# all_demos,name_list,kinematics=TScluster_blocks_experiment()
	all_demos=json.load(open('block_segmentations.json','rb'))
	name_list=json.load(open('block_segmentations_names.json','rb'))
	kinematics=json.load(open('block_segmentations_kine.json','rb'))


	intersect=lambda x,y:tree_gen.LCS_intersect(x,y)
	clusterer=lambda x,y,num_groups:funcs.relational_cluster(x,y,num_groups=num_groups,group_thresh=gthresh,element_thresh=ethresh)

	our_tree,node_dict,lost_dict=tree_gen.get_tree(all_demos,clusterer,intersect_meth=intersect,names=name_list)
	
	with open('ed_tsc_params.json','w') as f:
		json.dump(node_dict,f)
		f.close()
	with open('ed_tsc_params_tree.pkl','wb') as f:
		pickle.dump(our_tree,f)
	with open('ed_tsc_params_kinematics.pkl','wb') as f:
		pickle.dump(kinematics,f)
	make_plots(our_tree,node_dict,kinematics,gthresh,ethresh)

	our_tree.render_tree()	

def parse_kinematics(demo):
	fname='kinematics/'+str(demo)+'.txt'
	rtn={}
	for i in range(76):
		rtn[i]=[]
	with open(fname,'r') as f:
		for line in f:
			tempy=line.split()
			for i,x in enumerate(tempy):
				rtn[i].append(x)

	return rtn

def make_plots(tree,node_dict,kinematics,gthresh,ethresh):
	name_tree=extract_experiments_of_cluster(tree,node_dict)
	stack=[name_tree]
	while stack:
		new_=[]
		for node in stack:
			print node.node_name
			# plot_all(node.item,kinematics,[39,40,41],node.node_name,gthresh,ethresh)
			plot_all(node.item,kinematics,[0,1],node.node_name,gthresh,ethresh)
			if node.subtrees:
				new_+=node.subtrees
		stack=new_

def plot_all(demos,kinematics,feats_to_sample,node_name,gthresh,ethresh):
	directory='plots/'+str(gthresh)+'_'+str(ethresh)+'/'
	if not os.path.exists(directory):
		os.makedirs(directory)
	fig,axes=plt.subplots(len(feats_to_sample),sharex=True)
	linelist=[]
	for key in demos:
		# print key
		datalist=kinematics[key]
		# print (datalist[0])
		if len(feats_to_sample)>1:
			for z,feat_index in enumerate(feats_to_sample):
				list_=datalist[feat_index-1]
				l,=axes[z].plot(list(range(len(list_))),list_)
				if z==0:
					linelist.append(l)
		else:
			list_=datalist[feats_to_sample[0]-1]
			axes.plot(list(range(len(list_))),list_)
	fig.legend(linelist,demos,'upper right')
	axes[0].set_title('X position versus time')
	axes[1].set_title('Y position versus time')
	axes[2].set_title('Z position versus time')
	fig.subplots_adjust(hspace=.5)
	plt.savefig(directory+str(node_name)+'.png',dpi=fig.get_dpi()*5)
	plt.close('all')


def extract_experiments_of_cluster(tree,node_dict):
	if not tree.subtrees:
		# print node_dict[tree.node_name]
		return tree_gen.Tree([node_dict[tree.node_name][0]],node_name=tree.node_name)
	vals=[]
	subtrees=[]
	for child in tree.subtrees:
		temp=extract_experiments_of_cluster(child,node_dict)
		subtrees.append(temp)
		vals+=temp.item
	return tree_gen.Tree(vals,subtree=subtrees,node_name=tree.node_name)


def param_sweep_tsc(true_length,num_trials):
	data = pickle.load(open(TSC_PICKLE, "rb"))
	keys=data.keys()
	all_demos=[]
	for key in keys:
		LOOCV_demo=data[key]
		demo=random.choice(LOOCV_demo)
		demo=map(lambda x:x[-1],demo)
		all_demos.append(demo)

	intersect=lambda x,y:tree_gen.LCS_intersect(x,y)
	thresh=[-25,-22.5,-20,-17.5,-15,-12.5,-10,-5,-2.5]
	options={
		    -25:0,
		    -22.5:1,
		    -20:2,
		    -17.5:3,
		    -15:4,
		    -12.5:5,
		    -10:6,
		    -5:7,
		    -2.5:8
		}
	overall_error_dict={}
	for i in range(num_trials):
		avg_error_dict={}
		for gthresh in thresh:
			for ethresh in thresh:
				print i, gthresh,ethresh
				clusterer=lambda x,y,num_groups:funcs.relational_cluster(x,y,num_groups=num_groups,group_thresh=gthresh,element_thresh=ethresh)
				our_tree,node_dict,lost_dict=tree_gen.get_tree(all_demos,clusterer,intersect_meth=intersect)
				error_level=[]
				avg_=get_errors(our_tree,error_level,true_length)
				if i==0:
					overall_error_dict[(gthresh,ethresh)]=avg_/num_trials
				else:
					overall_error_dict[(gthresh,ethresh)]+=avg_/num_trials

				avg_error_dict[(gthresh,ethresh)]=avg_
				plt.figure()
				plt.plot(xrange(len(error_level)),error_level,'ro')
				plt.axis([-1,len(error_level)+1,min(error_level)-1,max(error_level)+1])
				plt.suptitle('group threshold, element thresh='+str(gthresh)+', '+str(ethresh))
				plt.savefig('plots/'+str(gthresh)+'_'+str(ethresh)+'_'+str(i+1)+'.png')
				# plt.show()


		keylist=avg_error_dict.keys()

		mat=np.zeros((9,9))
		
		for key in keylist:
		    g=options[key[0]]
		    e=options[key[1]]
		    mat[g,e]=avg_error_dict[key]
		plt.figure()
		plt.imshow(mat,interpolation='spline36',origin='Lower')
		plt.colorbar()
		labels=[-25,-22.5,-20,-17.5,-15,-12.5,-10,-5,-2.5]
		# labels=list(reversed(labels))
		tick_marks = np.arange(len(labels))
		plt.xticks(tick_marks, labels)
		plt.yticks(tick_marks, labels)
		plt.ylabel('group threshold')
		plt.xlabel('element threshold')
		plt.tight_layout()
		plt.savefig('plots/Avg_error_of_parameters_'+str(i+1)+'.png')
		# plt.show()
	keylist=overall_error_dict.keys()

	mat=np.zeros((9,9))
	
	for key in keylist:
	    g=options[key[0]]
	    e=options[key[1]]
	    mat[g,e]=avg_error_dict[key]
	plt.figure()
	plt.imshow(mat,interpolation='spline36',origin='Lower')
	plt.colorbar()
	labels=[-25,-22.5,-20,-17.5,-15,-12.5,-10,-5,-2.5]
	# labels=list(reversed(labels))
	tick_marks = np.arange(len(labels))
	plt.xticks(tick_marks, labels)
	plt.yticks(tick_marks, labels)
	plt.ylabel('group threshold')
	plt.xlabel('element threshold')
	plt.tight_layout()
	plt.savefig('plots/Overall_Avg_error_of_parameters.png')


def get_errors(root,lvl_list,length):
	stack=[root]
	avg_=0
	num_=0
	while stack:
		if stack[0].node_name=='0_unrooted':
			stack=stack[0].subtrees
			continue
		new_level=[]
		sum_=0
		tempnum=0
		for tree in stack:
			tempnum+=1
			children=tree.subtrees
			# print tree
			# print children
			if children:
				new_level+=children
			if isinstance(length,int):
				diff=abs(len(tree.item)-length)
			else:
				diff=funcs.edit_distance(tree,tree_gen.Tree(length))
			avg_+=diff
			sum_+=diff
		num_+=tempnum
		sum_=sum_/tempnum
		lvl_list.append(sum_)
		stack=new_level
	return avg_/num_

def parse_json(path):
	experiment=json.load(open(path,'rb'))
	steps=map(lambda x:map(lambda y:np.array(map(eval,y)),x),experiment['all_steps'])
	walls=experiment['walls']
	return steps,walls

def matrixfy(nest_):
	return map(lambda x:(lambda y:np.array(y),x),nest_)

def TScluster_blocks_experiment():
	filelist=[]
	#iterate through the directories here
	# print os.listdir(BASE_PATH)
	for i in os.listdir(BASE_PATH):
		if os.path.isdir(BASE_PATH+i):
			for x in os.listdir(BASE_PATH+i):
				if x.endswith(".json"):
					filelist.append(BASE_PATH+i+'/'+x)
	# print filelist
	alllist=[]
	print filelist
	for jfile in filelist:
		# print jfile
		steps,walls=parse_json(jfile)
		# steps=map(lambda x:(x,walls),steps)
		alllist.append((walls,steps))
	transitions=tsc.TransitionStateClustering(window_size=3)
	walltype=[]
	i=0
	kinematics={}
	name_list=[]
	for walls in alllist:
		x=0
		
		for index in random.sample(range(len(walls[1])),len(walls[1])*2/10):
			demo=walls[1][index]
			d=random.choice(range(len(demo)))
			"""this is because for some reason index 4 was complete garbage, no idea how it got added"""
			transitions.addDemonstration(np.delete(demo[d],4,1))
			# walltype.append(i)
			# print i,len(filelist)
			key=filelist[i]+'_'+str(index)+'_'+str(d)
			kinematics[key]={}
			sub=0
			for z in range(demo[d].shape[-1]):
				y=z+sub
				if z==4:
					sub-=1
					continue
				kinematics[key][y]=demo[d][:,y].ravel().tolist()
				name_list.append(key)
			x+=1
		i+=1

	transitions.fit(pruning=0)
	
	rtn=[[] for x in range(len(name_list))]
	for transition in transitions.task_segmentation:
		# wall=walltype[transition[0]]
		rtn[transition[0]].append(transition[2])

	return rtn,name_list,kinematics

if __name__=='__main__':
	test_ed_tsc_on_params(-15,-20)
	# param_sweep_tsc(true_seq,1)