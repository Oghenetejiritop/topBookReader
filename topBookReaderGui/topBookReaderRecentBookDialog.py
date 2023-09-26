
'''
* Coding: UTF-8
* Author: Oghenetejiri Peace Onosajerhe (peaceonosajerhe@gmail.com).
* topBookReaderRecentBooksDialog.py
* A part of TOP BOOK Reader.
* Licensed under the Massachusetts Institute of Technology (MIT);
* Copyright (C) 2023 Oghenetejiri Peace Onosajerhe.
'''


from os import path

from  wx import (Bitmap, BITMAP_TYPE_PNG,
    BoxSizer, ALL, CENTER,  EXPAND, HORIZONTAL, LEFT, VERTICAL,
    Button, BU_EXACTFIT, EVT_BUTTON, EVT_LIST_ITEM_ACTIVATED, Font, FONTFAMILY_DEFAULT, FONTSTYLE_ITALIC, FONTWEIGHT_BOLD, ID_CANCEL,
    Dialog, ICON_EXCLAMATION, MessageDialog,
    StaticText,)

from topBookReaderGui.topBookReaderListDisplay import TopBookReaderListDisplay as ListDisplay

isExistingPath = path.exists    #alias this function

def showMessage(msg):
    dlg = MessageDialog(None, msg, 'Missing File Error!', style=ICON_EXCLAMATION)
    dlg.ShowModal()
    dlg.Destroy()

#dialog for the recent documents opened
class TopBookReaderRecentBooksDialog(Dialog):
    '''
    this class presents the app with recently opened documents
    Accepts three parameters;
    parent: that requires the topBookReaderPanel object.
    bookFile: requires the FileValidator object
    list: takes the UniqueList object as an argument
    '''

    def __init__(self, parent, bookFile, list):
        super().__init__(None, -1, title='Recently Opened Books', size=(500, 400))

        self.__parent = parent
        self.__bookFile = bookFile
        self.__list = list
        self.__dictPaths = self.__parent.getRecentBookInfo()
        self.__dictBookmarks = self.__parent.getBookmarks()    #stores the bookmark history

        #instantiate the box sizers for the components 
        self.__vSizer = BoxSizer(VERTICAL)
        hSizer1 = BoxSizer(HORIZONTAL)
        self.__hSizer2 = BoxSizer(HORIZONTAL)
        hSizer1.Add(StaticText(self, -1, 'Select an item'), 0,  ALL, 5)
        self.__listDisplay = ListDisplay(self, 'S/N', 'File Name', 'File Path')    #instantiate the ListDisplay object to show recently opened books.
        hSizer1.Add(self.__listDisplay, 1, EXPAND | ALL, 10)
        self.__vSizer.Add(hSizer1, 0, ALL)
        self.Bind(EVT_LIST_ITEM_ACTIVATED, self.on_open, self.__listDisplay)
        #insert the default items to the list display
        self.__insertDefaultItem()

        self.__showBtn()


    #methods defined

    #method that inserts default item to the list display if not empty
    def __insertDefaultItem(self):
        self.__listDisplay.DeleteAllItems()
        #insert the serialNumber, file name and path to their respective columns
        for number, path in enumerate(self.__list.output()[:15]):
            self.__bookFile.insertTempFile(path)
            self.__listDisplay.InsertItem(number, f'{number + 1}')
            self.__listDisplay.SetItem(number, 1, self.__bookFile.getTempFileName())
            self.__listDisplay.SetItem(number, 2, self.__bookFile.getTempFileSource())

        #select and set focus on the first item
        self.__listDisplay.Focus(0)
        self.__listDisplay.Select(0, True)

    #method that returns the (label and event handler) for each button  
    def __buttonInfo(self):
        return (
        ('&Open item', self.on_open),
        ('&Remove item', self.on_delete),
        ('&Clear all', self.on_clear),
        )

    #method that implements the button component; 
    #accepts three parameters: id (wx.ID_ANY), label (str) and evtHandler (event handler)
    def __implementBtn(self, id, label, evtHandler):
        btn = Button(self, id, label, style=BU_EXACTFIT)
        self.Bind(EVT_BUTTON, evtHandler, btn)
        return btn

    #the method that displays the button to the screen
    def __showBtn(self):
        #determine the state of the buttons if the list is empty or not
        isEmpty = False if self.__list.isEmpty() else True
        #unpack the __buttonInfo
        for label, evtHandler in self.__buttonInfo():
            #add each button to the hSizer
            btn = self.__implementBtn(-1, label, evtHandler)
            btn.Enable(isEmpty)
            self.__hSizer2.Add(btn, 0, ALL | CENTER, 5)
        self.__hSizer2.Add(Button(self, ID_CANCEL, 'Cancel', style=BU_EXACTFIT), 0, ALL | CENTER, 5)
        self.__vSizer.Add(self.__hSizer2, 0, EXPAND)
        self.__vSizer.SetSizeHints(self)
        self.SetSizer(self.__vSizer)

    #method that handles deletion of an item
    #accepts two parameters index (int) and filePathKey (dictionary key)
    def __delete(self, index, filePathKey):
        self.__listDisplay.DeleteItem(index)    #delete selected item from the list box
        self.__list.delete(index)
        self.__dictPaths.pop(filePathKey)    #remove the filePath key from the dictPaths
        self.__dictBookmarks.pop(filePathKey) if filePathKey in self.__dictBookmarks else None

    #method that handles multiple update for both serialized files and status info
    def __updateNotifier(self):
        #update the serialized files
        self.__parent.updateRecentList(self.__list.output())
        self.__parent.updateRecentBookInfo(self.__dictPaths)
        self.__parent.updateBookmarks(self.__dictBookmarks)
    #update both the displayedContent and statusbar
        self.__parent.displayDefaultValue()
        self.__parent.updateStatusBar()

    #events associated with this class

    #this event accesses the selected item from the list of recent opened books
    def on_open(self, event):
        itemIndex = self.__listDisplay.GetNextSelected(-1)

        if itemIndex == -1:
            return

        fileItem = self.__listDisplay.GetItemText(itemIndex, 2)    #stores the selected file path from the list display
        #display the content of the fileItem if it still exists
        if isExistingPath(fileItem):
            self.__parent.displayContent(fileItem)
            self.Destroy()
            return

        #otherwise, present a non_existing dialog
        self.__bookFile.insertTempFile(fileItem)
        msg = f'It seems the file: {self.__bookFile.getTempFileName()}; from the location: {self.__bookFile.getTempFileSource()} is missing from your device!'
        showMessage(msg)

    #this event deletes an item from the recent opened books
    def on_delete(self, event):
        index = self.__listDisplay.GetNextSelected(-1)    #get the index of the selected item from the list display
        filePathKey = self.__list.selectItem(index)    #store the file path

        #delete the item from the list and     the filePath key from the dictionary
        if index == -1:
            return

        #otherwise, remove the highlighted item
        self.__delete(index, filePathKey)
        self.__insertDefaultItem()    #update the list display
        #update the information
        self.__updateNotifier()

        #also, destroy the dialog if the list is empty
        if self.__list.isEmpty():
            self.Destroy()

    #this event clears all items from the recent opened books
    def on_clear(self, event):
        self.__listDisplay.DeleteAllItems()    #clear all items from the list display
        self.__list.clearAll()
        self.__dictPaths.clear()    #empty the paths dictionary 
        self.__dictBookmarks.clear()    #empty the bookmarks dictionary  
        #update the information
        self.__updateNotifier()
        self.Destroy()
