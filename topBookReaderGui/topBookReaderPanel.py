
'''
* Coding: UTF-8
* Author: Oghenetejiri Peace Onosajerhe (peaceonosajerhe@gmail.com).
* topBookReaderPanel.py
* A part of TOP BOOK Reader.
* Licensed under the Massachusetts Institute of Technology (MIT);
* Copyright (C) 2023 Oghenetejiri Peace Onosajerhe.

e:
ebarVenv\Scripts\activate.bat
cd topBookReader
py topBookReader.py
'''

from os import path

import wx
from wx.adv import Sound

from topBookReaderGui.topBookReaderContentDisplay  import TopBookReaderContentDisplay
from topBookReaderGui.topBookReaderRecentBookDialog import TopBookReaderRecentBooksDialog
from topBookReaderGui.topBookReaderVoiceAdjustmentDialog import TopBookReaderVoiceAdjustmentDialog

from topBookReaderGui.topBookReaderBookFormats.fileValidator import FileValidator
from topBookReaderGui.topBookReaderExtras.topBookReaderSupport import UniqueList
from topBookReaderGui.topBookReaderExtras.topBookReaderFunc import topBookReaderPath, createTopBookReaderPaths

#create the topBookReader paths
homeDirectory = path.expanduser('~').replace('\\', '/')
topBookReaderDirectory =f'{homeDirectory}/.topBookReader/topBookReaderLib'
createTopBookReaderPaths(topBookReaderDirectory)

#alias the path.exists function
isExistingPath = path.exists

#variable that holds the default displayed text 
defaultValue = '''  Welcome to the TOP Book Reader; an accessible E-book reader which presents users with an intuitive interface that enables you to access any book in various electronic formats.
Head to the Help menu item to learn more about it.
Happy reading, ENJOY!
        '''

