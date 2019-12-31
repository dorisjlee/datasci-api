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
	#list to keep track of columns and rows already included in the output (ensure no repeat graphs)
	columnNames = []
	rowNames = []
	for obj in vizCollection:
		#have to remove count() column from the specification first
		obj.removeColumnFromSpec("count()")

		columns = obj.getObjByRowColType("Column")
		rows = obj.getObjByRowColType("Row")
		numCol = len(columns)
		numRow = len(rows)
		numRowCol = numCol + numRow
		#iterates through the columns of the data object and removes one column at a time if the number of
		#rows and columns in the data object is greater than 1
		if numRowCol > 1:
			#if there is more than one column in a data object, iterate through the columns and remove them one by one
			if numCol > 1:
				for column in columns:
					tempDataObj = DataObj(obj.dataset, obj.spec)
					tempDataObj.removeColumnFromSpec(column.columnName)

					if len(tempDataObj.spec) > 0 and tempDataObj.spec[0].columnName not in columnNames:
						tempDataObj.score = valueBasedInterestingness(tempDataObj)
						outputDataCollection.append(tempDataObj)
						columnNames.append(tempDataObj.spec[0].columnName)
			else:
				columnNames.append(obj.spec[0].columnName)

			#iterates through the rows of the data object and removes one row at a time
			for row in rows:
				#use the original dataset before any filtering occurs
				tempDataObj = DataObj(dobj.dataset, obj.getObjByRowColType("Column"))
				#remove current row from the data object's specification
				originalRows = obj.getObjByRowColType("Row")
				newRows = originalRows.remove(row)

				#only adds rows to the temp data object specifications if there are rows to add
				if newRows != None:
					tempDataObj.spec.append(newRows)

				if len(tempDataObj.spec) > 0 and (newRows not in rowNames or newRows == None):
					tempDataObj.score = valueBasedInterestingness(tempDataObj)
					outputDataCollection.append(tempDataObj)
					rowNames.append(newRows)

		#if the data object only contains a single column, calculate its interestingness and add to the output
		else:
			obj.score = valueBasedInterestingness(obj)
			outputDataCollection.append(obj)

	return(outputDataCollection)