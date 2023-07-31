
#for .pdf files
from pdfplumber import open

from topBookReaderGui.topBookReaderBookFormats.abstractBookFormat import AbstractBookFormat

class TopBookReaderPdf(AbstractBookFormat):

    def __init__(self, file):
        super().__init__()
        self.insertFile(file)
        self.__openPdf = open(self.getFileSource())
        self.__totalPages = len(self.__openPdf.pages)

    #access the file
    def openFile(self):
        pdfText = self.__openPdf.pages[self.getPageNumber()]
        pdfText = pdfText.extract_text()
        return pdfText

    #get the number of total pages
    def getTotalPages(self):
        return self.__totalPages

    #go to previous page
    def previousPage(self):
        if self.getPageNumber() == 0:
            self.setPageNumber(0)
        else:
            self.setPageNumber(self.getPageNumber() -1)
        return self.openFile()

    #go to next page
    def nextPage(self):
        if self.getPageNumber() == self.__totalPages -1:
            self.setPageNumber(self.__totalPages -1)
        else:
            self.setPageNumber(self.getPageNumber() + 1)
        return self.openFile()
