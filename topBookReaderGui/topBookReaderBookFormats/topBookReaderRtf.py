

'''
* Coding: UTF-8
* Author: Oghenetejiri Peace Onosajerhe (peaceonosajerhe@gmail.com).
* topBookReaderRtf.py
* A part of TOP BOOK Reader.
* Licensed under the Massachusetts Institute of Technology (MIT);
* Copyright (C) 2023 Oghenetejiri Peace Onosajerhe.
'''


from topBookReaderGui.topBookReaderBookFormats.abstractBookFormat import AbstractBookFormat

#for .rtf files
class TopBookReaderRtf(AbstractBookFormat):
    '''
    this class extends from the AbstractBookFormat class; enabling it to handle rtf.
    Has  a parameter (file)  that requires str for the file path.
    '''

    def __init__(self, file):
        super().__init__()

        #insert the file
        self.insertFile(file)
        self.__openRtf = open(self.getFileSource(), 'r')

    #access the file
    def openFile(self):
        readRtf = self.__openRtf.read()
        self.__openRtf.close()
        return readRtf