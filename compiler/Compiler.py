from dataObj.Row import Row
from dataObj.Column import Column
class Compiler:
	def __init__(self):
		self.name = "Compiler"
	def __repr__(self):
		return f"<Compiler>"

	def expandUnderspecified(self,dobj):
		# Automatic type conversion (only for single attributes not lists of attributes)
		for rcObj in dobj.spec:
			if( type(rcObj) is Column and type(rcObj)=="string"):
				if (rcObj.dataType==""):
					rcObj.dataType = dobj.dataset.dataTypeLookup[rcObj.columnName]

				if (rcObj.dataModel==""):
					rcObj.dataModel = dobj.dataset.dataModelLookup[rcObj.columnName]

	def applyDataTransformations(self,dataset,fAttribute,fVals):
		if fVals[0] != "?":
			dataset.df = dataset.df[dataset.df[fAttribute].isin(fVals)]
		return dataset

	def enumerateCollection(self,dobj):
		from dataObj.dataObj import DataObj
		from dataObj.DataObjCollection import DataObjCollection

		def convert2List(x):
			'''
			"a" --> ["a"]
			["a","b"] --> ["a","b"]
			'''
			if type(x)!=list:
				return [x]
			else:
				return x
		# Get all the column and row object, assign the attribute names to variables
		colSpecs = list(filter(lambda x: x.className=="Column", dobj.spec))
		rowSpecs = list(filter(lambda x: x.className=="Row", dobj.spec))
		col1Attrs = []
		col2Attrs = []
		# TODO: This needs to be rewritten in a recursive manner so that the channel and other specification can be inheritted
		if len(colSpecs)>0:
			col1Attrs = convert2List(colSpecs[0].columnName)
		if len(colSpecs)>1:
			col2Attrs = convert2List(colSpecs[1].columnName)
		if len(rowSpecs)>0:
			rowVals = convert2List(rowSpecs[0].fVal)
		# Generate Collection
		collection = []
		if (len(col1Attrs)<=1 and len(col2Attrs)<=1 and len(rowSpecs)<=1):
			return  DataObjCollection(collection)
		else:
			for col1 in col1Attrs:
				for col2 in col2Attrs:
					if len(rowVals)>0:
						# create the data objects
						transformedDataset = self.applyDataTransformations(dobj.dataset, rowSpecs[0].fAttribute,rowVals) #rename?
						dataObj = DataObj(transformedDataset,[Column(col1), Column(col2)])
						collection.append(dataObj)
					else:
						dataObj = DataObj(dobj.dataset, [Column(col1), Column(col2)])
						collection.append(dataObj)
			return  DataObjCollection(collection)