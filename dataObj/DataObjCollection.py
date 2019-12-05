from vizLib.altair.AltairRenderer import AltairRenderer
class DataObjCollection:
	'''
	DataObjCollection is a list of DataObjects. 
	'''
	def __init__(self,collection):
		self.collection=collection

	def __repr__(self):
		return f"<Data Obj Collection: {str(self.collection)}>"

	def map(self,function):
		# generalized way of applying a function to each element
		return map(function, self.collection)
	
	def get(self,fieldName):
		# Get the value of the field for all objects in the collection
		def getField(dObj):
			fieldVal = getattr(dObj,fieldName)
			# Might want to write catch error if key not in field
			return fieldVal
		return self.map(getField)

	def set(self,fieldName,fieldVal):
		return NotImplemented

	def sort(self, descending = True):
		# sort in-place by “score” by default if available, otherwise user-specified field to sort by
		self.collection.sort(key=lambda x: x.score, reverse=descending)

	def topK(self,k):
		#sort and truncate list to first K items
		self.sort()
		return DataObjCollection(self.collection[:k])
	def bottomK(self,k):
		#sort and truncate list to first K items
		self.sort(descending=False)
		return DataObjCollection(self.collection[:k])

	def display(self,renderer="altair"):
		# Similar to display for individual DataObjects, takes fully specified visualizations and renders them. If score is available, display order of dashboard is based on score, otherwise random display order
		import jupyter_widget_mockup
		chartSpecs = []
		if (renderer=="altair"):
			renderer = AltairRenderer()
		collection = self.collection
		for viz in collection:
			chart = renderer.createVis(viz.compiled).to_dict()
			chartSpecs.append(chart)
		widget = jupyter_widget_mockup.Mockup(graphSpecs = chartSpecs)	
		return widget