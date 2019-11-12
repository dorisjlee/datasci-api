from vizLib.altair.AltairChart import AltairChart
import altair as alt
class ScatterChart(AltairChart):
	def __init__(self,dobj):
		self.dobj = dobj
		self.chart = self.initializeChart()
	def __repr__(self):
		return f"ScatterChart <{str(self.dobj)}>"
	def initializeChart(self):
		measures = list(filter(lambda x: x.dataModel=="measure" if hasattr(x,"dataModel") else False,self.dobj.spec))
		chart = alt.Chart(self.dobj.dataset.df).mark_circle().encode(
		    x=alt.X(measures[0].columnName),
		    y=alt.Y(measures[1].columnName)
		)
		chart = chart.configure_mark(tooltip=alt.TooltipContent('encoding')) # Setting tooltip as non-null
		chart = chart.interactive() # If you want to enable Zooming and Panning

		return chart 