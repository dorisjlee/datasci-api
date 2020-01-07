from dataObj.dataObj import DataObj
from dataObj.dataObj import Row
from dataObj.dataObj import Column

from dataObj.DataObjCollection import DataObjCollection
from interestingness.valueBasedInterestingness import valueBasedInterestingness
import pandas as pd
'''
Shows possible visualizations when filtered by categorical variables in the data object's dataset
'''
def filter(dobj):
	filters = dobj.getObjByRowColType("Row")
	output = []
	#if Row is specified, create visualizations where data is filtered by all values of the Row's categorical variable 
	if len(filters) > 0:
		columnSpec = dobj.getObjByRowColType("Column")
		#get unique values for all categorical values specified and creates corresponding filters
		for row in filters:
			uniqueValues = dobj.dataset.df[row.fAttribute].unique()
			#creates new data objects with new filters
			for i in range(0, len(uniqueValues)):
				newSpec = columnSpec.copy()
				newFilter = Row(fAttribute = row.fAttribute, fVal = uniqueValues[i])
				newSpec.append(newFilter)
				print(newSpec)
				tempDataObj = DataObj(dobj.dataset, newSpec)
				output.append(tempDataObj)
		return(output)
	#if Row is not specified, create filters using unique values from all categorical variables in the dataset
	else:
		return(0)