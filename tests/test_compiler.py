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

def test_channelEnforcingScatter():
	# No channel specified
	dataset = Dataset("data/cars.csv",schema=[{"Year":{"dataType":"date"}}])
	dobj = DataObj(dataset,[Column("MilesPerGal"),Column("Weight")])
	assert dobj.compiled.spec[0].channel =="x"
	assert dobj.compiled.spec[1].channel =="y"
	# Partial channel specified
	dobj = DataObj(dataset,[Column("MilesPerGal", channel="y"),Column("Weight")])
	assert dobj.compiled.spec[0].channel =="y"
	assert dobj.compiled.spec[1].channel =="x"

	# Full channel specified
	dobj = DataObj(dataset,[Column("MilesPerGal", channel="y"),Column("Weight", channel="x")])
	assert dobj.compiled.spec[0].channel =="y"
	assert dobj.compiled.spec[1].channel =="x"
	# Duplicate channel specified
	with pytest.raises(ValueError):
		# Should throw error because there should not be columns with the same channel specified
		dobj = DataObj(dataset,[Column("MilesPerGal", channel="x"),Column("Weight", channel="x")])

def test_channelEnforcingHistogram():
	dataset = Dataset("data/cars.csv",schema=[{"Year":{"dataType":"date"}}])
	
	# Partial channel specified
	dobj = DataObj(dataset,[Column("MilesPerGal",channel="y")])
	assert dobj.compiled.spec[0].channel =="y"

	# Fail: need to debug
	# dobj = DataObj(dataset,[Column("MilesPerGal", channel="x")])
	# assert dobj.compiled.spec[0].channel =="x"

