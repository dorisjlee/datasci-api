'''
Gets a measure of skewness of the distributions of all measures
'''
def distribution(dobj):
	# Enumerate --> compute the scores for each item in the collection 
	# -->  return DataObjectCollection with the scores 
	import scipy.stats
	import numpy as np
	# TODO: need to make this work for DataObject (when input is not collection and just a single DataObject)
	vizCollection = dobj.compiled.collection
	for obj in vizCollection:
		measure = obj.getObjByDataModel("measure")[0]
		msr = measure.columnName
		
		msrVals = list(obj.dataset.df[msr])
		obj.score = np.abs(scipy.stats.skew(msrVals))