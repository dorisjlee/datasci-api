def valueBasedInterestingness(dobj):
	import pandas as pd

	#checks to see if a filter is applied to the data object, if no filter just use
	#basic aggregate function
	if len(dobj.getObjByRowColType("Row")) == 0:
		aggVal = dobj.dataset.df[dobj.spec[0].columnName].sum(skipna = True)
		return(list(aggVal)[0])
	else:
		row = dobj.getObjByRowColType("Row")[0]
		filteredData = dobj.dataset.df[dobj.dataset.df[row.fAttribute] == row.fVal]
		if len(filteredData) != 0:
			filteredAggVal = filteredData[dobj.spec[0].columnName].sum(skipna = True)
			return(list(filteredAggVal)[0])
		else:
			return(0)

