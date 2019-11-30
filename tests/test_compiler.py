from dataset.Dataset import Dataset
from dataObj.dataObj import DataObj
from dataObj.Row import Row
from dataObj.Column import Column
import pytest
def test_underspecifiedSingleVis():
	dataset = Dataset("data/cars.csv",schema=[{"Year":{"dataType":"date"}}])
	dobj = DataObj(dataset,[Column("MilesPerGal"),Column("Weight")])
	assert dobj.spec[0].dataType == ""
	assert dobj.spec[0].dataModel == ""

	assert dobj.compiled.spec[0].dataType=="quantitative"
	assert dobj.compiled.spec[0].dataModel=="measure"
def test_underspecifiedVisCollection():
	# TODO write test for visualization collection
	assert True

def test_underspecifiedVisCollection_Z():
	dataset = Dataset("data/cars.csv",schema=[{"Year":{"dataType":"date"}}])
	dobj = DataObj(dataset,[Column("Horsepower"),Column("Brand"),Row("Origin",["Japan","USA"])])
	assert type(dobj.compiled).__name__ == "DataObjCollection"
	assert len(dobj.compiled.collection) == 2

	dobj = DataObj(dataset,[Column(["Horsepower","Weight"]),Column("Brand"),Row("Origin",["Japan","USA"])])
	assert type(dobj.compiled).__name__ == "DataObjCollection"
	assert len(dobj.compiled.collection) == 4

def test_autoencodingScatter():
	# No channel specified
	dataset = Dataset("data/cars.csv",schema=[{"Year":{"dataType":"date"}}])
	dobj = DataObj(dataset,[Column("MilesPerGal"),Column("Weight")])
	assert dobj.compiled.getByColumnName("MilesPerGal")[0].channel == "x"
	assert dobj.compiled.getByColumnName("Weight")[0].channel == "y"
	# Partial channel specified
	dobj = DataObj(dataset,[Column("MilesPerGal", channel="y"),Column("Weight")])
	assert dobj.compiled.getByColumnName("MilesPerGal")[0].channel == "y"
	assert dobj.compiled.getByColumnName("Weight")[0].channel == "x"

	# Full channel specified
	dobj = DataObj(dataset,[Column("MilesPerGal", channel="y"),Column("Weight", channel="x")])
	assert dobj.compiled.getByColumnName("MilesPerGal")[0].channel == "y"
	assert dobj.compiled.getByColumnName("Weight")[0].channel == "x"
	# Duplicate channel specified
	with pytest.raises(ValueError):
		# Should throw error because there should not be columns with the same channel specified
		dobj = DataObj(dataset,[Column("MilesPerGal", channel="x"),Column("Weight", channel="x")])

	
def test_autoencodingHistogram():
	dataset = Dataset("data/cars.csv",schema=[{"Year":{"dataType":"date"}}])
	
	# Partial channel specified
	dobj = DataObj(dataset,[Column("MilesPerGal",channel="y")])
	assert dobj.compiled.getByColumnName("MilesPerGal")[0].channel == "y"

	dobj = DataObj(dataset,[Column("MilesPerGal", channel="x")])
	assert dobj.compiled.getByColumnName("MilesPerGal")[0].channel == "x"
	assert dobj.compiled.getByColumnName("count()")[0].channel == "y"

def test_autoencodingLineChart():
	dataset = Dataset("data/cars.csv",schema=[{"Year":{"dataType":"date"}}])
	dobj = DataObj(dataset,[Column("Year"),Column("Acceleration")])
	checkAttributeOnChannel(dobj,"Year","x")
	checkAttributeOnChannel(dobj,"Acceleration","y")
	# Partial channel specified
	dobj = DataObj(dataset,[Column("Year", channel="y"),Column("Acceleration")])
	checkAttributeOnChannel(dobj,"Year","y")
	checkAttributeOnChannel(dobj,"Acceleration","x")

	# Full channel specified
	dobj = DataObj(dataset,[Column("Year", channel="y"),Column("Acceleration", channel="x")])
	checkAttributeOnChannel(dobj,"Year","y")
	checkAttributeOnChannel(dobj,"Acceleration","x")
	# Duplicate channel specified
	with pytest.raises(ValueError):
		# Should throw error because there should not be columns with the same channel specified
		dobj = DataObj(dataset,[Column("Year", channel="x"),Column("Acceleration", channel="x")])

def test_autoencodingColorLineChart():
	dataset = Dataset("data/cars.csv",schema=[{"Year":{"dataType":"date"}}])
	dobj = DataObj(dataset,[Column("Year"),Column("Acceleration"),Column("Origin")])
	checkAttributeOnChannel(dobj,"Year","x")
	checkAttributeOnChannel(dobj,"Acceleration","y")
	checkAttributeOnChannel(dobj,"Origin","color")
def test_autoencodingColorScatterChart():
	dataset = Dataset("data/cars.csv",schema=[{"Year":{"dataType":"date"}}])
	dobj = DataObj(dataset,[Column("Horsepower"),Column("Acceleration"),Column("Origin")])
	checkAttributeOnChannel(dobj,"Origin","color")
	dobj = DataObj(dataset,[Column("Horsepower"),Column("Acceleration",channel="color"),Column("Origin")])
	checkAttributeOnChannel(dobj,"Acceleration","color")
def checkAttributeOnChannel(dobj,attrName,channelName):
	assert dobj.compiled.getByColumnName(attrName)[0].channel == channelName