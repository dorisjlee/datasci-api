import altair as alt
class BarChart():
	def __init__(self,dobj):
		self.dobj = dobj
		self.chart = self.initializeChart()
	def __repr__(self):
		return f"Bar Chart <{str(self.dobj)}>"
	def initializeChart(self):
		dimension = list(filter(lambda x: x.dataModel=="dimension" if hasattr(x,"dataModel") else False,self.dobj.spec))[0].columnName
		measure = list(filter(lambda x: x.dataModel=="measure" if hasattr(x,"dataModel") else False,self.dobj.spec))[0].columnName
		chart = alt.Chart(self.dobj.dataset.df).mark_bar().encode(
		    y = alt.Y(dimension, type = "nominal"),
		    x = alt.X(measure,type="quantitative", aggregate="mean")#TODO: fix to non-default aggregate function
		)
		chart = chart.configure_mark(tooltip=alt.TooltipContent('encoding')) # Setting tooltip as non-null
		# Can not do interactive whenever you have default count measure otherwise output strange error (Javascript Error: Cannot read property 'length' of undefined)
		#chart = chart.interactive() # If you want to enable Zooming and Panning
		return chart 
	