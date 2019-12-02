from action.Action import Action
class Correlation(Action):
	'''
	Correlation between measure variables
	'''
	def __init__(self):
		self.name = ""
		self.description = ""
		self.dobj_requirement = {}
	def __repr__(self):
		return f"<Action: {str(self.settings)}>"
			
	def check_requirement(self,dobj):
		# Check whether data object has the right set of requirements to execute this action
		raise NotImplementedError

	def compute(self,dobj):
		# Enumerate --> compute the scores for each item in the collection 
		# -->  return DataObjectCollection with the scores 
		import scipy.stats
		import numpy as np
		# TODO: need to make this work for DataObject (when input is not collection and just a single DataObject)
		for obj in dobj.compiled.collection:
		    measures = obj.getObjByDataModel("measure")

		    msr1 = measures[0].columnName
		    msr2 = measures[1].columnName

		    msr1Vals = list(obj.dataset.df[msr1])
		    msr2Vals = list(obj.dataset.df[msr2])
		    
		    obj.score = np.abs(scipy.stats.pearsonr(msr1Vals,msr2Vals)[0])
		print (dobj.compiled)
	def displayAsWidget(self,dobj):
		# display result in widget
		raise NotImplementedError

