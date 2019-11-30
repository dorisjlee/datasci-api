from vizLib.altair.BarChart import BarChart
from vizLib.altair.ScatterChart import ScatterChart
from vizLib.altair.LineChart import LineChart
from vizLib.altair.Histogram import Histogram

class AltairRenderer:
	'''
	Chart Object represents one Altair chart
	'''
	def __init__(self):
		pass
		# self.spec = spec
		# self.chart = self.initializeChart()
	def __repr__(self):
		return f"AltairRenderer <{str(self.dobj)}>"
	def createVis(self,dobj):
		if (dobj.mark =="histogram"):
			chart = Histogram(dobj)
		elif (dobj.mark =="bar"):
			chart = BarChart(dobj)
		elif (dobj.mark =="scatter"):
			chart = ScatterChart(dobj)
		elif (dobj.mark =="line"):
			chart = LineChart(dobj)
		return chart.chart
	def initializeChart(self):
		return NotImplemented
