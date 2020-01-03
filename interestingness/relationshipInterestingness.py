def relationshipInterestingness(dobj):
	from scipy.stats import pearsonr
	#Interestingness metric for two measure attributes
  	#Calculate maximal information coefficient (see Murphy pg 61) or Pearson's correlation
	measures = dobj.getObjByDataModel("measure")
	m1 = measures[0]
	m2 = measures[1]

	if len(dobj.getObjByRowColType("Row")) == 0:
		m1Val = dobj.dataset.df[m1]
		m2Val = dobj.dataset.df[m2]
		pearsonCorr = pearsonr(m1Val, m2Val)[0]
		return(pearsonCorr)
	else:
		row = dobj.getObjByRowColType("Row")[0]
		filteredData = dobj.dataset.df[dobj.dataset.df[row.fAttribute] == row.fVal]
		if len(filteredData) != 0:
			m1Val = filteredData[m1]
			m2Val = filteredData[m2]
			pearsonCorr = pearsonr(m1Val, m2Val)[0]
			return(pearsonCorr)