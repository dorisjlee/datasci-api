from dataObj.dataObj import DataObj
from dataObj.DataObjCollection import DataObjCollection
from dataObj.Column import Column
from dataObj.Row import Row

class Enumeration:
    def __init__(self, xAttributes = [], yAttributes = [], zAttributes = []):
        self.xAttributes = xAttributes
        self.yAttributes = yAttributes
        self.zAttributes = zAttributes

    def GenerateDataObjCollection(self, dataset):
        collection = []
        for xAxis in self.xAttributes:
            for yAxis in self.yAttributes:
                if self.zAttributes:
                    for zAxis in self.zAttributes:
                        # create the data objects
                        dataObj = DataObj(dataset,[Column(xAxis, channel='x'), Column(yAxis, channel='y'), Row(fAttribute=zAxis,fVal='?')])
                        collection.append(dataObj)
                else:
                    dataObj = DataObj(dataset, [Column(xAxis, channel='x'), Column(yAxis, channel='y')])
                    collection.append(dataObj)
        self.collection = DataObjCollection(collection)

    def getDataObjCollection(self):
        return self.collection


def testEnumeration():
    enumeration = Enumeration(["Displacement","Horsepower"],["Weight","Acceleration"],["Name"])
    enumeration.GenerateDataObjCollection()
    vizCollection = enumeration.getDataObjCollection()
    vizCollection.map(DataObj.showMe())
