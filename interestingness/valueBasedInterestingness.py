def valueBasedInterestingness(dobj):
  import pandas as pd

  aggVal = dobj.dataset.df.groupby(dobj.spec[0].columnName).count().iloc[:,0].sum()
  return(aggVal)