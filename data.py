import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

from multiprocessing import Pool
import json
from io import StringIO
from itertools import accumulate



class Data:

    def __init__(self, filePath):
        #instantiate the source file path with file path given 
        self.sourceFilePath = filePath

    def makeDataFrame(self):
        #try catch for instiantiation of dataframe
        try:

            

            #create data frame from json file
            dataFrame = pd.read_json(self.sourceFilePath, lines=True)
            

            #return data frame 
            return dataFrame

        except Exception as e:
            #print error
            print(e)
            #raise Exception("Error: Unable To load In Data") 


    def fastest(self):
        datas=[]
        with open(self.sourceFilePath, "r") as json_f:      
            data = json_f.readlines()
        
        with Pool() as p:
            data = p.map(json.loads, data)
        
        p.close()
        p.join()

        return pd.DataFrame(data)









    






  





