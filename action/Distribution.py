'''
Gets a measure of skewness of the distributions of all measures
'''
def distribution(dobj,ignoreIdentity=True,ignoreTranspose=True):
	# Enumerate --> compute the scores for each item in the collection 
	# -->  return DataObjectCollection with the scores 
	import scipy.stats
	import numpy as np
	# TODO: need to make this work for DataObject (when input is not collection and just a single DataObject)
	vizCollection = dobj.compiled.collection
	if (ignoreIdentity): vizCollection =  filter(lambda x: x.spec[0].columnName!=x.spec[1].columnName,dobj.compiled.collection)
	def checkTransposeNotComputed(dobj,a,b):
		transposeExist = list(filter(lambda x:(x.spec[0].columnName==b) and (x.spec[1].columnName==a),dobj.compiled.collection))
		if (len(transposeExist)>0):
			return transposeExist[0].score==-1
		else:
			return False
	for obj in vizCollection:
		measure = obj.getObjByDataModel("measure")
		msr = measures.columnName
		
		msrVals = list(obj.dataset.df[msr])
		obj.score = np.abs(scipy.stats.skew(msrVals))