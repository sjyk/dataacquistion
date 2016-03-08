import pickle
import json
from TSC_tests import make_plots

our_tree=pickle.load(open('ed_tsc_params_tree.pkl','rb'))

kinematics=pickle.load(open('ed_tsc_params_kinematics.pkl','rb'))
node_dict=json.load(open('ed_tsc_params.json','r'))

gthresh=-15
ethresh=-20

make_plots(our_tree,node_dict,kinematics,gthresh,ethresh)
