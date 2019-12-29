from dataObj.dataObj import DataObj
from interestingness.valueBasedInterestingness import valueBasedInterestingness
'''
Shows possible visualizations when one attribute or filter from the current context is removed
'''
def generalize(dobj):
	# takes in a dataObject and generates a list of new dataObjects, each with a single measure from the original object removed
	# -->  return list of dataObjects with corresponding interestingness scores 
	import scipy.stats
	import numpy as np
	# TODO: need to make this work for DataObject (when input is not collection and just a single DataObject)

	vizCollection = dobj.compiled.collection
	#list that will contain the DataObjs to be returned in the output
	outputDataCollection = []
	#list to keep track of columns already included in the output (ensure no repeat graphs)
	columnNames = []
	for obj in vizCollection:
		measures = obj.getObjByDataModel("measure")
		if len(measures) > 1:
			for measure in measures:
				tempDataObj = DataObj(obj.dataset, obj.spec)
				tempDataObj.removeColumnFromSpec(measure.columnName)
				if len(tempDataObj.spec) > 0 and tempDataObj.spec[0].columnName not in columnNames:
					tempDataObj.score = valueBasedInterestingness(tempDataObj)
					outputDataCollection.append(tempDataObj)
					columnNames.append(tempDataObj.spec[0].columnName)
	return(outputDataCollection)