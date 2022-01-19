import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from processing import Processing
from continent import Continent
from data import Data


class Task4(Processing):
    #constructor
    def __init__(self,data):
        super().__init__(data)
        self.data = data


    def biggestReaders(self):
        #limit it to pagereadtime events
        readerVisitors = self.data[self.data['event_type'] == "pagereadtime"]

        #return a new dataframe groupy by  the visitor id and sorted by largest event readtime attrubute
        biggestReaders = (readerVisitors[['visitor_uuid', 'event_readtime']].groupby('visitor_uuid').sum()).sort_values(['event_readtime'], ascending=False)

        #get top ten
        biggestReaders = biggestReaders.head(10)

        #return biggest readers
        return biggestReaders







