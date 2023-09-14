
'''
* Coding: UTF-8
* Author: Oghenetejiri Peace Onosajerhe (peaceonosajerhe@gmail.com).
* topBookReaderContentDisplay.py
* A part of TOP BOOK Reader.
* Licensed under the Massachusetts Institute of Technology (MIT);
* Copyright (C) 2023 Oghenetejiri Peace Onosajerhe.
'''


import wx

from topBookReaderGui.topBookReaderExtras.topBookReaderFunc import topBookReaderPath

#the text control  that handles displayed contents
class TopBookReaderContentDisplay(wx.TextCtrl):
    '''
    this class displays contents to the screen.
    Accepts  two parameters;
    parent: that requires the topBookReaderPanel object.
    topBookReaderDirectory: takes the path of the topBookReaderFont (str).
    '''

    def __init__(self, parent, topBookReaderDirectory):
        super().__init__(parent, wx.ID_ANY, size=(600, 540), style=(wx.TE_MULTILINE | wx.TE_READONLY| wx.TE_RICH2))
        self.__dir = topBookReaderDirectory
        #handle the font data
        self.__fontProperties = topBookReaderPath(self.__dir, 'topBookReaderFont.pkl')    #stores the font properties in a list
        #instantiate the font data
        self.__fontData = wx.FontData()
        #extract the fontProperties 
        font = wx.Font(self.__fontProperties[0], self.__fontProperties[1], self.__fontProperties[2], self.__fontProperties[3])
        self.__fontData.SetInitialFont(font)
        self.__fontData.SetColour(self.__fontProperties[4])
        #set the font properties for the display
        self.SetFont(font)
        self.SetForegroundColour(self.__fontProperties[4])  #sets the text colour
        self.__zoomValue = 1.0

        self.Bind(wx.EVT_MOUSEWHEEL, self.on_mouse_wheel)

    #method that managesthe the font adjustment for the content display
    def adjustFont(self):
        #instantiate the font dialog
        dlg = wx.FontDialog(None, self.__fontData)
        #when okay is clicked, apply the font changes.
        if dlg.ShowModal() == wx.ID_OK:
            fontData = dlg.GetFontData()
            fontSelected = fontData.GetChosenFont()
            #adjust the font of the content display
            self.SetFont(fontSelected)
            self.SetForegroundColour(fontData.GetColour())
            #update the initial font file with the properties
            fontProperties = [fontSelected.GetPointSize(), fontSelected.GetFamily(), fontSelected.GetStyle(), fontSelected.GetWeight(), fontData.GetColour()]
            topBookReaderPath(self.__dir, 'topBookReaderFont.pkl', fontProperties)
        dlg.Destroy()

    #method for zooming in on a text
    def zoomIn(self):
        self.__zoomValue *= 1.1
        self.__updateFont()

    #method for zooming out on a text
    def zoomOut(self):
        self.__zoomValue /= 1.1
        self.__updateFont()

    #update the font status
    def __updateFont(self):
        font = self.GetFont()
        font.SetPointSize(int(10 * self.__zoomValue))  # Adjust the base font size
        self.SetFont(font)

    def on_mouse_wheel(self, event):
        rotation = event.GetWheelRotation()
        delta = rotation / 120  # Normalizing the rotation value

        if delta > 0:
            self.zoomIn()
        else:
            self.zoomOut()
