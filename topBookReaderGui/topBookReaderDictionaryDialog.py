
'''
* Coding: UTF-8
* Author: Oghenetejiri Peace Onosajerhe (peaceonosajerhe@gmail.com).
* topBookReaderDictionaryDialog.py
* A part of TOP BOOK Reader.
* Licensed under the Massachusetts Institute of Technology (MIT);
* Copyright (C) 2023 Oghenetejiri Peace Onosajerhe.
'''


from  wx import (BoxSizer, ALL, CENTER,  EXPAND, HORIZONTAL, LEFT, VERTICAL,
    Button, BU_EXACTFIT, EVT_BUTTON,
    Dialog, Panel, StaticText, ID_CANCEL,
    TextCtrl, EVT_TEXT_ENTER, TE_PROCESS_ENTER, TE_MULTILINE, TE_READONLY, TE_RICH2,)

from topBookReaderGui.topBookReaderExtras.topBookReaderFunc import topBookReaderWordMeaning

#dialog for searching the meaning of words (dictionary)
class TopBookReaderDictionaryDialog(Dialog):
    '''
    this class functions like a mini dictionary.
    Has  no parameter.
    '''

    def __init__(self):
        super().__init__(None, title='Quick Word Search...')

        #instantiate the vertical box sizer
        vSizer = BoxSizer(VERTICAL)

        pnl = Panel(self)

        label = StaticText(pnl, -1, 'Type word to search for:')
        vSizer.Add(label, 0, ALL | LEFT, 10)

        self.__wordText = TextCtrl(pnl, -1, size=(100, 25), style=TE_PROCESS_ENTER)
        self.Bind(EVT_TEXT_ENTER, self.on_wordMeaning, self.__wordText)
        vSizer.Add(self.__wordText, 0, ALL | LEFT, 5)

        searchBtn = Button(pnl, -1, '&Search word')
        searchBtn.Bind(EVT_BUTTON, self.on_wordMeaning)
        vSizer.Add(searchBtn, 0, ALL | LEFT, 5)
  
        cancelBtn = Button(pnl, ID_CANCEL, 'Cancel')
        vSizer.Add(cancelBtn, 0, ALL | LEFT, 10)

        self.__displayMeaningLabel = StaticText(pnl, -1, 'Search result:')
        vSizer.Add(self.__displayMeaningLabel, 0, ALL | LEFT, 10)

        self.__displayMeaning = TextCtrl(pnl, -1, size=(450, 450), style=TE_MULTILINE | TE_READONLY | TE_RICH2)
        vSizer.Add(self.__displayMeaning, 0, ALL | LEFT, 5)

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
