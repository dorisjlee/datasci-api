from vizLib.altair.AltairChart import AltairChart
import altair as alt
class BarChart(AltairChart):
	def __init__(self,dobj):
		self.dobj = dobj
		self.chart = self.initializeChart()
	def __repr__(self):
		return f"Bar Chart <{str(self.dobj)}>"
	def initializeChart(self):
		dimension = list(filter(lambda x: x.dataModel=="dimension" if hasattr(x,"dataModel") else False,self.dobj.spec))[0].columnName
		measure = list(filter(lambda x: x.dataModel=="measure" if hasattr(x,"dataModel") else False,self.dobj.spec))[0].columnName
		chart = alt.Chart(self.dobj.dataset.df).mark_bar().encode(
		    y = alt.Y(dimension, type = "nominal", sort=alt.EncodingSortField(
		            field=measure,  # The field to use for the sort
		            op="mean",  # The operation to run on the field prior to sorting
		            order="descending"  # The order to sort in
		        )),
		    x = alt.X(measure,type="quantitative", aggregate="mean")
		)
		chart = chart.configure_mark(tooltip=alt.TooltipContent('encoding')) # Setting tooltip as non-null
		chart = chart.interactive() # If you want to enable Zooming and Panning

		return chart 
	