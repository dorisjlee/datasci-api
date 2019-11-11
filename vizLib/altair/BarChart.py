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
		    x = alt.X(measure,type="quantitative", aggregate="mean")#,
		    #color=alt.condition(
		    #     f"datum.{dimension} == {insightDic['FILTER_VAL']}",  # If the year is 1810 this test returns True,
		    #     alt.value('orange'),     # which sets the bar orange.
		    #     alt.value('steelblue')   # And if it's not true it sets the bar steelblue.
		    # )
		)
		return chart 
	