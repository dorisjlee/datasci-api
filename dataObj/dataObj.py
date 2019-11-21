from dataObj.Row import Row
from dataObj.Column import Column
from vizLib.Autoencoding import Autoencoding
class DataObj:
	'''
	DataObj is an abstract object representing some aspect of the data. 
	This can be based on what the user has specified or what is created as outputs.
	It can be a visualization, group of data points, column, etc and does not have to be fully specified.
	'''
	def __init__(self, dataset, spec = [] ):
		self.dataset = dataset # may be inefficient use of memory
		self.spec =spec #list of Row and Column objects
		self.type = ""
		self.expandUnderspecified()

	def __repr__(self):
		# TODO: figure out a way to call display when printing out a data obj
		# currently repr can not be used for printing out non-string values. (Ref to how Dataframe is displayed by default in Pandas)
		return f"<Data Obj: {str(self.dataset)} -- {str(self.spec)}>"

	# def __str__(self):
	# 	vis = self.display()
	# 	if (vis): 
	# 		return vis
	# 	else: 
	# 		return f"<Data Obj: {str(self.dataset)} -- {str(self.spec)}>"
	def expandUnderspecified(self):
		for rcObj in self.spec:
			if( type(rcObj) is Column):
				if (rcObj.dataType==""):
					rcObj.dataType = self.dataset.dataTypeLookup[rcObj.columnName]

				if (rcObj.dataModel==""):
					rcObj.dataModel = self.dataset.dataModelLookup[rcObj.columnName]

	def display(self,renderer="altair"): 
		# render this data object as: vis, columns, etc.?
		import jupyter_widget_mockup
		encoder = Autoencoding(renderer)
		chart = encoder.createVis(self)
		widget = jupyter_widget_mockup.Mockup(graphSpecs = [chart.to_dict()])
		return widget
		# return chart
	def removeColumnFromSpec(self,columnName):
		self.spec = list(filter(lambda x: x.columnName!=columnName,self.spec))
	