from vizLib.altair.AltairChart import AltairChart
import altair as alt
class Histogram(AltairChart):
	def __init__(self,dobj):
		super(Histogram,self).__init__(dobj)
	def __repr__(self):
		return f"Histogram <{str(self.dobj)}>"
	def initializeChart(self):
		xAttr = self.dobj.getObjFromChannel("x")[0].columnName
		yAttr = self.dobj.getObjFromChannel("y")[0].columnName
		#measures = list(filter(lambda x: x.dataModel=="measure" if hasattr(x,"dataModel") else False,self.dobj.spec))
		print (yAttr)
		if (yAttr=="count()"):
			chart = alt.Chart(self.dobj.dataset.df).mark_bar().encode(
				alt.X(xAttr, type="quantitative", bin=alt.Bin(maxbins=50)),
				alt.Y(yAttr),
			)
		else:
			chart = alt.Chart(self.dobj.dataset.df).mark_bar().encode(
				alt.X(xAttr),
				alt.Y(yAttr, type="quantitative", bin=alt.Bin(maxbins=50))
			)
		chart = chart.configure_mark(tooltip=alt.TooltipContent('encoding')) # Setting tooltip as non-null
		# interactive doesn't work for histograms
		#chart = chart.interactive() # If you want to enable Zooming and Panning 
		return chart 