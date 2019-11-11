class DataObj:
	'''
	DataObj is an abstract object representing some aspect of the data. 
	This can be based on what the user has specified or what is created as outputs.
	It can be a visualization, group of data points, column, etc and does not have to be fully specified.
	'''
	def __init__(self, dataset, spec = [] ):
		self.dataset = dataset
		self.spec =spec #list of Row and Column objects
		self.type = ""
	def __repr__(self):
		return f"<Data Obj: {str(self.dataset)} -- {str(self.spec)}>"

	def display(): 
		# render this data object as: vis, columns, etc.?
		return NotImplemented

