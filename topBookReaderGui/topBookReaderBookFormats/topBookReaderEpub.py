
'''
* Coding: UTF-8
* Author: Oghenetejiri Peace Onosajerhe (peaceonosajerhe@gmail.com).
* topBookReaderEpub.py
* A part of TOP BOOK Reader.
* Licensed under the Massachusetts Institute of Technology (MIT);
* Copyright (C) 2023 Oghenetejiri Peace Onosajerhe.
'''


import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup

from topBookReaderGui.topBookReaderBookFormats.abstractBookFormat import AbstractBookFormat

#for .epub files
class TopBookReaderEpub(AbstractBookFormat):
    '''
    this class extends from the AbstractBookFormat class; enabling it to handle epub document.
    Has  a parameter (file)  that requires str for the file path.
    '''

    def __init__(self, file):
        super().__init__()

        #insert the file
        self.insertFile(file)
        #open the epub file
        self.__openEpub = epub.read_epub(self.getFileSource())
        self.__totalWordsLength = lambda words: len(words.split())    #little function that retrieves length of given words
        #get the list of contents
        self.__contents = list(self.__openEpub.get_items_of_type(ebooklib.ITEM_DOCUMENT))
        self.__epubProperties = {content: self.__totalWordsLength(self.__extractEpubContent(content)) for content in self.__contents}
        self.__pageDeterminer = 290
        #set the pages
        self.__pages = []
        self.__setPages()
        #get the total pages
        self.__totalPages = len(self.__pages)

    #method that determines possible number of pages
    def __determinePages(self, totalWords):
        return (totalWords // self.__pageDeterminer) if totalWords % self.__pageDeterminer  == 0 else (totalWords // self.__pageDeterminer + 1)

    def __extractEpubContentChapterTitle(self, chapter):
        soup = BeautifulSoup(chapter.get_body_content(), 'html.parser')
        text = [para.get_text() for para in soup.find_all('title')]
        return ''.join(text)

    #method that extracts the epub content
    #accepts one parameter: chapter (eppub object)
    def __extractEpubContent(self, chapter):
        soup = BeautifulSoup(chapter.get_content(), 'html.parser')    #renders it as html content
        #scrape out the html contents
        content = soup.find()
        return content.get_text()     #returns the refined content

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
        #loop through the epubProperties and extract each content
        for content in self.__epubProperties:
            text = self.__extractEpubContent(content)    #stores the extracted content
            #append the text to the pages list if the current text's length <= the pageDeterminer
            if self.__epubProperties[content] <= self.__pageDeterminer:
                print(self.__extractEpubContentChapterTitle(content))
                self.__pages.append(text)
            else:    #otherwise,
                #create extra pages if the page Determiner > length of text.
                print(self.__extractEpubContentChapterTitle(content))
                for pageCount in range(self.__determinePages(self.__epubProperties[content])):
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
