import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from processing import Processing
from continent import Continent
from data import Data

#inherits from Processing class 
class Task2(Processing):

    #constructor
    def __init__(self,data):
        super().__init__(data)
        self.data = data
    
  
    #This method is for returning the occurences of visits from countires to a specific document
    def countriesForDoc(self, UUID):

        #try catch to catch errors raised

        try:
            self.checkForDocument(UUID)
            #this dictionary is for all the conditions applied to the dataframe
            conditionDic = {
                "read": "event_type"
            }

            # call processing count occurences on loaded in data, for a specfic document UUID,
            # with conditions in dictionary applied, counting visitor_country
            result = self.countOccurences(self.data, conditionDic, "visitor_country", UUID)

            #return result 
            return result
        except Exception as e:
            raise Exception(e)



    #This method is for returning the occurences of visits from continents to a specific document
    def continentsForDoc(self, UUID):
        try:
            self.checkForDocument(UUID)
            #create a new a continent object
            cont = Continent()

            #add Continents Attribute to dataframe
            cont.setContinent(self.data)

            #set conditions in dictionary
            #event_type must be read
            conditionDic = {
                "read": "event_type"
            }

            #call countOccurences on data loaded, on document UUID, with conditions in dictionary,
            #counting Continents
            result = self.countOccurences(self.data, conditionDic, "Continents", UUID)

            #return Result
            return result

        except Exception as e:
            raise Exception(e)





        
        

    

