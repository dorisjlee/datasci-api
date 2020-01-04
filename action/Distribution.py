'''
Gets a measure of skewness of the distributions of all measures
'''
def distribution(dobj):
	# Enumerate --> compute the scores for each item in the collection 
	# -->  return DataObjectCollection with the scores 
	import scipy.stats
	import numpy as np
	dobj.recommendation = {"action":"Distribution",
						   "description":"Show univariate count distributions of different attributes in the dataset."}
	vizCollection = dobj.compiled.collection
	for obj in vizCollection:
		measure = obj.getObjByDataModel("measure")[0]
		msr = measure.columnName
		msrVals = list(obj.dataset.df[msr])
		obj.score = np.abs(scipy.stats.skew(msrVals))
	dobj.compiled.sort()
	dobj.recommendation["collection"] = dobj.compiled