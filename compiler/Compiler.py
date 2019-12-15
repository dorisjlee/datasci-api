from dataObj.Row import Row
from dataObj.Column import Column
from dataset.Dataset import Dataset


class Compiler:
	def __init__(self):
		self.name = "Compiler"
	def __repr__(self):
		return f"<Compiler>"

	def expandUnderspecified(self,dobj):
		# Automatic type conversion (only for single attributes not lists of attributes)
		import copy
		expandedDobj = copy.deepcopy(dobj) # Preserve the original dobj
		for rcObj in expandedDobj.spec:
			if(rcObj.className == "Column" and rcObj.columnName !="?"):
				if (rcObj.dataType==""):
					rcObj.dataType = expandedDobj.dataset.dataTypeLookup[rcObj.columnName]
				if (rcObj.dataModel==""):
					rcObj.dataModel = expandedDobj.dataset.dataModelLookup[rcObj.columnName]
		return expandedDobj

	def generateCollection(self, colAttrs,rowVals,fAttr,dobj): #[["a","b","c"],["c","d","f"]]
		# TODO: add logic for picking x and y axis

		from dataObj.dataObj import DataObj
		from dataObj.DataObjCollection import DataObjCollection

		collection = []

		def combine(colAttrs, accum):
			last = (len(colAttrs) == 1)
			n = len(colAttrs[0])
			for i in range(n):
				accum.append(colAttrs[0][i])
				item = accum
				accum = []
				if last:
					columnList = list(map(Column,item))
					if len(rowVals) > 0:
						for row in rowVals:
							fVal = row
							transformedDataset = applyDataTransformations(dobj.dataset, fAttr, fVal)  # rename?
							dataObj = DataObj(transformedDataset, columnList, title=f"{fAttr}={fVal}")
							collection.append(dataObj)
					else:
						dataObj = DataObj(dobj.dataset, columnList)
						collection.append(dataObj)
				else:
					combine(colAttrs[1:], item)

		combine(colAttrs, [])
		return DataObjCollection(collection)

	def enumerateCollection(self,dobj):
		# Get all the column and row object, assign the attribute names to variables
		colSpecs = list(filter(lambda x: x.className=="Column", dobj.spec))
		rowSpecs = list(filter(lambda x: x.className=="Row", dobj.spec))
		colAttrs = []
		rowVals = []
		fAttr = ''
		# TODO: This needs to be rewritten in a recursive manner so that the channel and other specification can be inheritted
		if len(colSpecs)>0:
			colAttrs.append(populateOptions(dobj,colSpecs[0]))

			# TODO: Note that this needs to be modified so that we can put in constraints such as: 
			# Column("?", dataModel = "measure") --> enumerate over all the attributes that are measures
			#if colSpecs[0].columnName =="?": populateOptions(colSpecs[0])
		if len(colSpecs)>1:
			colAttrs.append(populateOptions(dobj,colSpecs[1]))
		if len(rowSpecs)>0:
			rowVals = populateOptions(dobj,rowSpecs[0]) #populate rowvals with all unique possibilities
			fAttr = rowSpecs[0].fAttribute
		if all(len(attrs) <= 1 for attrs in colAttrs) and len(rowVals)<=1: # changed condition to check if every column attribute has at least one attribute
			# If DataObj does not represent a collection, return False.
			return False
		else:
			return self.generateCollection(colAttrs, rowVals, fAttr, dobj)

	def determineEncoding(self,dobj):
		'''
		determineEncoding populates dobj with the appropriate mark type and channel information
		
		Implementing automatic encoding from Tableau's VizQL 
		Mackinlay, J. D., Hanrahan, P., & Stolte, C. (2007). 
		Show Me: Automatic presentation for visual analysis. 
		IEEE Transactions on Visualization and Computer Graphics, 13(6), 1137–1144. 
		https://doi.org/10.1109/TVCG.2007.70594
	
		'''
		# TODO: possibly implement chart alternatives as a list of possible encodings
		# TODO: Need to generalize this import to other rendering mechanisms

		# Count number of measures and dimensions
		Ndim = 0 
		Nmsr = 0 
		for spec in dobj.spec:
			if (spec.className=="Column"):
				if (spec.dataModel == "dimension"):
					Ndim +=1
				elif (spec.dataModel == "measure"):
					Nmsr +=1
		# print ("Ndim,Nmsr:",Ndim,Nmsr)
		# Helper function (TODO: Move this into utils)
		def lineOrBar(dimension,measure):
			dimType = dimension.dataType
			if (dimType =="date" or dimType == "oridinal"):
				# chart = LineChart(dobj)
				return "line", {"x": dimension, "y": measure}
			else: # unordered categorical
				# chart = BarChart(dobj)
				return "bar", {"x": measure, "y": dimension}
				# TODO: if cardinality large than 6 then sort bars
		
		def enforceSpecifiedChannel(dobj, autoChannel):		
			resultDict = {} # result of enforcing specified channel will be stored in resultDict
			specifiedDict = {} # specifiedDict={"x":[],"y":[list of Dobj with y specified as channel]}
			# create a dictionary of specified channels in the given dobj
			for val in autoChannel.keys():
				specifiedDict[val]= dobj.getObjFromChannel(val)
				resultDict[val] = ""
			# for every element, replace with what's in specifiedDict if specified
			for sVal,sAttr in specifiedDict.items():
				if (len(sAttr)==1): #if specified in dobj
					# remove the specified channel from autoChannel (matching by value, since channel key may not be same)
					for i in list(autoChannel.keys()):
						if (autoChannel[i].columnName==sAttr[0].columnName):
							autoChannel.pop(i)
					sAttr[0].channel=sVal
					resultDict[sVal] = sAttr[0]
				elif (len(sAttr)>1):
					raise ValueError("There should not be more than one attribute specified in the same channel.")
			# For the leftover channels that are still unspecified in resultDict,
			# and the leftovers in the autoChannel specification,
			# step through them together and fill it automatically.
			leftover_channels = list(filter(lambda x: resultDict[x] =='',resultDict))
			for leftover_channel,leftover_encoding in zip(leftover_channels,autoChannel.values()):
				leftover_encoding.channel = leftover_channel
				resultDict[leftover_channel] = leftover_encoding
			dobj.spec = list(resultDict.values())
			return dobj
		# ShowMe logic + additional heuristics
		countCol = Column("count()",dataModel="measure")
		# print (Ndim,Nmsr)
		xAttr = dobj.getObjFromChannel("x")
		yAttr = dobj.getObjFromChannel("y")
		zAttr = dobj.getObjFromChannel("z")
		if (Ndim == 0 and Nmsr ==1):
			# Histogram with Count on the y axis
			measure = dobj.getObjByDataModel("measure")[0]
			dobj.spec.append(countCol)
			# measure.channel = "x"
			autoChannel = {"x": measure,"y": countCol}
			dobj.mark = "histogram"
		elif (Ndim ==1 and (Nmsr ==0 or Nmsr==1)):
			# Bar Chart
			#if x is unspecified
			if (Nmsr==0): 
				countCol.channel= "y" 
				dobj.spec.append(countCol)
			dimension = dobj.getObjByDataModel("dimension")[0]
			measure = dobj.getObjByDataModel("measure")[0]
			# measure.channel = "x"
			dobj.mark, autoChannel = lineOrBar(dimension,measure)
		elif (Ndim ==2 and (Nmsr==0 or Nmsr==1)):
			# Line or Bar chart broken down by the dimension
			dimensions = dobj.getObjByDataModel("dimension")
			d1 = dimensions[0]
			d2 = dimensions[1]
			if (dobj.dataset.cardinality[d1.columnName]<dobj.dataset.cardinality[d2.columnName]):
				# d1.channel = "color"
				dobj.removeColumnFromSpec(d1.columnName)
				dimension = d2
				colorAttr = d1
			else:
				if (d1.columnName == d2.columnName):
					dobj.spec.pop(0) # if same attribute then removeColumnFromSpec will remove both dims, we only want to remove one
				else:
					dobj.removeColumnFromSpec(d2.columnName)
				dimension = d1
				colorAttr = d2
			# Colored Bar/Line chart with Count as default measure
			if (Nmsr==0):
				dobj.spec.append(countCol)
			measure = dobj.getObjByDataModel("measure")[0]
			dobj.mark, autoChannel = lineOrBar(dimension,measure)
			autoChannel["color"] = colorAttr
		elif (Ndim ==0 and Nmsr==2):
			# Scatterplot
			dobj.mark = "scatter"
			autoChannel = {"x": dobj.spec[0],
				"y":dobj.spec[1]}
		elif (Ndim ==1 and Nmsr ==2):
			# Scatterplot broken down by the dimension
			measure = dobj.getObjByDataModel("measure")
			m1 = measure[0]
			m2 = measure[1]

			colorAttr = dobj.getObjByDataModel("dimension")[0]
			dobj.removeColumnFromSpec(colorAttr)
			
			dobj.mark = "scatter"
			autoChannel = {"x": m1,
							"y":m2,
							"color":colorAttr}

		dobj = enforceSpecifiedChannel(dobj,autoChannel)
		return dobj
def convert2List(x):
	'''
	"a" --> ["a"]
	["a","b"] --> ["a","b"]
	'''
	if type(x)!=list:
		return [x]
	else:
		return x
def applyDataTransformations(dataset, fAttribute, fVal):
	transformedDataset = Dataset(dataset.filename, dataset.schema)
	transformedDataset.df = dataset.df[dataset.df[fAttribute] == fVal]
	return transformedDataset
def populateOptions(dobj,rowCol):
	if rowCol.className =="Column":
		if rowCol.columnName =="?":
			options = set(dobj.dataset.attrList) # all attributes
			if (rowCol.dataType !=""):
				options = options.intersection(set(dobj.dataset.dataType[rowCol.dataType]))
			if (rowCol.dataModel !=""):
				options = options.intersection(set(dobj.dataset.dataModel[rowCol.dataModel]))
			options = list(options)
		else: 
			options = convert2List(rowCol.columnName)
	elif rowCol.className =="Row":
		if rowCol.fVal =="?":
			options = dobj.dataset.df[rowCol.fAttribute].unique()
		else: 
			options = convert2List(rowCol.fVal)
	return options
	