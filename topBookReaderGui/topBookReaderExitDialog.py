
'''
* Coding: UTF-8
* Author: Oghenetejiri Peace Onosajerhe (peaceonosajerhe@gmail.com).
* topBookReaderExitDialog.py
* A part of TOP BOOK Reader.
* Licensed under the Massachusetts Institute of Technology (MIT);
* Copyright (C) 2023 Oghenetejiri Peace Onosajerhe.
'''


import wx

#dialog for the exitting action
class TopBookReaderExitDialog(wx.Dialog):
    '''
    this class pops up with the confirming message; (Yes, No and Cancel buttons) in order to exit the app.
    Has  a parameter (parent)  that requires the topBookReaderFrame object.
    '''

    def __init__(self, parent):
        super().__init__(None, title='Exitting...')

        self.__parent = parent
        wx.StaticText(self, wx.ID_ANY, "Want to leave and continue from where you left off later?")    #sets the label confirmation message

        #instantiate the horizontal box sizer for the buttons
        self.__hSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.__showBtn()


    #methods for the class

    #method that returns the (id, label and event handler) of each button 
    def __buttonInfo(self):
        return (
        (wx.ID_ANY, '&Yes', self.on_yes),
        (wx.ID_ANY, '&No',  self.on_no),
        )

    #method that implements the button component; 
    #accepts three parameters: id (wx.ID_ANY), label (str) and evtHandler (event handler)
    def __implementBtn(self, id, label, evtHandler):
        btn = wx.Button(self, id, label)    #stores the button object
        self.Bind(wx.EVT_BUTTON, evtHandler, btn)
        return btn

    #the method that displays the button to the screen
    def __showBtn(self):
        #unpack the __buttonInfo
        for id, label, evtHandler in self.__buttonInfo():
            #add each button to the vSizer
            self.__hSizer.Add(self.__implementBtn( id, label, evtHandler), 0, wx.ALL | wx.CENTER, 5)
        self.__hSizer.Add(wx.Button(self, wx.ID_CANCEL, 'Cancel',), 0, wx.ALL | wx.CENTER, 5)
        self.__hSizer.SetSizeHints(self)
        self.SetSizer(self.__hSizer)


    #events associated with this class

    #event that saves a book info before closing the program
    def on_yes(self, event):
        filePath = self.__parent.pnl.getRecentList()[0]    #get the first item from the recent book list (a file path)
        fileDict = self.__parent.pnl.getRecentBookInfo()    #get the previous book information including the current opened book
        fileDict[filePath] = self.__parent.pnl.getOpenedBookInfo()    #update the current book information including (the title, page number and the position of a character)
        self.__parent.pnl.updateRecentBookInfo(fileDict)    #update the recentBookInfo file
        self.Destroy()
        self.__parent.Close(True)

    #event that just closes the app without saving
    def on_no(self, event):
        self.Destroy()
        self.__parent.Close(True)

