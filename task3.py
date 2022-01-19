import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from processing import Processing
from browsers import Browsers
from data import Data




#inherits from Processing class 
class Task3(Processing):

    #constructor
    def __init__(self,data):
        super().__init__(data)
        self.data = data

    def browserData(self, UUID=None):

        conditionDic = {
                "read": "event_type"
            }
        if UUID is not None:
            data = self.countOccurences(newdata, conditionDic,"visitor_useragent", UUID)
        else:
            data = self.countOccurences(self.data, conditionDic,"visitor_useragent")

      
        return data


    def GeneralBrowserData(self, UUID=None):
        #create new browser object
        bw = Browsers()
        
        #if they have specified a document id or not
        if UUID is not None:
            newdata = self.data[self.data["env_doc_id"] == UUID]
            if newdata.shape[0] <=0:
                raise Exception("Error: No instances that match these conditions")
            return bw.setBrowsers(newdata)
            
        else:
            return bw.setBrowsers(self.data)
            