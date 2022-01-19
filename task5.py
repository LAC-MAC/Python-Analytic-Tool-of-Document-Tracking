import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from processing import Processing
from continent import Continent
from data import Data
import graphviz


class Task5(Processing):
    
     #constructor
    def __init__(self,data):
        super().__init__(data)
        
    #This method gets the readers of a specific document
    def readersOfDocument(self, UUID):
        try:
            self.checkForDocument(UUID)
        except:
            print("error")


        readers = self.documentsOrReaders(UUID, "readers")
       
        return readers


    #This method gets the documents read by a specific reader
    def documentsOfReaders(self, visitorUUID):

        try:
            self.checkForVisitor(visitorUUID)
        except:
            print("error")

        documents = self.documentsOrReaders(visitorUUID, "documents")
       
        return documents


    #This methods gets the also like documents of a specific document
    def alsoLikes(self,task_id, UUID, visitorUUID=None, sorter=None):
            #return all readers of a document
            readers = self.readersOfDocument(UUID)
            readers = (readers["visitor_uuid"]).to_numpy()

            #if no visitor ID passed then
            if visitorUUID is not None:
                self.checkForVisitor(visitorUUID)
                #call helper method in processing
                alsoLikesDocuments, documentsOfReaderDict = self.alsoLikesVisitorHelper(visitorUUID, UUID, readers)
            else:
                #call helper method in processing
                alsoLikesDocuments, documentsOfReaderDict = self.alsoLikesNoVisitorHelper(readers)

            #remove all the instances of the input document from alsoLikesDocuments
            try:
                while True:
                    alsoLikesDocuments.remove(UUID)
            except ValueError:
                pass
            
            if sorter is not None:
                #call the sorting function on the alsoLikesDocuments array
                sortedDocs  = sorter(alsoLikesDocuments)
            else:
                sortedDocs  = self.sorter(alsoLikesDocuments)

            # if specified taskid is 6 then produce graph            
            if task_id == "6":    
                #pretty print it in the graph (task 6)
                self.prettyPrint(readers, sortedDocs, documentsOfReaderDict, UUID, visitorUUID)

            #return sorted array
            
            return sortedDocs





    
    #This methods generates the graphs for also likes
    def prettyPrint(self, readers, sortedDocs, documentsOfReadersDict, targetDoc, targetVisitor=None): 
        #create graph
        dot = graphviz.Digraph(("alsoLikesGraph"+targetDoc), comment="AlsoLikesGraph")

        #set rank style and size 
        dot.attr(rankdir='TB', size='8,5')

        #set format to ps
        #dot.format = 'ps'

        #called method to make graph key
        self.range(dot)

        #if a visitor parameter is included call the corresponding helper method
        if targetVisitor is not None:
            self.prettyPrintVisitorHelper(readers, targetVisitor, dot)
        else:
            self.prettyPrintNoVisitorHelper(readers, dot)

  
        #set up target document node
        dot.node(targetDoc, targetDoc[-4:], style="filled" ,fillcolor="green", color="green", shape="circle")
        
        #loop through all documents
        for i in range(len(sortedDocs.items())):
            document = str(list(sortedDocs.items())[i][0])
            #set up node for each document
            dot.node(document, document[-4:], shape="circle")

        #loop through list of dictionary
        items = list(documentsOfReadersDict.items())
        for i in range(len(items)):
            #create edges for reader to each document they have read that is in also likes documents
            documents = list(items[i][1])
            for j in range(len(documents)):
                try:
                    sortedDocs[documents[j]]
                    dot.edge(items[i][0], documents[j])

                except:
                    pass
            dot.edge(items[i][0],targetDoc)
                

        


        

        #render the document out
        dot.render(directory='doctest-output/', view=True)

        

    

    #sorter function based on how many readers have read a document

    def sorter(self, alsoLikeDocuments):
        #sorted dict
        dictReadersPerDocuments = {}

        #iterator for documents in also likes unsorted
        for i in alsoLikeDocuments:

            #add document UUID and the number of readers of that document
            dictReadersPerDocuments[i] = (self.readersOfDocument(i)).shape[0]

        #sort the dictionary into decsending order 
        
        sortedDic = {k: v for k, v in sorted(dictReadersPerDocuments.items(), key=lambda x:x[1], reverse=True)[:10]}

        print(sortedDic)
        
        return(sortedDic)


    #this function is for setting up left side key of the graph
    #shows which side is documents and which is readers as well as size of file
    def range(self, dot):
        #get how many instances and round
        label = int(self.data.shape[0])

        
        #python really needs a use case
        if label == 102401 :
            label = "100k"
        elif label == 400000:
            label = "400k"
        elif label == 600000:
            label = "600k"
        else:
            label = "3M"


        #set up a readers node 
        dot.node("readers", "Readers", shape="none", rank="readers")

        #set up a documents node 
        dot.node("documents", "Documents", shape="none", rank="documents")

        #create an edge between them
        dot.edge("readers", "documents", label=("Size:" + label))
        

