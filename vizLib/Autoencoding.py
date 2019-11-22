from dataObj.Row import Row
from dataObj.Column import Column

class Autoencoding:
	'''
	Implementing automatic encoding from Tableau's VizQL 
		Mackinlay, J. D., Hanrahan, P., & Stolte, C. (2007). 
		Show Me: Automatic presentation for visual analysis. 
		IEEE Transactions on Visualization and Computer Graphics, 13(6), 1137–1144. 
		https://doi.org/10.1109/TVCG.2007.70594
	'''
	def __init__(self, renderer = "altair"):
		self.renderer = renderer

	def createVis(self,dobj):
		# TODO: possibly implement chart alternatives as a list of possible encodings
		# TODO: Need to generalize this import to other rendering mechanisms
		if (self.renderer=="altair"):
			from vizLib.altair.BarChart import BarChart
			from vizLib.altair.ScatterChart import ScatterChart
			from vizLib.altair.Histogram import Histogram
			from vizLib.altair.LineChart import LineChart
		# Count number of measures and dimensions
		Ndim = 0 
		Nmsr = 0 
		for spec in dobj.spec: 
			if (dobj.dataset.dataModelLookup[spec.columnName] == "dimension"):
				Ndim +=1
			elif (dobj.dataset.dataModelLookup[spec.columnName] == "measure"):
				Nmsr +=1
		# print ("Ndim,Nmsr:",Ndim,Nmsr)
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
		countCol = Column("count()",dataModel="measure")
		if (Ndim == 0 and Nmsr ==1):
			# Histogram with Count on the y axis
			chart = Histogram(dobj)
		elif (Ndim ==2 and Nmsr==0):
			# Colored Bar/Line chart with Count as default measure
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
			dobj.spec.append(countCol)
			# print (dobj)
			chart = lineOrBar(dobj)
			# print (colorAttr)
			# TODO: Generalize to breakdown by? 
			chart.chart = chart.chart.encode(color=colorAttr)
		elif (Ndim ==0 and Nmsr==2):
			# Scatterplot
			chart = ScatterChart(dobj)
		elif (Ndim ==1 and Nmsr ==2):
			# Scatterplot broken down by the dimension
			measure = filterDataModel(dobj,"measure")
			m1 = measure[0]
			m2 = measure[1]

			colorAttr = filterDataModel(dobj,"dimension")[0].columnName
			dobj.removeColumnFromSpec(colorAttr)
			
			chart = ScatterChart(dobj)
			# TODO: Generalize to breakdown by? 
			chart.chart = chart.chart.encode(color=colorAttr)
		elif (Ndim ==1 and (Nmsr ==0 or Nmsr==1)):
			# Bar Chart
			if (Nmsr==0): dobj.spec.append(countCol)
			chart = lineOrBar(dobj)
		elif (Ndim ==2 and Nmsr==1):
			# Bar/Line chart broken down by dimension
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
			chart = lineOrBar(dobj)
			# TODO: Generalize to breakdown by? 
			chart.chart = chart.chart.encode(color=colorAttr)
		elif (Ndim==3):
			pass
		else:
			pass
		if (chart):
			return chart.chart
		else:
			False
