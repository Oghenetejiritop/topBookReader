
#for .rtf files

from topBookReaderGui.topBookReaderBookFormats.abstractBookFormat import AbstractBookFormat

class TopBookReaderRtf(AbstractBookFormat):

    def __init__(self, file):
        super().__init__()

        self.insertFile(file)
        self.__openRtf = open(self.getFileSource(), 'r')

    #access the file
    def openFile(self):
        readRtf = self.__openRtf.read()
        self.__openRtf.close()
        return readRtf