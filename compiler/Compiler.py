from dataObj.Row import Row
from dataObj.Column import Column
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
			if( rcObj.className == "Column"):
				if (rcObj.dataType==""):
					rcObj.dataType = expandedDobj.dataset.dataTypeLookup[rcObj.columnName]
				if (rcObj.dataModel==""):
					rcObj.dataModel = expandedDobj.dataset.dataModelLookup[rcObj.columnName]
		return expandedDobj

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
		rowAttrs = []
		# TODO: This needs to be rewritten in a recursive manner so that the channel and other specification can be inheritted
		if len(colSpecs)>0:
			col1Attrs = convert2List(colSpecs[0].columnName)
		if len(colSpecs)>1:
			col2Attrs = convert2List(colSpecs[1].columnName)
		if len(rowSpecs)>0:
			rowAttrs = convert2List(rowSpecs[0].rowName)
		# Generate Collection

		collection = []
		if (len(col1Attrs)<=1 and len(col2Attrs)<=1 and len(rowSpecs)<=1):
			# If DataObj does not represent a collection, return False. 
			return False
		else:
			for col1 in col1Attrs:
				for col2 in col2Attrs:
					if len(rowAttrs)>0:
						for row in rowAttrs:
							# create the data objects
							dataObj = DataObj(dobj.dataset,[Column(col1), Column(col2), Row(fAttribute=row,fVal='?')])
							collection.append(dataObj)
					else:
						dataObj = DataObj(dobj.dataset, [Column(col1), Column(col2)])
						collection.append(dataObj)
			return  DataObjCollection(collection)

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
			if (spec.dataModel == "dimension"):
				Ndim +=1
			elif (spec.dataModel == "measure"):
				Nmsr +=1
		# print ("Ndim,Nmsr:",Ndim,Nmsr)
		# Helper function (TODO: Move this into utils)
		def lineOrBar(dobj):
			dimension = filterDataModel(dobj,"dimension")[0]
			dimType = dimension.dataType
			if (dimType =="date" or dimType == "oridinal"):
				# chart = LineChart(dobj)
				return "line"
			else: # unordered categorical
				# chart = BarChart(dobj)
				return "bar"
				# TODO: if cardinality large than 6 then sort bars
			return chart
		def filterDataModel(dobj,dmodel):       
			return list(filter(lambda x: x.dataModel==dmodel if hasattr(x,"dataModel") else False,dobj.spec))
		def enforceSpecifiedChannel(dobj, autoChannel):
			available_channels = list(autoChannel.keys()) 
			# create a dictionary of specified channels in the given dobj
			specifiedDict = {} # specifiedDict={"x":[],"y":[list of Dobj with y specified as channel]}
			import copy
			specifiedChannel = copy.deepcopy(autoChannel)
			for val in available_channels:
				specifiedDict[val]=dobj.getObjFromChannel(val)
				specifiedChannel[val].channel = val # populate initially with the auto-values, will be overridden later if necessary
			# for every specified element, swap with channel that originally contained that element in the autoChannel
			for sVal,sAttr in specifiedDict.items():
				if (len(sAttr)==1): #if specified in dobj
					# remove the specified channel from available channels
					if (len(available_channels)>0):
						available_channels.remove(sVal)
						swapWithChannel = available_channels[0] # pick any
						specifiedChannel[swapWithChannel].channel = sVal
						specifiedChannel[sVal].channel = swapWithChannel
						available_channels.remove(swapWithChannel)
				elif (len(sAttr)>1):
					raise ValueError("There should not be more than one attribute specified in the same channel.")
				# elif (len(sAttr)==0): # if unspecified, then populate the channel value with the showMe default
				# 	specifiedChannel[sVal].channel = sVal
			dobj.spec = list(specifiedChannel.values())
			return dobj
		# ShowMe logic + additional heuristics
		countCol = Column("count()",dataModel="measure")
		# print (Ndim,Nmsr)
		xAttr = dobj.getObjFromChannel("x")
		yAttr = dobj.getObjFromChannel("y")
		zAttr = dobj.getObjFromChannel("z")
		if (Ndim == 0 and Nmsr ==1):
			# Histogram with Count on the y axis
			measure = filterDataModel(dobj,"measure")[0]
			measure.channel = "x"
			dobj.mark = "histogram"
		elif (Ndim ==1 and (Nmsr ==0 or Nmsr==1)):
			# Bar Chart
			#if x is unspecified
			if (Nmsr==0): 
				countCol.channel= "y" 
				dobj.spec.append(countCol)
			measure = filterDataModel(dobj,"measure")[0]
			measure.channel = "x"
			dobj.mark = lineOrBar(dobj)
		elif (Ndim ==2 and (Nmsr==0 or Nmsr==1)):
			
			dimension = filterDataModel(dobj,"dimension")
			d1 = dimension[0]
			d2 = dimension[1]
			if (dobj.dataset.cardinality[d1.columnName]<dobj.dataset.cardinality[d2.columnName]):
				# d1.channel = "color"
				dobj.removeColumnFromSpec(d1.columnName)
				colorAttr = d1.columnName
			else:
				# d2.channel = "color"
				dobj.removeColumnFromSpec(d2.columnName)
				colorAttr = d2.columnName
			# Colored Bar/Line chart with Count as default measure
			if (Nmsr==0):
				dobj.spec.append(countCol)
			# print (dobj)
			dobj.mark = lineOrBar(dobj)
			
			# TODO: Generalize to breakdown by? 
			chart.chart = chart.chart.encode(color=colorAttr)
		elif (Ndim ==0 and Nmsr==2):
			# Scatterplot
			dobj.mark = "scatter"
			autoChannel = {"x": dobj.spec[0],
				"y":dobj.spec[1]}
		elif (Ndim ==1 and Nmsr ==2):
			# Scatterplot broken down by the dimension
			measure = filterDataModel(dobj,"measure")
			m1 = measure[0]
			m2 = measure[1]

			colorAttr = filterDataModel(dobj,"dimension")[0].columnName
			dobj.removeColumnFromSpec(colorAttr)
			
			dobj.mark = "scatter"
			# TODO: Generalize to breakdown by? 
			chart.chart = chart.chart.encode(color=colorAttr)
		dobj = enforceSpecifiedChannel(dobj,autoChannel)
		return dobj