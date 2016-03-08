import sys
import ete2
def render_tree(name,format=8):
	t=ete2.Tree(name,format)
	ts=ete2.TreeStyle()
	ts.rotation=90
	t.show(tree_style=ts)

if __name__=='__main__':
	if len(sys.argv)!=2:
		print 'please put a file as second commandline argument'
	fname=sys.argv[1]
	render_tree(fname)