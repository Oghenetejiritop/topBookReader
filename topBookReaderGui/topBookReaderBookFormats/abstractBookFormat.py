
from abc import ABC, abstractmethod

class AbstractBookFormat(ABC):
    '''  This class serves as base class for all file formats.  '''

    def __init__(self):
        self.__pageNumber = 0

    #methods defined 

    #insert the file
    def insertFile(self, file):
        self.__fileSource = file.replace('\\', '/')    #replaces all blackslashes with forward slashes and stores here
        self.__fileExtension = self.__fileSource[self.__fileSource.rindex('.'):]    #stores the file extension here
        self.__fileName = self.__fileSource[self.__fileSource.rindex('/') +1:].replace(self.__fileExtension, '')

    #method that handles temporary insertion of file
    def insertTempFile(self, file):
        self.__tempFileSource = file.replace('\\', '/')    #replaces all blackslashes with forward slashes and stores here
        fileExtension = self.__tempFileSource[self.__tempFileSource.rindex('.'):]    #stores the file extension here
        self.__tempFileName = self.__tempFileSource[self.__tempFileSource.rindex('/') +1:].replace(fileExtension, '')

    #get the file name
    def getFileName(self):
        return self.__fileName

    #get the temporary file name
    def getTempFileName(self):
        return self.__tempFileName

    #get the absolute file path
    def getFileSource(self):
        return self.__fileSource

    #get the temporary absolute file path
    def getTempFileSource(self):
        return self.__tempFileSource

    #get the file type
    def getFileExtension(self):
        return self.__fileExtension

    @abstractmethod
    #access the file
    def openFile(self):
        pass

    #set a new page number
    def setPageNumber(self, number):
        self.__pageNumber = number

    #retrieve the page number
    def getPageNumber(self):
        return self.__pageNumber

    #get the number of total pages
    def getTotalPages(self):
        return self.__pageNumber + 1

    #go to the previous page if supported
    def previousPage(self):
        return self.openFile()

    #go to the next page if supported
    def nextPage(self):
        return self.openFile()
