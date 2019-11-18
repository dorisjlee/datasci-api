import pandas as pd
import json
class Dataset:
	def __init__(self,filename, schema=[]):
		self.filename = filename
		self.df = self.loadCSV()
		self.attrList = list(self.df.columns)
		self.schema = schema
		# self.df_json  = self.df.to_json(orient='records')
		self.dataTypeLookup = {}
		self.dataType = {}
		self.computeDataType()
		self.dataModelLookup = {}
		self.dataModel = {}
		self.computeDataModel()
		self.computeStats()

	def __repr__(self):
		return f"<Dataset Obj: {str(self.filename)}>"

	def loadCSV(self):
		df = pd.read_csv(self.filename)
		return df

	def computeDataType(self):
		# df = self.df
		# self.dataType = {
		# 	"quantitative":list(df.dtypes[df.dtypes=="float64"].keys()) + list(df.dtypes[df.dtypes=="int64"].keys()),
		# 	"categorical":list(df.dtypes[df.dtypes=="object"].keys()),
		# 	"ordinal": [],
		# 	"date":[]
		# }

		for attr in self.attrList:
			if self.df.dtypes[attr]=="float64" or self.df.dtypes[attr]=="int64":
				self.dataTypeLookup[attr]="quantitative"
			elif self.df.dtypes[attr]=="object":
				self.dataTypeLookup[attr]="categorical"
		# Override with schema specified types
		for attrInfo in self.schema:
			key= list(attrInfo.keys())[0]
			self.dataTypeLookup[key]= attrInfo[key]["dataType"]
		# for attr in list(df.dtypes[df.dtypes=="int64"].keys()):
		# 	if self.cardinality[attr]>50:
		self.dataType = self.mapping(self.dataTypeLookup)

	def computeDataModel(self):
		self.dataModel = {
			"measure":self.dataType["quantitative"],
			"dimension":self.dataType["ordinal"]+self.dataType["categorical"]+self.dataType["date"]
		}

		self.dataModelLookup = self.reverseMapping(self.dataModel)

	def mapping(self,rmap):
	    groupMap = {}
	    uniqueVal = list(set(rmap.values()))
	    for val in ["quantitative","ordinal","categorical","date"]:
	        groupMap[val] = list(filter(lambda x:rmap[x]==val,rmap))
	    return groupMap

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
		for dimension in self.df.columns:
			self.cardinality[dimension]=cardinality(self.df,dimension)
		
		