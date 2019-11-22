class Row:
	'''
	Row Object represents one or a group of datapoints (rows) in the Dataset.
	'''
	def __init__(self, fAttribute="",fVal= "", highlight="",clusterOutlier=""):
		self.className = "Row"
		# Descriptor
		self.fAttribute = fAttribute
		self.fVal = fVal

		self.points = []
		self.pattern = []
		# Properties
		self.highlight = highlight
		self.clusterOutlier = clusterOutlier
		
	def __repr__(self):
		return f"Row <{str(self.fAttribute)},{str(self.fVal)}>"

