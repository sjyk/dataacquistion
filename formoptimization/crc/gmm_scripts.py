import numpy as np
from sklearn import mixture

class gmm_stuff:
	def __init__(self,n_comp=2):
		self.g = mixture.GMM(n_components=n_comp)

	def fit(self,data):
		data_=map(lambda x:x.item if isinstance(x,Tree) else x,data)
		self.g.fit(data_)

	def predict(self,data):
		predictions=list(self.g.predict([x.item if isinstance(x,Tree) else x for x in data]))
		return zip(data,predictions)

	