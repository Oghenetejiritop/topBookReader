
'''
* Coding: UTF-8
* Author: Oghenetejiri Peace Onosajerhe (peaceonosajerhe@gmail.com).
* topBookReaderBookmarkListDialog.py
* A part of TOP BOOK Reader.
* Licensed under the Massachusetts Institute of Technology (MIT);
* Copyright (C) 2023 Oghenetejiri Peace Onosajerhe.
'''


import wx

from topBookReaderGui.topBookReaderListDisplay import TopBookReaderListDisplay as ListDisplay

#dialog for the bookmark list of an opened document
class TopBookReaderBookmarkListDialog(wx.Dialog):
    '''
    this class retrieves and display the bookmark history of an opened document.
    Has  a parameter (parent)  that requires the topBookReaderFrame object.
    '''

    def __init__(self, parent):
        self.__parent = parent
        #get the current title
        titleIndex = self.__parent.GetTitle().rfind('-')
        title = self.__parent.GetTitle()[:titleIndex]
        super().__init__(None, wx.ID_ANY, title=f'Bookmark History for {title}')

        #instantiate the horizontal box sizer
        self.__hSizer = wx.BoxSizer(wx.HORIZONTAL)    

        #get the reference to the displayedContent component of the app
        self.__displayedContent = self.__parent.pnl.cloneDisplayedText()

        self.__path = self.__parent.pnl.getFilePath()
        #get the bookmark history
        self.__dictBookmarks = self.__parent.pnl.getBookmarks()
        self.__currentBookmarkList = self.__dictBookmarks.get(self.__path, [])

        self.__label = wx.StaticText(self, -1, 'Select a Bookmark Item')
        self.__listDisplay = ListDisplay(self, 'Bookmark Name', 'Page Number', 'Bookmarked Text')    #instantiate the ListDisplay object to show the bookmark list.
        self.__insertDefaultItem()    #fill the list display with bookmarked info
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.on_open, self.__listDisplay)

        #show the buttons
        self.__showBtn()

    #methods defined

    #method that inserts default item to the list display if not empty
    def __insertDefaultItem(self):
        self.__listDisplay.DeleteAllItems()
        #insert the bookmark's (name, page number and bookmarked text) to their respective columns
        for number, bookmarkItem in enumerate(self.__currentBookmarkList[:10]):
            #call the __insertItem() method
            self.__insertItem(bookmarkItem)
            self.__listDisplay.InsertItem(number, self.__bookmarkName)
            self.__listDisplay.SetItem(number, 1, self.__pageNumber)
            self.__listDisplay.SetItem(number, 2, self.__bookmarkedText)

        #select and set focus on the first item
        self.__listDisplay.Focus(0)
        self.__listDisplay.Select(0, True)

    #method that gets each part of the inserted bookmarked item (name, page number, text and char position)
    #has a parameter (item) which is a string pattern  that has the inserted bookmarked item
    def __insertItem(self, item):
    #get each index component of the inserted bookmarked item 
        nameIndex = item.index(';')
        pageIndex = item.index('-')
        textIndex = item.rindex(';')
        #store the (name, page number, text and char position) in instance variables
        self.__bookmarkName = item[:nameIndex]
        self.__pageNumber = item[nameIndex+2:pageIndex]
        self.__bookmarkedText = item[pageIndex+2:textIndex]
        self.__charPosition = item[textIndex+2:]

    #method that returns the (id, label and event handler) of each button  
    def __buttonInfo(self):
        return (
        ('&Open item', self.on_open),
        ('&Remove item', self.on_remove),
        ('&Clear all', self.on_clear),
        )

    #method that implements the button component; 
    #accepts three parameters: id ( id reference), label (str) and evtHandler (event handler)
    def __implementBtn(self, id, label, evtHandler):
        btn = wx.Button(self, id, label, pos=(100, 50), size=(200, 500))
        self.Bind(wx.EVT_BUTTON, evtHandler, btn)
        return btn

    #the method that displays the button to the screen
    def __showBtn(self):
        #determine the state of the buttons if the list is empty or not
        decider = True if self.__currentBookmarkList else False
        #unpack the __buttonInfo
        for label, evtHandler in self.__buttonInfo():
            btn = self.__implementBtn(wx.ID_ANY, label, evtHandler).Enable(decider)
            #add each button to the vSizer
            self.__hSizer.Add(btn, 0, wx.ALL | wx.CENTER, 5)
        self.__hSizer.Add(wx.Button(self, wx.ID_CANCEL, 'Cancel'), 0, wx.ALL | wx.CENTER, 5)
        self.__hSizer.SetSizeHints(self)
        self.SetSizer(self.__hSizer)

    #method that handles update for the bookmark serialized file
    def __updateNotifier(self):
        self.__parent.pnl.updateBookmarks(self.__dictBookmarks)

    #events associated with this class

    #this event accesses the selected item from the bookmark list 
    def on_open(self, event):
        index = self.__listDisplay.GetNextSelected(-1)
        if index == -1:
            return

        selectedItem = self.__currentBookmarkList[index]
        self.__insertItem(selectedItem)

        insertionPoint = int(self.__charPosition)
        pageNumber = int(self.__pageNumber)
        self.__parent.pnl.setPageNumber(pageNumber-1)
        self.__parent.pnl.pageNavigator(self.__parent.pnl.getBookContent())
        self.__displayedContent.SetInsertionPoint(insertionPoint)
        self.Destroy()

    #this event deletes an item from the bookmark list
    def on_remove(self, event):
        index = self.__listDisplay.GetNextSelected(-1)    #get the index of the selected item from the list display

        if index == -1:
            return 

        #otherwise, remove the highlighted item
        self.__listDisplay.DeleteItem(index)    #delete selected item from the list box
        self.__currentBookmarkList.pop(index)
        self.__insertDefaultItem()
        self.__updateNotifier()

        #also, destroy the dialog if the list is empty
        if len(self.__currentBookmarkList) == 0:
            self.Destroy()

    #this event clears all items from the bookmark list
    def on_clear(self, event):
        self.__dictBookmarks.pop(self.__path)
        self.__updateNotifier()
        self.Destroy()
