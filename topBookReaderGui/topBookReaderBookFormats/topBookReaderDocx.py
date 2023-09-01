
'''
* Coding: UTF-8
* Author: Oghenetejiri Peace Onosajerhe (peaceonosajerhe@gmail.com).
* topBookReaderDocx.py
* A part of TOP BOOK Reader.
* Licensed under the Massachusetts Institute of Technology (MIT);
* Copyright (C) 2023 Oghenetejiri Peace Onosajerhe.
'''


from docx import Document

from topBookReaderGui.topBookReaderBookFormats.abstractBookFormat import AbstractBookFormat

#for .docx files
class TopBookReaderDocx(AbstractBookFormat):
    '''
    this class extends from the AbstractBookFormat class; enabling it to handle word document.
    Has  a parameter (file)  that requires str for the file path.
    '''

    def __init__(self, file):
        super().__init__()

        #insert the file
        self.insertFile(file)
        self.__openDocx = Document(self.getFileSource())    #opens the file
        self.__docxParagraphs = [parag.text for parag in self.__openDocx.paragraphs]    #extracts all text from the opened document
        #get the whole document
        self.__wholeDocument = '\n'.join(self.__docxParagraphs)
        #set the pages
        self.__pageDeterminer = 290
        self.__pages = []
        self.__setPages()
        #get the total pages
        self.__totalPages = len(self.__pages)

    #method that determines possible number of pages
    def __determinePages(self, totalWords):
        return (totalWords // self.__pageDeterminer) if totalWords % self.__pageDeterminer  == 0 else (totalWords // self.__pageDeterminer + 1)

    #method that extracts a new page
    #accepts three parameters: content (str), character(str) and pos (int)
    def __extractPages(self, content, character, pos):
        total = 0
        #iterate through the length of the content
        for index in range(len(content)):
            #increment total by 1; when the index value matches the character
            if content[index] == character:
                total += 1
            #return the index when the position is same with total
            if pos == total:
                return index
        #otherwise, return -1
        return -1

    #method that creates the page list
    def __setPages(self):
        text = self.__wholeDocument    #stores the document content
        lengthOfWords = len(text.split())    #stores the length of the document content
        #append the text to the pages list if the current text's length <= the pageDeterminer
        if lengthOfWords <= self.__pageDeterminer:
            self.__pages.append(text)
        else:    #otherwise,
            #create extra pages if the page Determiner > length of text.
            for pageCount in range(self.__determinePages(lengthOfWords)):
                spaceIndex = self.__extractPages(text, ' ', self.__pageDeterminer)
                self.__pages.append(text[:spaceIndex])
                text = text[spaceIndex:]

    #access the file
    def openFile(self):
        return self.__pages[self.getPageNumber()]

    #method that gets the number of total pages
    def getTotalPages(self):
        return self.__totalPages

    #method that goes to previous page
    def previousPage(self):
        #don't change if this is the 1st page
        if self.getPageNumber() == 0:
            self.setPageNumber(0)
        else:    #otherwise, switch to the previous page
            self.setPageNumber(self.getPageNumber() -1)
        return self.openFile()

    #method that goes  to next page
    def nextPage(self):
        #don't change page if this is the last page
        if self.getPageNumber() == self.__totalPages -1:
            self.setPageNumber(self.__totalPages -1)
        else:    #otherwise, switch to the next page
            self.setPageNumber(self.getPageNumber() + 1)
        return self.openFile()