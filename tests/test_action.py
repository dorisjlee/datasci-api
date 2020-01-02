from dataset.Dataset import Dataset
from dataObj.dataObj import DataObj
from dataObj.Row import Row
from dataObj.Column import Column
import pytest
import numpy as np 
import math
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
	dobj.distribution()
	assert dobj.compiled.collection[0].score != 0

def test_generalize():
	dataset = Dataset("data/cars.csv",schema=[{"Year":{"dataType":"date"}}])

	dobj = DataObj(dataset,[Column(["Acceleration", "Horsepower"])])
	generalizedList = dobj.generalize()
	assert math.isclose(generalizedList[0].score, 40952, rel_tol=0.01) 
	assert math.isclose(generalizedList[1].score, 6092.2, rel_tol=0.01) 
	assert len(generalizedList) == 2

	dobj = DataObj(dataset,[Column(["Acceleration", "Horsepower"]),Row(fAttribute="Origin",fVal="USA")])
	generalizedList = dobj.generalize()
	assert math.isclose(generalizedList[0].score, 29167, rel_tol=0.01) 
	assert math.isclose(generalizedList[1].score,3672.6, rel_tol=0.01) 
	assert len(generalizedList) == 3

	dobj = DataObj(dataset,[Column(["Acceleration", "Horsepower"]),Column("MilesPerGal")])
	generalizedList = dobj.generalize()
	assert math.isclose(generalizedList[0].score, 40952, rel_tol=0.01) 
	assert len(generalizedList) == 3

	#dobj = DataObj(dataset,[Column("?",dataModel="measure"), Column("MilesPerGal")])
	#generalizedList = dobj.generalize()
	#assert generalizedList[0].score == 392
	#assert len(generalizedList) == 6