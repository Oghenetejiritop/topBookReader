
'''
* Coding: UTF-8
* Author: Oghenetejiri Peace Onosajerhe (peaceonosajerhe@gmail.com).
* topBookReaderDictionaryDialog.py
* A part of TOP BOOK Reader.
* Licensed under the Massachusetts Institute of Technology (MIT);
* Copyright (C) 2023 Oghenetejiri Peace Onosajerhe.
'''


import wx

from topBookReaderGui.topBookReaderExtras.topBookReaderFunc import topBookReaderWordMeaning

#dialog for searching the meaning of words (dictionary)
class TopBookReaderDictionaryDialog(wx.Dialog):
    '''
    this class functions like a mini dictionary.
    Has  no parameter.
    '''

    def __init__(self):
        super().__init__(None, title='Quick Word Search...')

        #instantiate the vertical box sizer
        vSizer = wx.BoxSizer(wx.VERTICAL)

        pnl = wx.Panel(self)

        label = wx.StaticText(pnl, -1, 'Type word to search for:')
        vSizer.Add(label, 0, wx.ALL | wx.LEFT, 10)

        self.__wordText = wx.TextCtrl(pnl, wx.ID_ANY, size=(100, 25), style=wx.TE_PROCESS_ENTER)
        self.Bind(wx.EVT_TEXT_ENTER, self.on_wordMeaning, self.__wordText)
        vSizer.Add(self.__wordText, 0, wx.ALL | wx.LEFT, 5)

        searchBtn = wx.Button(pnl, wx.ID_ANY, '&Search word')
        searchBtn.Bind(wx.EVT_BUTTON, self.on_wordMeaning)
        vSizer.Add(searchBtn, 0, wx.ALL | wx.LEFT, 5)
  
        cancelBtn = wx.Button(pnl, wx.ID_CANCEL, 'Cancel')
        vSizer.Add(cancelBtn, 0, wx.ALL | wx.LEFT, 10)

        self.__displayMeaningLabel = wx.StaticText(pnl, -1, 'Search result:')
        vSizer.Add(self.__displayMeaningLabel, 0, wx.ALL | wx.LEFT, 10)

        self.__displayMeaning = wx.TextCtrl(pnl, wx.ID_ANY, size=(450, 450), style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH2)
        vSizer.Add(self.__displayMeaning, 0, wx.ALL | wx.LEFT, 5)

        vSizer.SetSizeHints(pnl)
        pnl.SetSizer(vSizer)

    #event associated with this class

    #event that handles the meaning of a word when searched
    def on_wordMeaning(self, event):
        #update the label of the displayMeaningLabel
        self.__displayMeaningLabel.SetLabel(f'Search result for the word {self.__wordText.GetValue()}:')
        #access the searched word
        self.__displayMeaning.SetValue(
        topBookReaderWordMeaning(self.__wordText.GetValue())
        )
        self.__displayMeaning.SetFocus()
