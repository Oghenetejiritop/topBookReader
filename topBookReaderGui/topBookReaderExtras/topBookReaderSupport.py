
#module with supportive classes
from wx import FontData

class UniqueList:
    '''
    a list that functions like a set (stores only unique items).
    '''

    def __init__(self, bookFile, list):
        self.__list = list
        self.__bookFile = bookFile

    def append(self, item):    #append item to the list uniquely
        #remove an existing item from the list and inserts it at position 0
        if item in self.__list:
            self.__list.remove(item)
        self.__list.insert(0, item)

    def delete(self, index):    #delete an item from the list
        self.__list.pop(index)

    def clearAll(self):    #clear all items from the list
        self.__list.clear()

    def numList(self, limit=15):    #add a number to each item of the list and set a limit to its items
        newList = []
        for number, item in enumerate(self.__list):
            self.__bookFile.insertFileTemp(item)
            if number == limit:
                break
            newList.append(f'{number + 1}. {self.__bookFile.getFileTempName()} - File Path: {self.__bookFile.getTempFileSource()}: {item}')
        return newList

    def selectItem(self, index):    #access the highlighted index value
        return self.__list[index]

    #checks if the list is empty
    def isEmpty(self):
        return len(self.__list) == 0

    def output(self):    #return the list
        return self.__list


#class for the font data serialization
class SerializedFontData:
        fontData = FontData()

