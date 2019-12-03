from dataObj.Row import Row
from dataObj.Column import Column
from vizLib.altair.AltairRenderer import AltairRenderer
from compiler.Compiler import Compiler
class DataObj:
	'''
	DataObj is an abstract object representing some aspect of the data. 
	This can be based on what the user has specified or what is created as outputs.
	It can be a visualization, group of data points, column, etc and does not have to be fully specified.
	'''
	def __init__(self, dataset, spec = [], title = "" ):
		self.dataset = dataset # may be inefficient use of memory
		self.spec =spec #list of Row and Column objects
		self.title = title
		self.type = ""
		self.mark = ""
		self.compile()

	def __repr__(self):
		# TODO: figure out a way to call display when printing out a data obj
		# currently repr can not be used for printing out non-string values. (Ref to how Dataframe is displayed by default in Pandas)
		if hasattr(self,"score"):
			return f"<Data Obj: {str(self.dataset)} -- {str(self.spec)} -- {self.score:.2f}>"
		else:
			return f"<Data Obj: {str(self.dataset)} -- {str(self.spec)}>"

	# def __str__(self):
	# 	vis = self.display()
	# 	if (vis): 
	# 		return vis
	# 	else: 
	# 		return f"<Data Obj: {str(self.dataset)} -- {str(self.spec)}>"

	def compile(self):
		dobj = self
		compiler = Compiler()
		# 1. If the DataObj represent a collection, then compile it into a collection. Otherwise, return False
		# Input: DataObj --> Output: DataObjCollection/False
		dataObjCollection = compiler.enumerateCollection(dobj)
		# 2. For every DataObject in the DataObject Collection, expand underspecified
		# Output : DataObj/DataObjectCollection
		if (dataObjCollection):
			self.compiled = dataObjCollection  # Preserve any dataObjectCollection specification
			compiledCollection = []
			for dataObj in dataObjCollection.collection:
				compiled = compiler.expandUnderspecified(dataObj) # autofill data type/model information
				compiled = compiler.determineEncoding(compiled)    # autofill viz related information
				compiledCollection.append(compiled)
				# print ("uncompiled:",dataObj)
				# print ("compiled:",compiled)
			self.compiled.collection = compiledCollection # return DataObjCollection
		else:
			compiled = compiler.expandUnderspecified(dobj) # autofill data type/model information
			compiled = compiler.determineEncoding(compiled)    # autofill viz related information
			self.compiled = compiled
			# print ("uncompiled:",dobj)
			# print ("compiled:",self.compiled)
			
	def display(self,renderer="altair"): 
		# render this data object as: vis, columns, etc.?
		# import jupyter_widget_mockup
		# if (renderer=="altair"):
		# 	renderer = AltairRenderer()
		# chart = renderer.createVis(self.compiled)
		# widget = jupyter_widget_mockup.Mockup(graphSpecs = [chart.to_dict()])
		# return widget
		# return chart
		import jupyter_widget_mockup
		chartSpecs = []
		if (renderer=="altair"):
			renderer = AltairRenderer()
		collection=[]
		if (type(self.compiled).__name__=="DataObj"):
			collection = [self]
		elif (type(self.compiled).__name__=="DataObjCollection"):
			collection = self.compiled.collection
		for viz in collection:
			chart = renderer.createVis(viz.compiled).to_dict()
			chartSpecs.append(chart)
		widget = jupyter_widget_mockup.Mockup(graphSpecs = chartSpecs)	
		return widget
	def singleDisplay(self,renderer="altair"): 
		# For debugging only: 
		# display not through widget but through altair default 
		if (renderer=="altair"):
			renderer = AltairRenderer()
		chart = renderer.createVis(self.compiled)
		return chart
	def getObjFromChannel(self,channel):
		specObj =  list(filter(lambda x: x.channel ==channel if hasattr(x,"channel") else False ,self.spec))
		return specObj
	def getObjByDataModel(self,dmodel):       
		return list(filter(lambda x: x.dataModel==dmodel if hasattr(x,"dataModel") else False,self.spec))
	def getByColumnName(self,columnName):
		return list(filter(lambda x: x.columnName == columnName, self.spec))
	def removeColumnFromSpec(self,columnName):
		self.spec = list(filter(lambda x: x.columnName!=columnName,self.spec))
	

	# Mappers to Action classes
	def correlation(self):
		from action.Correlation import Correlation
		corr = Correlation()
		corr.compute(self)