# from vizLib.altair.AltairChart import AltairChart
import altair as alt
class Histogram():
	def __init__(self,dobj):
		self.dobj = dobj
		self.chart = self.initializeChart()
	def __repr__(self):
		return f"Histogram <{str(self.dobj)}>"
	def initializeChart(self):
		xAttr = self.dobj.getObjFromChannel("x")[0].columnName
		#measures = list(filter(lambda x: x.dataModel=="measure" if hasattr(x,"dataModel") else False,self.dobj.spec))
		chart = alt.Chart(self.dobj.dataset.df).mark_bar().encode(
			alt.X(xAttr, type="quantitative", bin=alt.Bin(maxbins=50)),
			y='count()',
		)
		chart = chart.configure_mark(tooltip=alt.TooltipContent('encoding')) # Setting tooltip as non-null
		# interactive doesn't work for histograms
		#chart = chart.interactive() # If you want to enable Zooming and Panning 
		return chart 