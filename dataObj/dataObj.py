from dataObj.Row import Row
from dataObj.Column import Column
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
		return f"<Data Obj: {str(self.dataset)} -- {str(self.spec)}>"

	def expandUnderspecified(self):
		for rcObj in self.spec:
			if (rcObj.dataType==""):
				rcObj.dataType = self.dataset.dataTypeLookup[rcObj.columnName]
			
			if (rcObj.dataModel==""):
				rcObj.dataModel = self.dataset.dataModelLookup[rcObj.columnName]
			
	def display(self): 
		# render this data object as: vis, columns, etc.?
		return self.showMe()
		# return NotImplemented
	def showMe(self):
		# TODO: possibly implement chart alternatives as a list of possible encodings
		dobj = self 
		# TODO: Need to generalize this import to other rendering mechanisms
		from vizLib.altair.BarChart import BarChart
		from vizLib.altair.ScatterChart import ScatterChart
		from vizLib.altair.Histogram import Histogram
		from vizLib.altair.LineChart import LineChart
		# Count number of measures and dimensions
		Ndim = 0 
		Nmsr = 0 
		for spec in dobj.spec: 
			if (spec.dataModel == "dimension"):
				Ndim +=1
			elif (spec.dataModel == "measure"):
				Nmsr +=1
		print ("Ndim,Nmsr:",Ndim,Nmsr)
		# Helper function (TODO: Move this into utils)
		def lineOrBar(dobj):
			dimension = filterDataModel(dobj,"dimension")[0]
			dimType = dimension.dataType
			if (dimType =="date" or dimType == "oridinal"):
				chart = LineChart(dobj)
			else: # unordered categorical
				chart = BarChart(dobj)
				# TODO: if cardinality large than 6 then sort bars
			return chart
		def filterDataModel(dobj,dmodel):       
			return list(filter(lambda x: x.dataModel==dmodel if hasattr(x,"dataModel") else False,dobj.spec))
		# ShowMe logic + additional heuristics
		countCol = Column("Count")
		if (Ndim == 0 and Nmsr ==1):
			# Histogram with Count on the y axis
			chart = Histogram(dobj)
		elif (Ndim ==2 and Nmsr==0):
			pass
		elif (Ndim ==0 and Nmsr==2):
			# Scatterplot
			chart = ScatterChart(dobj)
		elif (Ndim ==1 and Nmsr ==2):
			# Scatterplot broken down by the dimension
			pass 
		elif (Ndim ==1 and (Nmsr ==0 or Nmsr==1)):
			# Bar Chart
			if (Nmsr==0): dobj.spec.append(countCol)
			chart = lineOrBar(dobj)
		elif (Ndim ==2 and Nmsr==1):
			print("here")
			# Bar/Line chart broken down by dimension
			dimension = filterDataModel(dobj,"dimension")
			d1 = dimension[0]
			d2 = dimension[1]
			if (dobj.dataset.cardinality[d1.columnName]<dobj.dataset.cardinality[d2.columnName]):
				d1.channel = "color"
			else:
				d2.channel = "color"
			chart = lineOrBar(dobj)
			# TODO: Generalize to breakdown by? 
			chart.chart = chart.chart.encode(color="Origin")
		elif (Ndim==3):
			pass
		else:
			pass
		return chart.chart
