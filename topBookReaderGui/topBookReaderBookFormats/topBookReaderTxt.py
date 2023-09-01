
'''
* Coding: UTF-8
* Author: Oghenetejiri Peace Onosajerhe (peaceonosajerhe@gmail.com).
* topBookReaderTxt.py
* A part of TOP BOOK Reader.
* Licensed under the Massachusetts Institute of Technology (MIT);
* Copyright (C) 2023 Oghenetejiri Peace Onosajerhe.
'''


from topBookReaderGui.topBookReaderBookFormats.abstractBookFormat import AbstractBookFormat

#for .txt files
class TopBookReaderTxt(AbstractBookFormat):
    '''
    this class extends from the AbstractBookFormat class; enabling it to handle text file.
    Has  a parameter (file)  that requires str for the file path.
    '''

    def __init__(self, file):
        super().__init__()

        #insert the file
        self.insertFile(file)
        self.__openTxt = open(self.getFileSource(), 'r')    #sstores the open file
        self.__readTxt = self.__openTxt.read()    #saves the content here
        self.__openTxt.close()    #closes the file

    #access the file
    def openFile(self):
        return self.__readTxt