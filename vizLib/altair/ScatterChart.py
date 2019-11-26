import altair as alt
class ScatterChart():
	def __init__(self,dobj):
		self.dobj = dobj
		self.chart = self.initializeChart()
	def __repr__(self):
		return f"ScatterChart <{str(self.dobj)}>"
	def initializeChart(self):
		# UP TO HERE: Broken because self.expandUnderspecified() in dataObj does not run when there are multiple object, we should not rely on spec
		# measures = list(filter(lambda x: x.dataModel=="measure" if hasattr(x,"dataModel") else False,self.dobj.spec))
		measures = self.dobj.spec
		chart = alt.Chart(self.dobj.dataset.df).mark_circle().encode(
		    x=alt.X(measures[0].columnName),
		    y=alt.Y(measures[1].columnName)
		)
		chart = chart.configure_mark(tooltip=alt.TooltipContent('encoding')) # Setting tooltip as non-null
		chart = chart.interactive() # If you want to enable Zooming and Panning

		return chart 