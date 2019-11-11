class AltairChart:
	'''
	Chart Object represents one Altair chart
	'''
	def __init__(self, spec):
		self.spec = spec
		self.chart = self.initializeChart()
	def __repr__(self):
		return f"AltairChart <{str(self.dobj)}>"

	def initializeChart(self):
		return NotImplemented
