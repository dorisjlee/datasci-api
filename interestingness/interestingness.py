def interestingness(dobj):
	numAttributes = len(dobj.getObjByRowColType("Column"))
	if numAttributes == 1:
		attrType = dobj.spec[0].dataModel
		if classType == "measure":
			from interestingness import valueBasedInterestingness
			return(valueBasedInterestingness(dobj))
		elif classType == "dimension":
			return(0.5)
			#from interestingness import countBasedInterestingness
			#return(countBasedinterstingness(dobj))
	elif numAttributes == 2:
		numMeasure = len(dobj.getObjByDataModel("measure"))
		numDimension = len(dobj.getObjByDataModel("dimension"))

		if numMeasure == 2:
			from interestingness import relationshipBasedInterestingness
			return(relationshipBasedInterestingness(dobj))
		elif numMeasure == 1 and numDimension == 1
			return(0.5)
			#from interstingness import distributionBasedInterestingness
			#return(distributionBasedInterestingness(dobj))
		else:
			return(0)