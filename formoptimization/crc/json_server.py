import Flask
import tests

@app.route('/compressclean/gettreejson')
def our_webservice():
	file_name=request.args.get('file')
	cutoff_func=request.args.get('cutoff')
	threshold=request.args.get('threshold')
	group_func=request.args.get('group_func')
	return tests.gettreejson(file_name,cutoff_func,threshold,group_func)