
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

from topBookReaderGui.topBookReaderExtras.topBookReaderSupport import UniqueList, ThreadControls
from topBookReaderGui.topBookReaderExtras.topBookReaderFunc import topBookReaderPath, createTopBookReaderPaths, textToSpeech as tts

#set the paths
homeDirectory = path.expanduser('~').replace('\\', '/')
topBookReaderDirectory =f'{homeDirectory}/.topBookReader/topBookReaderLib'
createTopBookReaderPaths(topBookReaderDirectory)    #creates the topBookReader paths

#alias the path.exists function
isExistingPath = path.exists

#variable that holds the default displayed text 
defaultValue = '''  Welcome to the TOP Book Reader; an accessible E-Book reader which presents users with an intuitive interface that enables you to access any book in various electronic formats.
Head to the Help menu item to learn more about it.
Happy reading, ENJOY!
        '''

#panel for the application
class TopBookReaderPanel(wx.Panel):
    '''
    this class handles the rendering of the document basic controls which include: (the display content text area, previous with next page button, play button and some components)
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
        self.__displayedText = TopBookReaderContentDisplay(self, topBookReaderDirectory)    #instantiates the TopBookReaderContentDisplay object
        #show the default content
        self.displayDefaultValue()

        #instantiate the vertical box sizer for the buttons
        self.__vSizer = wx.BoxSizer(wx.VERTICAL)

        #make the buttons visible
        self.__showBtn()
        self.__readAloudBtn = self.__btnList[1]    #stores the play/pause button object

        #set keyboard shortcuts
        btnShortcuts = wx.AcceleratorTable(self.__btnEntries)
        self.SetAcceleratorTable(btnShortcuts)

        self.updateStatusBar()    #updates the statusbar information


    #methods defined

    #method that return a reference of the display content
    def cloneDisplayedText(self):    #return a reference of the display content
        return self.__displayedText

    #method that returns the label and event handler of each button  
    def __buttonInfo(self):
        return (
        ('Previous Page (P)', self.on_prvPage),
        ('&Play Aloud', self.on_playAloud),
        ('Next Page (N)', self.on_nxtPage),
        ('&Recent Opened Books...', self.on_recentBooks),
        ('&Voice Adjustment Setting...', self.on_voiceAdjustment)
        )

    #method that implements the button component; 
    #accepts three parameters: id (wx.ID_ANY), label (str) and evtHandler (event handler)
    def __implementBtn(self, id, label, evtHandler):
        btn = wx.Button(self, id, label, style=wx.BU_EXACTFIT)
        self.Bind(wx.EVT_BUTTON, evtHandler, btn)
        return btn

    #the method that displays the button to the screen
    def __showBtn(self):
        i = j = 0    #serves as counters 
        pngFiles = ('previous', 'play', 'next')    #store the btn icons in a tuple
        self.__btnList = []    #a list that will hold each button object
        #set the entries for the page navigation key's shortcuts
        self.__btnEntries = [wx.AcceleratorEntry(), wx.AcceleratorEntry()]

        #unpack the __buttonInfo
        for label, evtHandler in self.__buttonInfo():
            btn = self.__implementBtn(wx.ID_ANY, label, evtHandler)
            self.__btnList.append(btn)    #appends the current btn object

            #set the shortcut keys (n and p) for both the previous and next buttons
            if(label.endswith(')')):
                self.__btnEntries[i].Set(wx.ACCEL_NORMAL, ord(label[0]), btn.GetId())
                i += 1    #increments i by 1

            #add each button to the vSizer
            self.__vSizer.Add(btn, 0, wx.ALL | wx.CENTER, 5)

        #insert the button icons
        for icon in pngFiles:
            bmp = wx.Bitmap(f'resources/images/{icon}.png', wx.BITMAP_TYPE_PNG)
            self.__btnList[j].SetBitmap(bmp)
            j += 1    #increments j by 1

        self.__vSizer.SetSizeHints(self)
        self.SetSizer(self.__vSizer)

    #method that updates the recent list of opened books (as a serialized file)
    #accepts one parameter: content (list)
    def updateRecentList(self, content):
        topBookReaderPath(topBookReaderDirectory, 'topBookReaderRecentList.pkl', content=content)

    #method that get the recent list of opened books (from a  serialized list)
    def getRecentList(self):
        return topBookReaderPath(topBookReaderDirectory, 'topBookReaderRecentList.pkl')    #returns a list

    #method that updates the book info (as a serialized file)
    #accepts one parameter: content (dictionary)
    def updateRecentBookInfo(self, content):
        topBookReaderPath(topBookReaderDirectory, 'topBookReaderRecentBookInfo.pkl', content=content)

    #method that retrieves the content from the book info (from a serialized dictionary)
    def getRecentBookInfo(self):
        return topBookReaderPath(topBookReaderDirectory, 'topBookReaderRecentBookInfo.pkl')    #returns a dictionary

    #update the bookmarks of the current opened book (as a serialized file)
    #accepts one parameter: content (dictionary)
    def updateBookmarks(self, content):
        topBookReaderPath(topBookReaderDirectory, 'topBookReaderBookmarksHistory.pkl', content)

    #method that retrieve the bookmarks of the current opened book (from a serialized dictionary)
    def getBookmarks(self):
        return topBookReaderPath(topBookReaderDirectory, 'topBookReaderBookmarksHistory.pkl')    #returns a dictionary

    #method that updates the statusbar info
    def updateStatusBar(self):
        #get the current book page information if opened
        if not self.isBookOpened():
            bookPageInfo = self.getPageInfo()    #stores both the current page number and total pages of the opened book

        #update the statusbar by displaying the page number or an open a document message if the list is empty
        statusValue = 'You can open a document by clicking on ctrl + o!' if self.__list.isEmpty() else f'Page {bookPageInfo[0]} Of {bookPageInfo[1]} Pages'
        self.__statusBar.SetStatusText(statusValue)
        #set the readAloud and noSwitchedPage flags to false
        self.__readAloud= self.__noSwitchedPage = False

    #method to access an opened document for the 1st time
    #accepts one parameter: filePath (str)
    def __accessNewOpenedBook(self, filePath):
        self.__parent.SetTitle(f'{self.__bookFile.getFileName()} - TOP Book Reader')    #update the title bar
        self.__displayedText.SetValue(self.__bookFile.openFile())    #displays the content
        #map the current book info with the serialized opened book information (title, page num and char position)
        self.__bookInfo[filePath] = (self.__parent.GetTitle(), 0, 0)
        self.updateRecentBookInfo(self.__bookInfo)    #updates recentBookInfo file

    #method to access a previously opened document
    #accepts one parameter: filePath (str)
    def __accessPreviousOpenedBook(self, filePath):
        #retrieve the book information from the serialized dictionary
        bookInfo = self.__bookInfo[filePath]
        self.__parent.SetTitle(bookInfo[0])    #updates the title bar
        self.__bookFile.setPageNumber(bookInfo[1])    #sets the page number
        self.__displayedText.SetValue(self.__bookFile.openFile())    #displays the content
        self.__displayedText.SetInsertionPoint(bookInfo[2])    #sets the previous character position

    #method that displays the opened file content
    #accepts one parameter: file (str)
    def displayContent(self, file):
        self.__bookFile.insertFile(file)    #inserts the document to access its content
        filePath = self.getFilePath() #stores the file source
        self.__list.append(filePath)    #updates the list with the file path
        self.updateRecentList(self.__list.output())    #updates the topBookReaderRecentList file (serialized list)

        #access the book if opened before; by checking if the file path is a serialized dictionary key.
        if filePath in self.getRecentBookInfo():
            self.__accessPreviousOpenedBook(filePath)
        #otherwise, access the new opened book
        else:
            self.__accessNewOpenedBook(filePath)

        self.updateStatusBar()    #updates the statusbar.

        #method that displays the default value
    def displayDefaultValue(self):
        #access the first book from the list if the list isn't empty and the file still exists
        if (not self.__list.isEmpty()) and (isExistingPath(self.__list.selectItem(0))):
            self.displayContent(self.__list.selectItem(0))  
            return
        #otherwise, display the default value
        self.__parent.SetTitle('TOP Book Reader')
        self.__displayedText.SetValue(defaultValue)

    #method that gets the current title, page number and character position of an opened book
    def getOpenedBookInfo(self):
        return (self.__parent.GetTitle(), self.__bookFile.getPageNumber(), self.__displayedText.GetInsertionPoint(),)    #returns a tuple

    #method that is responsible for temporary  insertion of file path into the bookFile object
    #accepts one parameter: file (str)
    def insertTempFile(self, file):
        self.__bookFile.insertTempFile(file)        

        #method that gets the file name
    def getFileName(self):
        return self.__bookFile.getFileName()    #returns str

    #method that gets the file path
    def getFilePath(self):
        return self.__bookFile.getFileSource()    #returns str

    #method that gets the content of the opened book
    def getBookContent(self):
        return self.__bookFile.openFile()    #returns str

    #method that sets the page number for an opened book
    #accepts one parameter: number (int)
    def setPageNumber(self, number):
        self.__bookFile.setPageNumber(number)

    #method that returns the current page number and total pages of an opened book
    def getPageInfo(self):
        return (self.__bookFile.getPageNumber() + 1, self.__bookFile.getTotalPages())    #returns a tuple

    #method that verifies if a book is opened
    def isBookOpened(self):
        return len(self.__parent.GetTitle()) == 15    #returns bool


    #method that handles the page navigation rendering
    #accepts one parameter: page (str)
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

    #method that updates the thread operation in regards to the on_play event handler
    def __updateThread(self):
        #resume the thread operation if readAloud and noSwitchedPage flags are set to true
        if(self.__readAloud and self.__noSwitchedPage):
            self.__thread.resume()
        else:    #otherwise, start the thread operation
            #set the readAloud and noSwitchedPage flags to true
            self.__readAloud= self.__noSwitchedPage = True
            textLines = self.__displayedText.GetValue().split('.')
            self.__thread = ThreadControls(target=tts, args=(textLines,), btn=self.__readAloudBtn)
            self.__thread.start()

    #event that is responsible for both the play and pause of the read aloud feature.
    def on_playAloud(self, event):
        if self.__readAloudBtn.GetLabel().endswith('d'):
            self.__updateThread()
        else:
            self.__thread.pause()
        
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
