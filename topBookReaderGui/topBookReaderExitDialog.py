
'''
* Coding: UTF-8
* Author: Oghenetejiri Peace Onosajerhe (peaceonosajerhe@gmail.com).
* topBookReaderExitDialog.py
* A part of TOP BOOK Reader.
* Licensed under the Massachusetts Institute of Technology (MIT);
* Copyright (C) 2023 Oghenetejiri Peace Onosajerhe.
'''


from  wx import (BoxSizer, ALIGN_CENTER, ALL, CENTER,  EXPAND, HORIZONTAL, LEFT, VERTICAL,
    Button, BU_EXACTFIT, EVT_BUTTON, Font, FONTFAMILY_DEFAULT, FONTSTYLE_ITALIC, FONTWEIGHT_BOLD,
    Dialog, Panel, StaticText, ID_CANCEL,)

#dialog for the exitting action
class TopBookReaderExitDialog(Dialog):
    '''
    this class pops up with the confirming message; (Yes, No and Cancel buttons) in order to exit the app.
    Has  a parameter (parent)  that requires the topBookReaderFrame object.
    '''

    def __init__(self, parent):
        super().__init__(None, title='Exitting...', size=(500, 400))

        self.__parent = parent
        #instantiate the box sizers for the components (exit label and the buttons)
        self.__vSizer = BoxSizer(VERTICAL)
        hSizer1 = BoxSizer(HORIZONTAL)
        self.__hSizer2 = BoxSizer(HORIZONTAL)

        exitLabel = StaticText(self, -1, "Want to leave and continue from where you left off later?")    #sets the label confirmation message
        hSizer1.Add(exitLabel, 1, EXPAND | ALL, 10)
        self.__vSizer.Add(hSizer1, ALL | ALIGN_CENTER)

        self.__showBtn()


    #methods for the class

    #method that returns the (id, label and event handler) of each button 
    def __buttonInfo(self):
        return (
        (-1, '&Yes', self.on_yes),
        (-1, '&No',  self.on_no),
        )

    #method that implements the button component; 
    #accepts three parameters: id (-1), label (str) and evtHandler (event handler)
    def __implementBtn(self, id, label, evtHandler):
        btn = Button(self, id, label, style=BU_EXACTFIT)    #stores the button object
        self.Bind(EVT_BUTTON, evtHandler, btn)
        return btn

    #the method that displays the button to the screen
    def __showBtn(self):
        #unpack the __buttonInfo
        for id, label, evtHandler in self.__buttonInfo():
            #add each button to the box sizer
            self.__hSizer2.Add(self.__implementBtn( id, label, evtHandler), 0, ALL, 5)
        self.__hSizer2.Add(Button(self, ID_CANCEL, 'Cancel', style=BU_EXACTFIT), 0, ALL | CENTER, 5)
        self.__vSizer.Add(self.__hSizer2, 0, EXPAND)
        self.__vSizer.SetSizeHints(self)
        self.SetSizer(self.__vSizer)


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

