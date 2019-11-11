import pandas as pd
import json
class Dataset:
	def __init__(self,filename):
		self.filename = filename
		self.df = self.loadCSV()
		self.dataType = self.getDataType()
		self.dataModel = self.getDataModel()
		# self.df_json  = self.df.to_json(orient='records')
		self.computeStats()

	def __repr__(self):
		return f"<Dataset Obj: {str(self.filename)}>"

	def loadCSV(self):
		df = pd.read_csv(self.filename)
		return df

	def getDataType(self):
		df = self.df
		dataType = {
			"quantitative":list(df.dtypes[df.dtypes=="float64"].keys()),
			"categorical":list(df.dtypes[df.dtypes=="object"].keys()),
			"ordinal":list(df.dtypes[df.dtypes=="int64"].keys())
		}
		return dataType
	def getDataModel(self):
		dataModel = {
			"measure":self.dataType["quantitative"],
			"dimension":self.dataType["ordinal"]+self.dataType["categorical"]
		}
		return dataModel
	def computeStats(self):
		# precompute statistics
		def cardinality(df,columnName):
			return len(df[columnName].unique())
		self.cardinality = {}
		for dimension in self.dataModel["dimension"]:
			self.cardinality[dimension]=cardinality(self.df,dimension)
		
		