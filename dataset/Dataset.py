import pandas as pd
import json
class Dataset:
	def __init__(self,filename):
		self.filename = filename
		self.df = self.loadCSV()
		# self.df_json  = self.df.to_json(orient='records')
		self.computeDataType()
		self.computeDataModel()
		self.computeStats()

	def __repr__(self):
		return f"<Dataset Obj: {str(self.filename)}>"

	def loadCSV(self):
		df = pd.read_csv(self.filename)
		return df

	def computeDataType(self):
		df = self.df
		self.dataType = {
			"quantitative":list(df.dtypes[df.dtypes=="float64"].keys()) + list(df.dtypes[df.dtypes=="int64"].keys()),
			"categorical":list(df.dtypes[df.dtypes=="object"].keys()),
			"ordinal": [],
			"date":[]
		}
		# for attr in list(df.dtypes[df.dtypes=="int64"].keys()):
		# 	if self.cardinality[attr]>50:

		self.dataTypeLookup = self.reverseMapping(self.dataType)


	def computeDataModel(self):
		self.dataModel = {
			"measure":self.dataType["quantitative"],
			"dimension":self.dataType["ordinal"]+self.dataType["categorical"]+self.dataType["date"]
		}

		self.dataModelLookup = self.reverseMapping(self.dataModel)
	def reverseMapping (self, map):
		reverseMap ={}
		for valKey in map:
		    for val in map[valKey]:
		        reverseMap[val]=valKey
		return reverseMap

	def computeStats(self):
		# precompute statistics
		def cardinality(df,columnName):
			return len(df[columnName].unique())
		self.cardinality = {}
		for dimension in self.dataModel["dimension"]:
			self.cardinality[dimension]=cardinality(self.df,dimension)
		
		