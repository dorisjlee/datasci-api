from vizLib.altair.AltairChart import AltairChart
import altair as alt
class LineChart(AltairChart):
	def __init__(self,dobj):
		self.dobj = dobj
		self.chart = self.initializeChart()
	def __repr__(self):
		return f"Line Chart <{str(self.dobj)}>"
	def initializeChart(self):
		dimension = list(filter(lambda x: x.dataModel=="dimension" if hasattr(x,"dataModel") else False,self.dobj.spec))[0].columnName
		measure = list(filter(lambda x: x.dataModel=="measure" if hasattr(x,"dataModel") else False,self.dobj.spec))[0].columnName
		chart = alt.Chart(self.dobj.dataset.df).mark_line().encode(
		    x = alt.X(dimension, type = "ordinal"),
		    # TODO: need to change aggregate to non-default function, read aggFunc info in somewhere
		    y = alt.Y(measure,type="quantitative", aggregate="mean")
		)
		return chart 
	