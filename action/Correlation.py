'''
Correlation between measure variables
'''
def correlation(dobj):
	# Enumerate --> compute the scores for each item in the collection 
	# -->  return DataObjectCollection with the scores 
	import scipy.stats
	import numpy as np
	# TODO: need to make this work for DataObject (when input is not collection and just a single DataObject)
	for obj in dobj.compiled.collection:
	    measures = obj.getObjByDataModel("measure")
	    if len(measures)<2 : raise ValueError(f"Can not compute correlation between {[x.columnName for x in obj.spec]} since less than 2 measure values present.")
	    msr1 = measures[0].columnName
	    msr2 = measures[1].columnName

	    msr1Vals = list(obj.dataset.df[msr1])
	    msr2Vals = list(obj.dataset.df[msr2])
	    
	    obj.score = np.abs(scipy.stats.pearsonr(msr1Vals,msr2Vals)[0])