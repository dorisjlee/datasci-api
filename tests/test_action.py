from dataset.Dataset import Dataset
from dataObj.dataObj import DataObj
from dataObj.Row import Row
from dataObj.Column import Column
import pytest
import numpy as np 
def test_correlation():
	dataset = Dataset("data/cars.csv",schema=[{"Year":{"dataType":"date"}}])
	dobj = DataObj(dataset,[Column(["Horsepower","Weight","Acceleration","Displacement"]),Column("MilesPerGal")])
	dobj.correlation()
	# Make sure that all correlation result in a single score
	assert np.sum(list(map(lambda x: hasattr(x,"score"),dobj.compiled.collection)))==True*len(dobj.compiled.collection)

	dobj = DataObj(dataset,[Column(["MilesPerGal","Horsepower"]),Column("MilesPerGal")])
	dobj.correlation()
	assert dobj.compiled.collection[0].score == -1 # identity test

def test_distribution():
	dataset = Dataset("data/cars.csv",schema=[{"Year":{"dataType":"date"}}])
	dobj = DataObj(dataset,[Column(["Horsepower","Weight","Acceleration","Displacement"])])
	dobj.correlation()
	# Make sure that all correlation result in a single score
	assert np.sum(list(map(lambda x: hasattr(x,"score"),dobj.compiled.collection)))==True*len(dobj.compiled.collection)
	assert dobj.compiled.collection[0].score != 0 # identity test