
'''
* Coding: UTF-8
* Author: Oghenetejiri Peace Onosajerhe (peaceonosajerhe@gmail.com).
* topBookReaderPdf.py
* A part of TOP BOOK Reader.
* Licensed under the Massachusetts Institute of Technology (MIT);
* Copyright (C) 2023 Oghenetejiri Peace Onosajerhe.
'''


from pdfplumber import open

from topBookReaderGui.topBookReaderBookFormats.abstractBookFormat import AbstractBookFormat

#for .pdf files
class TopBookReaderPdf(AbstractBookFormat):
    '''
    this class extends from the AbstractBookFormat class; enabling it to handle pdf.
    Has  a parameter (file)  that requires str for the file path.
    '''

    def __init__(self, file):
        super().__init__()

        #insert the file
        self.insertFile(file)
        self.__openPdf = open(self.getFileSource())    #opens the file
        self.__totalPages = len(self.__openPdf.pages)    #stores the total pages

    #access the file
    def openFile(self):
        pdfText = self.__openPdf.pages[self.getPageNumber()]
        return pdfText.extract_text()

    #method that gets the number of total pages
    def getTotalPages(self):
        return self.__totalPages

    #method that goes  to previous page
    def previousPage(self):
        #don't change if this is the 1st page
        if self.getPageNumber() == 0:
            self.setPageNumber(0)
        else:    #otherwise, switch to the previous page
            self.setPageNumber(self.getPageNumber() -1)
        return self.openFile()

    #    method that goes  to next page
    def nextPage(self):
        #don't change page if this is the last page
        if self.getPageNumber() == self.__totalPages -1:
            self.setPageNumber(self.__totalPages -1)
        else:    #otherwise, switch to the next page
            self.setPageNumber(self.getPageNumber() + 1)
        return self.openFile()
