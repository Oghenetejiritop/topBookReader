
#dialog for the recent books opened
from os import path

import wx

from topBookReaderGui.topBookReaderListDisplay import TopBookReaderListDisplay as ListDisplay

isExistingPath = path.exists    #alias this function

def showMessage(msg):
    dlg = wx.MessageDialog(None, msg, 'Missing File Error!', style=wx.ICON_EXCLAMATION)
    dlg.ShowModal()
    dlg.Destroy()


class TopBookReaderRecentBooksDialog(wx.Dialog):

    def __init__(self, parent, bookFile, list):
        super().__init__(None, wx.ID_ANY, title='Recent Books')

        #the vertical sizer for the Components
        self.__vSizer = wx.BoxSizer(wx.VERTICAL)

        self.__parent = parent
        self.__bookFile = bookFile
        self.__list = list
        self.__dictPaths = self.__parent.getRecentBookInfo()
        self.__dictBookmarks = self.__parent.getBookmarks()

        self.__label = wx.StaticText(self, -1, 'Select an item')
        self.__listDisplay = ListDisplay(self, 'S/N', 'File Name', 'File Path')    #instantiate the ListDisplay object to show recently opened books.
        self.__vSizer.Add(self.__listDisplay, 1, wx.EXPAND)

        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.on_open, self.__listDisplay)
        #insert the default items to the list display
        self.__insertDefaultItem()

        self.__showBtn()


    #methods defined
    #insert default item to the list display if not empty
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

    #structure for each button property
    def __buttonInfo(self):
        return (
        ('&Open item', self.on_open),
        ('&Delete item', self.on_delete),
        ('&Clear all', self.on_clear),
        )

    def __implementBtn(self, id, label, evtHandler):
        btn = wx.Button(self, id, label, pos=(100, 50), size=(200, 500))
        self.Bind(wx.EVT_BUTTON, evtHandler, btn)
        return btn

    def __showBtn(self):
        #determine the state of the buttons if the list is empty or not
        emptyDecider = False if self.__list.isEmpty() else True
        #unpack the __buttonInfo
        for label, evtHandler in self.__buttonInfo():
            btn = self.__implementBtn(wx.ID_ANY, label, evtHandler).Enable(emptyDecider)
            #add each button to the vSizer
            self.__vSizer.Add(btn, 0, wx.ALL | wx.CENTER, 5)
        self.__vSizer.Add(wx.Button(self, wx.ID_CANCEL, 'Cancel'), 0, wx.ALL | wx.CENTER, 5)

        self.__vSizer.SetSizeHints(self)
        self.SetSizer(self.__vSizer)

    #method that handles deletion of an item
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
