
#for .docx files
from docx import Document

from topBookReaderGui.topBookReaderBookFormats.abstractBookFormat import AbstractBookFormat

class TopBookReaderDocx(AbstractBookFormat):

    def __init__(self, file):
        super().__init__()
        self.insertFile(file)
        self.__openDocx = Document(self.getFileSource())
        self.__docxParagraphs = [parag.text for parag in self.__openDocx.paragraphs]

    #access the file
    def openFile(self):
        return '\n'.join(self.__docxParagraphs)