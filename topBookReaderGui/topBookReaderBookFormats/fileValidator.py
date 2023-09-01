
'''
* Coding: UTF-8
* Author: Oghenetejiri Peace Onosajerhe (peaceonosajerhe@gmail.com).
* fileValidator.py
* A part of TOP BOOK Reader.
* Licensed under the Massachusetts Institute of Technology (MIT);
* Copyright (C) 2023 Oghenetejiri Peace Onosajerhe.
'''


from topBookReaderGui.topBookReaderBookFormats.abstractBookFormat import AbstractBookFormat
from topBookReaderGui.topBookReaderBookFormats.topBookReaderDocx import TopBookReaderDocx
from topBookReaderGui.topBookReaderBookFormats.topBookReaderEpub import TopBookReaderEpub
from topBookReaderGui.topBookReaderBookFormats.topBookReaderPdf import TopBookReaderPdf
from topBookReaderGui.topBookReaderBookFormats.topBookReaderRtf import TopBookReaderRtf
from topBookReaderGui.topBookReaderBookFormats.topBookReaderTxt import TopBookReaderTxt

#for the file validation
class FileValidator(AbstractBookFormat):
    '''  this class extends from the AbstractBookFormat class; enabling it to handle various document formats with their respective file objects.  '''

    def __init__(self):
        super().__init__()
        #map each file extention with their file object
        self.__fileExtensions = {
        '.docx': TopBookReaderDocx,
        '.epub': TopBookReaderEpub,
        '.pdf': TopBookReaderPdf,
        '.rtf': TopBookReaderRtf,
        '.txt': TopBookReaderTxt,
        }

    #overwrite the insertFile method
    #accepts one parameter: file (str)
    def insertFile(self, file):
        super().insertFile(file)
        self.__currentFile = self.__fileExtensions[self.getFileExtension()](self.getFileSource())

    #access the file
    def openFile(self):
        return self.__currentFile.openFile()

    #go to previous page
    def previousPage(self):
        return self.__currentFile.previousPage()

    #go to next page
    def nextPage(self):
        return self.__currentFile.nextPage()

    #set a new page number
    #accepts one parameter: number (int)
    def setPageNumber(self, number):
        self.__currentFile.setPageNumber(number)

    #retrieve the page number
    def getPageNumber(self):
        return self.__currentFile.getPageNumber()

    #get the number of total pages
    def getTotalPages(self):
        return self.__currentFile.getTotalPages()

'''test code
a = FileValidator()
a.insertFile("c:\\documents\\dreams.docx")
print(a.getFileSource())
print(a.getFileExtension())
print(a.getFileName())
a.nextPage()
#a.nextPage()
#a.previousPage()
print('opened file', a.openFile())'''