import altair as alt
class LineChart():
	def __init__(self,dobj):
		self.dobj = dobj
		self.chart = self.initializeChart()
	def __repr__(self):
		return f"Line Chart <{str(self.dobj)}>"
	def initializeChart(self):
		xAttr = self.dobj.getObjFromChannel("x")[0]
		yAttr = self.dobj.getObjFromChannel("y")[0]
		if (yAttr.dataModel == "measure"):		
			chart = alt.Chart(self.dobj.dataset.df).mark_line().encode(
			    x = alt.X(xAttr.columnName, type = "ordinal"),
			    # TODO: need to change aggregate to non-default function, read aggFunc info in somewhere
			    y = alt.Y(yAttr.columnName,type="quantitative", aggregate="mean")
			)
		else:
			chart = alt.Chart(self.dobj.dataset.df).mark_line().encode(
			    x = alt.X(xAttr.columnName,type="quantitative", aggregate="mean"),
			    y = alt.Y(yAttr.columnName, type = "ordinal")
			)
		chart = chart.configure_mark(tooltip=alt.TooltipContent('encoding')) # Setting tooltip as non-null
		chart = chart.interactive() # If you want to enable Zooming and Panning
		return chart 
	