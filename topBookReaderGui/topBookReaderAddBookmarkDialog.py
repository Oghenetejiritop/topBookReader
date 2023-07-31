
'''
* Coding: UTF-8
* Author: Oghenetejiri Peace Onosajerhe (peaceonosajerhe@gmail.com).
* topBookReaderAddBookmarkDialog.py
* A part of TOP BOOK Reader.
* Licensed under the Massachusetts Institute of Technology (MIT);
* Copyright (C) 2023 Oghenetejiri Peace Onosajerhe.
'''


import wx

from topBookReaderGui.topBookReaderExtras.topBookReaderFunc import unwantedCharRemover

#the dialog for adding a bookmark  
class TopBookReaderAddBookmarkDialog(wx.Dialog):
    '''
    this class is responsible for adding bookmarks to the bookmark history.
    Has  a parameter (parent)  that requires the topBookReaderFrame object.
    '''

    def __init__(self, parent):
        super().__init__(None, title='Add a Bookmark')

        self.__parent = parent

        #get the reference to the displayedContent component of the app
        self.__displayedContent = self.__parent.pnl.cloneDisplayedText()

        #call the __callBookmarkInfo method to retrieve the bookmark history of the current opened document.
        self.__callBookmarkInfo()

        #instantiate the vertical box sizer
        vSizer = wx.BoxSizer(wx.VERTICAL)

        pnl = wx.Panel(self)

        label = wx.StaticText(pnl, -1, 'Type a Bookmark Name for the Highlighted Text:')
        vSizer.Add(label, 0, wx.ALL | wx.LEFT, 10)

        self.__bookmarkText = wx.TextCtrl(pnl, wx.ID_ANY, size=(100, 25), style=wx.TE_PROCESS_ENTER)
        self.Bind(wx.EVT_TEXT_ENTER, self.on_addToBookmark, self.__bookmarkText)
        vSizer.Add(self.__bookmarkText, 0, wx.ALL | wx.LEFT, 5)

        addBtn = wx.Button(pnl, wx.ID_ANY, '&Add')
        addBtn.Bind(wx.EVT_BUTTON, self.on_addToBookmark)
        vSizer.Add(addBtn, 0, wx.ALL | wx.LEFT, 5)
  
        cancelBtn = wx.Button(pnl, wx.ID_CANCEL, 'Cancel')
        vSizer.Add(cancelBtn, 0, wx.ALL | wx.LEFT, 10)

        vSizer.SetSizeHints(pnl)
        pnl.SetSizer(vSizer)

    #methods defined for this class

    #get the bookmark history for the current book
    def __callBookmarkInfo(self):
        path = self.__parent.pnl.getFilePath()
        #get the bookmark history
        self.__dictBookmarks = self.__parent.pnl.getBookmarks()

        #get the list of bookmarks if path is a key
        if path in self.__dictBookmarks:
            self.__currentBookmarkList = self.__dictBookmarks[path]
            return

        #otherwise, create a new key for the path and add an empty list
        self.__dictBookmarks[path] = []
        self.__currentBookmarkList = self.__dictBookmarks[path]

    #event associated with this class

    #this event handles the bookmark function
    def on_addToBookmark(self, event):
        bookmarkName = self.__bookmarkText.GetValue()    #get the value of the name for the bookmark

        #validate the bookmark name if just contains letters or numbers
        bookmarkName = unwantedCharRemover(bookmarkName, '-;:[](){}&%@!#$^/?|\\"\~')
        bookmarkName = '(No bookmark name)' if bookmarkName.isspace()  or bookmarkName == '' else bookmarkName    #update the bookmark name if valid

        textSelection = self.__displayedContent.GetStringSelection()
        bookmarkText = f'{bookmarkName}; {self.__parent.pnl.getPageInfo()[0]}- {textSelection[:20]}...; {self.__displayedContent.GetInsertionPoint()}'

        #do nothing if the highlighted bookmark exist in the bookmarkList
        if bookmarkText in self.__currentBookmarkList:
            return

        #otherwise, append the bookmarked text;  and update the bookmark list
        self.__currentBookmarkList.append(bookmarkText)
        self.__parent.pnl.updateBookmarks(self.__dictBookmarks)
        self.Destroy()
