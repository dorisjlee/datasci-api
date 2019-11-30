from vizLib.altair.AltairChart import AltairChart
import altair as alt
class BarChart(AltairChart):
	def __init__(self,dobj):
		super(BarChart,self).__init__(dobj)
	def __repr__(self):
		return f"Bar Chart <{str(self.dobj)}>"
	def initializeChart(self):
		xAttr = self.dobj.getObjFromChannel("x")[0]
		yAttr = self.dobj.getObjFromChannel("y")[0]
		if (xAttr.dataModel == "measure"):
			chart = alt.Chart(self.dobj.dataset.df).mark_bar().encode(
			    y = alt.Y(yAttr.columnName, type = "nominal"),
			    x = alt.X(xAttr.columnName,type="quantitative", aggregate="mean")#TODO: fix to non-default aggregate function
			)
		else:
			chart = alt.Chart(self.dobj.dataset.df).mark_bar().encode(
				x = alt.X(xAttr.columnName, type = "nominal"),
			    y = alt.Y(yAttr.columnName,type="quantitative", aggregate="mean")#TODO: fix to non-default aggregate function
			)
		chart = chart.configure_mark(tooltip=alt.TooltipContent('encoding')) # Setting tooltip as non-null
		# Can not do interactive whenever you have default count measure otherwise output strange error (Javascript Error: Cannot read property 'length' of undefined)
		#chart = chart.interactive() # If you want to enable Zooming and Panning
		return chart 
	