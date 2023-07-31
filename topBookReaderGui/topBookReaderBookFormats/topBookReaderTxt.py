
#for .txt files

from topBookReaderGui.topBookReaderBookFormats.abstractBookFormat import AbstractBookFormat

class TopBookReaderTxt(AbstractBookFormat):

    def __init__(self, file):
        super().__init__()
        self.insertFile(file)
        self.__openTxt = open(self.getFileSource(), 'r')
        self.__readTxt = self.__openTxt.read()
        self.__openTxt.close()

    #access the file
    def openFile(self):
        return self.__readTxt