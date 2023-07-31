
#for .epub files
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup

from topBookReaderGui.topBookReaderBookFormats.abstractBookFormat import AbstractBookFormat

class TopBookReaderEpub(AbstractBookFormat):

    def __init__(self, file):
        super().__init__()

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

    #determine possible number of pages
    def __determinePages(self, totalWords):
        return (totalWords // self.__pageDeterminer) if totalWords % self.__pageDeterminer  == 0 else (totalWords // self.__pageDeterminer + 1)

    #extract the epub content
    def __extractEpubContentChapterTitle(self, chapter):
        soup = BeautifulSoup(chapter.get_body_content(), 'html.parser')
        text = [para.get_text() for para in soup.find_all('title')]
        return ''.join(text)

    def __extractEpubContent(self, chapter):
        soup = BeautifulSoup(chapter.get_content(), 'html.parser')
        content = soup.find()
        return content.get_text() 

    #extract new pages
    def __extractPages(self, content, character, pos):
        total = 0
        for index in range(len(content)):
            if content[index] == character:
                total += 1
            if pos == total:
                return index
        return -1

    #create a page list
    def __setPages(self):
        #loop through the epubProperties and extract each content
        for content in self.__epubProperties:
            text = self.__extractEpubContent(content)
            if self.__epubProperties[content] <= self.__pageDeterminer:
                print(self.__extractEpubContentChapterTitle(content))
                self.__pages.append(text)
            else:
                print(self.__extractEpubContentChapterTitle(content))
                for pageCount in range(self.__determinePages(self.__epubProperties[content])):
                    spaceIndex = self.__extractPages(text, ' ', self.__pageDeterminer)
                    self.__pages.append(text[:spaceIndex])
                    text = text[spaceIndex:]

    #access the file
    def openFile(self):
        return self.__pages[self.getPageNumber()]

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
