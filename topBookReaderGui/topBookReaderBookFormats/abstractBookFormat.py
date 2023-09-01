
'''
* Coding: UTF-8
* Author: Oghenetejiri Peace Onosajerhe (peaceonosajerhe@gmail.com).
* abstractBookFormat.py
* A part of TOP BOOK Reader.
* Licensed under the Massachusetts Institute of Technology (MIT);
* Copyright (C) 2023 Oghenetejiri Peace Onosajerhe.
'''


from abc import ABC, abstractmethod

class AbstractBookFormat(ABC):
    '''  This class serves as base class for all file formats.  '''

    def __init__(self):
        self.__pageNumber = 0

    #methods defined 

    #method used for the insertion of file
    #accepts one parameter: file (str)
    def insertFile(self, file):
        #get the file path
        self.__fileSource = file.replace('\\', '/')    #replaces all blackslashes with forward slashes and stores it here
        self.__fileExtension = self.__fileSource[self.__fileSource.rindex('.'):]    #stores the file extension here
        self.__fileName = self.__fileSource[self.__fileSource.rindex('/') +1:].replace(self.__fileExtension, '')    #stores the file name

    #method that handles temporary insertion of file
    #accepts one parameter: file (str)
    def insertTempFile(self, file):
        self.__tempFileSource = file.replace('\\', '/')    #replaces all blackslashes with forward slashes and stores here
        fileExtension = self.__tempFileSource[self.__tempFileSource.rindex('.'):]    #stores the file extension here
        self.__tempFileName = self.__tempFileSource[self.__tempFileSource.rindex('/') +1:].replace(fileExtension, '')    #stores the file name

    #method that gets the file name
    def getFileName(self):
        return self.__fileName

    #method that gets the temporary file name
    def getTempFileName(self):
        return self.__tempFileName

    #method that returns the absolute file path
    def getFileSource(self):
        return self.__fileSource

    #method that returns the temporary absolute file path
    def getTempFileSource(self):
        return self.__tempFileSource

    #method that returns the file type
    def getFileExtension(self):
        return self.__fileExtension

    @abstractmethod
    #an abstract method that accesses the file
    def openFile(self):
        pass

    #method that sets a new page number
    #accepts one parameter: number (int)
    def setPageNumber(self, number):
        self.__pageNumber = number

    #method that retrieves the page number
    def getPageNumber(self):
        return self.__pageNumber

    #method that gets the number of total pages
    def getTotalPages(self):
        return self.__pageNumber + 1

    #method that goes to the previous page if supported
    def previousPage(self):
        return self.openFile()

    #method that goes  to the next page if supported
    def nextPage(self):
        return self.openFile()
