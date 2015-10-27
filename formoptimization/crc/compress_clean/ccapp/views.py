from django.shortcuts import render
CODE_PATH='$HOME/DocumentsGitHub/dataacquisition/formoptimization/crc'
import sys
sys.path.append(CODE_PATH)
#from tests import get_tree_json

def home(request):
	return render(request,'ccapp/home.html')

def viewtree(request):#,cutoff,threshold,data_file,clustering_func,num_groups):
	tempdict={}
	tempdict['cutoff']=request.POST['cutoff_input']
	tempdict['th']=request.POST['threshold_input']
	tempdict['file_']=request.POST['file_input']
	tempdict['cluster']=request.POST['clustering_input']
	tempdict['groups']=request.POST['groups_input']
	#json=get_tree_json(eval(tempdict['file_']),eval(tempdict['th']),eval(tempdict['cutoff']),eval(tempdict['cluster']),eval(tempdict['groups']))
	return render(request,'ccapp/viewtree.html',tempdict)
# Create your views here.