#panel for the application
class TopBookReaderPanel(wx.Panel):
    '''
    this class handles the rendering of the document basic controls which include: (display content, previous with next page, play buttons and some components)
    Has  a parameter (parent)  that requires the topBookReaderFrame object.
    '''

    def __init__(self, parent):
        super().__init__(parent, wx.ID_ANY)

        self.__parent = parent
        self.__statusBar = self.__parent.CreateStatusBar()    #instantiates the status bar object

        self.__bookFile = FileValidator()    #instantiates the FileValidator object
        self.__list = UniqueList(self.__bookFile, self.getRecentList())    #instantiates the UniqueList object
        self.__bookInfo = self.getRecentBookInfo()    #stores the dictionary of each recent book information 

        self.__sound = Sound('resources/sounds/page_navigation.wav')    #inserts the sound file for page navigation.

        self.__label = wx.StaticText(self, wx.ID_ANY, 'Display Content')
        self.__displayedText = TopBookReaderContentDisplay(self, topBookReaderDirectory)
        #show the default content
        self.displayDefaultValue()

        #instantiate the vertical box sizer for the buttons
        self.__vSizer = wx.BoxSizer(wx.VERTICAL)

        #show the buttons
        self.__showBtn()

        #include keyboard shortcuts
        btnAccel = wx.AcceleratorTable(self.__btnEntries)
        self.SetAcceleratorTable(btnAccel)

        self.updateStatusBar()    #update the statusbar information.


    #methods defined
    def cloneDisplayedText(self):    #return a reference of the display content
        return self.__displayedText

    def __buttonInfo(self):
        return (
        ('Previous Page', self.on_prvPage),
        ('&Play Aloud', self.on_playAloud),
        ('Next Page', self.on_nxtPage),
        ('&Recent Opened Books...', self.on_recentBooks),
        ('&Voice Adjustment Setting...', self.on_voiceAdjustment)
        )

    def __implementBtn(self, id, label, evtHandler):
        btn = wx.Button(self, id, label, style=wx.BU_EXACTFIT)
        self.Bind(wx.EVT_BUTTON, evtHandler, btn)
        return btn

    def __showBtn(self):
        i = j = 0
        #store the btn icons in a tuple
        pngFiles = ('previous', 'play', 'next')

        #a list that holds each button object
        self.__btnList = []

        #entries for the page navigations key short cuts
        self.__btnEntries = [wx.AcceleratorEntry() for entry in range(2)]

        #unpack the __buttonInfo
        for label, evtHandler in self.__buttonInfo():
            btn = self.__implementBtn(wx.ID_ANY, label, evtHandler)
            self.__btnList.append(btn)

            #set the shortcut keys (n and p) for both the previous and next buttons
            if(label.endswith('e')):
                self.__btnEntries[i].Set(wx.ACCEL_NORMAL, ord(label[0]), btn.GetId())
                i += 1

            #add each button to the vSizer
            self.__vSizer.Add(btn, 0, wx.ALL | wx.CENTER, 5)

        #insert the button icons
        for icon in pngFiles:
            bmp = wx.Bitmap(f'resources/images/{icon}.png', wx.BITMAP_TYPE_PNG)
            self.__btnList[j].SetBitmap(bmp)
            j += 1

        self.__vSizer.SetSizeHints(self)
        self.SetSizer(self.__vSizer)

    #update the recent list of opened books (to a serialized list)
    def updateRecentList(self, content):
        topBookReaderPath(topBookReaderDirectory, 'topBookReaderRecentList.pkl', content=content)

    #get the recent list of opened books (from a  serialized list)
    def getRecentList(self):
        return topBookReaderPath(topBookReaderDirectory, 'topBookReaderRecentList.pkl')

    #update the book info (to a serialized dictionary)
    def updateRecentBookInfo(self, content):
        topBookReaderPath(topBookReaderDirectory, 'topBookReaderRecentBookInfo.pkl', content=content)

    #retrieve the content from the book info (from a serialized dictionary)
    def getRecentBookInfo(self):
        return topBookReaderPath(topBookReaderDirectory, 'topBookReaderRecentBookInfo.pkl')

    #update the bookmarks of the current opened book (to a serialized dictionary)
    def updateBookmarks(self, content):
        topBookReaderPath(topBookReaderDirectory, 'topBookReaderBookmarksHistory.pkl', content)

    #retrieve the bookmarks of the current opened book (from a serialized dictionary)
    def getBookmarks(self):
        return topBookReaderPath(topBookReaderDirectory, 'topBookReaderBookmarksHistory.pkl')

    #method to access newly opened book
    def __accessNewOpenedBook(self, filePath):
        self.__parent.SetTitle(f'{self.__bookFile.getFileName()} - TOP Book Reader')    #update the title bar
        self.__displayedText.SetValue(self.__bookFile.openFile())    #display the content
        #map the current book info with the serialized opened book information
        self.__bookInfo[filePath] = (self.__parent.GetTitle(), 0, 0)
        #update the recentBookInfo file
        self.updateRecentBookInfo(self.__bookInfo)

    #method to access previously opened book saved before
    def __accessPreviousOpenedBook(self, filePath):
        #retrieve the book information from the serialized dictionary
        bookInfo = self.__bookInfo[filePath]
        self.__parent.SetTitle(bookInfo[0])    #update the title bar
        self.__bookFile.setPageNumber(bookInfo[1])    #set the page number
        self.__displayedText.SetValue(self.__bookFile.openFile())    #display the content
        self.__displayedText.SetInsertionPoint(bookInfo[2])    #set the previous character position

    #method that displays the opened file content
    def displayContent(self, file):
        self.__bookFile.insertFile(file)    #insert the book file to access its content
        filePath = self.getFilePath() #get the file source
        self.__list.append(filePath)    #update the list with the file path
        self.updateRecentList(self.__list.output())    #update the topBookReaderRecentList file (serialized list)

        #access the book if opened before; by checking if the file path is a serialized dictionary key.
        if filePath in self.getRecentBookInfo():
            self.__accessPreviousOpenedBook(filePath)
        #otherwise, access the new opened book
        else:
            self.__accessNewOpenedBook(filePath)

        self.updateStatusBar()    #update the statusbar.

        #method that displays the default value
    def displayDefaultValue(self):
        #access the first book from the list if the list isn't empty and it still exists
        if (not self.__list.isEmpty()) and (isExistingPath(self.__list.selectItem(0))):
            self.displayContent(self.__list.selectItem(0))  
            return
        #otherwise, display the default value if recent list is empty or the first file on the list  is not found
        self.__parent.SetTitle('TOP Book Reader')
        self.__displayedText.SetValue(defaultValue)

    #method that updates the statusbar info
    def updateStatusBar(self):
        #get the current book page information if opened
        if not self.isBookOpened():
            bookPageInfo = self.getPageInfo()    #store both the current page number and total pages of the opened book

        #update the statusbar by displaying the page number or an open a file info if the list is empty.
        statusValue = 'You can open a book by clicking on ctrl + o!' if self.__list.isEmpty() else f'Page {bookPageInfo[0]} Of {bookPageInfo[1]} Pages'
        self.__statusBar.SetStatusText(statusValue)

    #method that gets the current title, page number and character position of an opened book
    def getOpenedBookInfo(self):
        return (self.__parent.GetTitle(), self.__bookFile.getPageNumber(), self.__displayedText.GetInsertionPoint(),)

    #method that is responsible for temporary  insertion of file path into the bookFile object
    def insertTempFile(self, file):
        self.__bookFile.insertTempFile(file)        

        #method that gets the file name
    def getFileName(self):
        return self.__bookFile.getFileName()

    #method that gets the file path
    def getFilePath(self):
        return self.__bookFile.getFileSource()        

    #method that gets the content of the opened book
    def getBookContent(self):
        return self.__bookFile.openFile()

    #method that sets the page number for an opened book
    def setPageNumber(self, number):
        self.__bookFile.setPageNumber(number)

    #method that returns the current page number and total pages of an opened book
    def getPageInfo(self):
        return (self.__bookFile.getPageNumber() + 1, self.__bookFile.getTotalPages())

    #method that verifies if a book is opened
    def isBookOpened(self):
        return len(self.__parent.GetTitle()) == 15

    #method that handles the page navigation rendering
    def pageNavigator(self, page):
        #play the page sound if page switches
        self.__sound.Play()

        #get the default size of the displayedContent
        defaultSize = self.__displayedText.GetSize()
        #shrink the displayedContent for a page change effect  
        self.__displayedText.SetSize(300, 220)
        #reset it to its default size
        self.__displayedText.SetSize(defaultSize)

        #switch to the current page and set focus to the displayedContent
        self.__displayedText.SetValue(page)
        self.__displayedText.SetFocus()
        self.updateStatusBar()    #update the statusbar.


    #events associated with this class

    #event that handles the previous page navigation.
    def on_prvPage(self, event):
        #just return if either no book is opened; or it's on the first page
        if(self.isBookOpened() or self.__bookFile.getPageNumber() == 0):
            return

        #otherwise, play the sound and switch to the previous page
        self.pageNavigator(self.__bookFile.previousPage())

    #event that is responsible for both the play and pause of the voice reader feature.
    def on_playAloud(self, event):
        pass

            #event that handles the next page navigation.
    def on_nxtPage(self, event):
        #just return if either no book is opened; or it's on the last page
        if(self.isBookOpened() or  self.__bookFile.getPageNumber() == self.__bookFile.getTotalPages() -1):
            return

        #otherwise, play the sound and switch to the next page
        self.pageNavigator(self.__bookFile.nextPage())

    #event that pops up with the recently opened book list dialog box.
    def on_recentBooks(self, event):
        dlg = TopBookReaderRecentBooksDialog(self, self.__bookFile, self.__list)
        dlg.ShowModal()
        dlg.Destroy()

    #event that pops up with the dialog box to make some setting adjustment to the current voice reader.
    def on_voiceAdjustment(self, event):
        dlg = TopBookReaderVoiceAdjustmentDialog(self)
        dlg.ShowModal()
        dlg.Destroy()
