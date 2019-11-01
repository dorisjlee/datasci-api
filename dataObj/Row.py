class Row:
	'''
	Row Object represents one or a group of datapoints (rows) in the Dataset.
	'''
	def __init__(self, fAttribute=fAttribute,fVal= fVal, highlightGrey=highlightGrey,clusterOutlier=clusterOutlier):
		# Descriptor
		self.fAttribute = fAttribute
		self.fVal = fVal

		self.points = []
		self.pattern = []
		# Properties
		self.highlightGrey = highlightGrey
		self.clusterOutlier = clusterOutlier
		
	def __repr__(self):
		return f"Row{str(self.rowName)}"

