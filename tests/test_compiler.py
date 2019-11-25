from dataset.Dataset import Dataset
from dataObj.dataObj import DataObj
from dataObj.Row import Row
from dataObj.Column import Column
def test_underspecifiedSingle():
	dataset = Dataset("data/cars.csv",schema=[{"Year":{"dataType":"date"}}])
	dobj = DataObj(dataset,[Column("MilesPerGal"),Column("Weight")])
	assert dobj.spec[0].dataType == ""
	assert dobj.spec[0].dataModel == ""

	assert dobj.compiled.spec[0].dataType=="quantitative"
	assert dobj.compiled.spec[0].dataModel=="measure"
