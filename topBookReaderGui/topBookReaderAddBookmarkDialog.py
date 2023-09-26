
'''
* Coding: UTF-8
* Author: Oghenetejiri Peace Onosajerhe (peaceonosajerhe@gmail.com).
* topBookReaderAddBookmarkDialog.py
* A part of TOP BOOK Reader.
* Licensed under the Massachusetts Institute of Technology (MIT);
* Copyright (C) 2023 Oghenetejiri Peace Onosajerhe.
'''


from  wx import (BoxSizer, ALL, CENTER,  EXPAND, HORIZONTAL, LEFT, VERTICAL,
    Button, BU_EXACTFIT, EVT_BUTTON, Font, FONTFAMILY_DEFAULT, FONTSTYLE_ITALIC, FONTWEIGHT_BOLD,
    Dialog, Panel, StaticText, ID_CANCEL,
    TextCtrl, EVT_TEXT_ENTER, TE_PROCESS_ENTER,)

from topBookReaderGui.topBookReaderExtras.topBookReaderFunc import unwantedCharRemover

#the dialog for adding a bookmark  
class TopBookReaderAddBookmarkDialog(Dialog):
    '''
    this class is responsible for adding bookmarks to the bookmark history.
    Has  a parameter (parent)  that requires the topBookReaderFrame object.
    '''

    def __init__(self, parent):
        super().__init__(None, title='Add a Bookmark', size=(260, 240))

        self.__parent = parent

        #get the reference to the displayedContent component of the app
        self.__displayedContent = self.__parent.pnl.cloneDisplayedText()

        #call the __callBookmarkInfo method to retrieve the bookmark history of the current opened document.
        self.__callBookmarkInfo()

        #instantiate the vertical box sizer
        vSizer = BoxSizer(VERTICAL)

        pnl = Panel(self)

        label = StaticText(pnl, -1, 'Type a Bookmark Name for the Highlighted Text:')
        vSizer.Add(label, 0, ALL | LEFT, 10)

        self.__bookmarkText = TextCtrl(pnl, -1, size=(75, 25), style=TE_PROCESS_ENTER)
        self.Bind(EVT_TEXT_ENTER, self.on_addToBookmark, self.__bookmarkText)
        vSizer.Add(self.__bookmarkText, 0, ALL | LEFT, 5)

        addBtn = Button(pnl, -1, '&Add')
        addBtn.Bind(EVT_BUTTON, self.on_addToBookmark)
        vSizer.Add(addBtn, 0, ALL | LEFT, 5)
  
        cancelBtn = Button(pnl, ID_CANCEL, 'Cancel')
        vSizer.Add(cancelBtn, 0, ALL | LEFT, 10)

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
