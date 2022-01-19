import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

#high level methods tasks reuse


class Processing():

    #constructor
    def __init__(self, data):
        self.data = data

    
    #check a document exists 
    def checkForDocument(self, UUID):
        #check for how instances with that document ID
        targetDocumentPD = self.data[self.data['env_doc_id'] == UUID]
        
        #if less or equal to zero raise error
        if len(targetDocumentPD) <= 0:
            raise Exception("Error: Document Not Found")
        else:
            #else return
            return targetDocumentPD



    #check a visitor exists 
    def checkForVisitor(self, visitorUUID):
        #check for how instances with that document ID
        targetDocumentPD = self.data[self.data['visitor_uuid'] == visitorUUID]
        
        #if less or equal to zero raise error
        if len(targetDocumentPD) <= 0:
            raise Exception("Error: Visitor Not Found")
        else:
            #else return
            return targetDocumentPD





    #This method is for counting occurences
    #It takes the dataframe
    #The document ID
    # A Dictionary with all the conditions to be applied to the dataframe 
    # the value to be counted
    def countOccurences(self, data, conditionDic, valueCounted, docID=None):
            #try catch
            try:
                if docID is not None:
                    #get all the instances of specific doc id 
                    newdata = data[data["env_doc_id"] == docID]
                else:
                    newdata = data
                
                
                #for all conditions in the dictionary
                for i in conditionDic.items():

                    #apply conditon to dataframe
                    newdata= newdata[(newdata[i[1]] == i[0])]
                    
                    #if there is no instances after condions have been applied then throw error
                    if newdata.shape[0] <= 0:
                        raise Exception("Error: No instances that match these conditions")
        
                #get value counts of the attribute specified
                counts = newdata[valueCounted].value_counts()

                #return counts
                return counts

            except Exception as e: 
                raise Exception(e)


    #This method is for plotting occurences
    def plotOccur(self, result, xtitle, title, filePath, ytitle=None):
        #consistent style
        plt.style.use('ggplot')

        #create plot
        result.plot(kind = "bar")

        #set title to document ID 
        plt.title(title)

        #set x label to choose title
        plt.xlabel(xtitle)

        if ytitle is not None:
            plt.ylabel(ytitle)
        else:
            #set y to title to frequency
            plt.ylabel('Frequency')

        #save to filepath given
        plt.savefig(filePath + title + '.png')

        plt.show()



    #This method returns either the documents a visitors has read
    # or the visitors of a document depending on what option is selected
    def documentsOrReaders(self, UUID, option):

        #check the option selected
        if option == "readers":
            #set conditions
            conditions = ["env_doc_id", "visitor_uuid"]
        else: 
            #set conditions
            conditions = ["visitor_uuid", "env_doc_id"]

        #only interested in readers
        documents = self.data[(self.data["event_type"] == "read")]
    
        #return instances that meet the condition of either 
        #equalling the document or visitor id specified
        documents = documents[documents[conditions[0]] == UUID]

        #check there is results returned
        if documents.shape[0] <= 0: 
            #throw exception 
            raise Exception("Error: No entires that match your query")
        else:
            #drop all duplicate documents or visitors depending on what option
            documents = documents.drop_duplicates(subset=[conditions[1]])

        #return result
        return documents




    #this is a helper function for also likes method of task 5 when a visitor has been specified
    #returns the unsorted array of alsolikesdocuments 
    # and the dictionary of all the readers and the documents they have read for a specified document 
    def alsoLikesVisitorHelper(self, visitorUUID, UUID, readers):
        #documents a reader has read dictionary
        documentsOfReaderDict = {}

        #makes array for the all other documents read by the readers of input document
        alsoLikesDocuments = []

        #for all readers of the input document 
        for i in readers:
            #if doesnt equal the supplied visitor ID then
            if i != visitorUUID:
                #return all documents they have read
                documents = self.documentsOfReaders(i)

                #just return the document ID 
                documents = documents["env_doc_id"]

                #add it to dict
                documentsOfReaderDict[i] = documents
            else:
                #if target visitor
                #drop all other documents they have read 
                #set it so the target visitor ID has only read the target document
                documentsOfReaderDict[i] = [UUID]

            #append the array of documents read by that reader to the alsolikesDocument array
            alsoLikesDocuments =  alsoLikesDocuments + list(documents.to_numpy())

        return alsoLikesDocuments, documentsOfReaderDict


    #this is a helper function for also likes method of task 5 when a visitor has not been specified
    def alsoLikesNoVisitorHelper(self, readers):

        #documents a reader has read dictionary
        documentsOfReaderDict = {}

    
        #makes array for the all other documents read by the readers of input document
        alsoLikesDocuments = []


        #for all readers of the input document 
        for i in readers:
            #return all documents they have read
            documents = self.documentsOfReaders(i)

            #just return the document ID 
            documents = documents["env_doc_id"]

            documentsOfReaderDict[i] = documents

            #append the array of documents read by that reader to the alsolikesDocument array
            alsoLikesDocuments =  alsoLikesDocuments + list(documents.to_numpy())


        return alsoLikesDocuments, documentsOfReaderDict



    #This is a helper function for the graph generation function of task 5 pretty print with a visitor ID specified 
    def prettyPrintVisitorHelper(self, readers, targetVisitor, dot):
        #for i in readers
        for i in range(len(readers)):
            #get current reader
            reader = str(readers[i])
            #if it equals target visitor
            if reader == targetVisitor:
                #green node
                dot.node(str(reader), reader[-4:], shape="box", style="filled" , fillcolor="green", color="green")
            else:
                dot.node(str(reader), reader[-4:], shape="box")




    #this is a helper function for the graph generation function of task 5 pretty print with no visitor ID specified
    def prettyPrintNoVisitorHelper(self, readers, dot):
        #create nodes for all readers
        for i in range(len(readers)):
            reader = str(readers[i])
            dot.node(str(reader), reader[-4:], shape="box")


    
