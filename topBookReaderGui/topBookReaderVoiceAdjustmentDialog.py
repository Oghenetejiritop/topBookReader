
'''
* Coding: UTF-8
* Author: Oghenetejiri Peace Onosajerhe (peaceonosajerhe@gmail.com).
* topBookReaderVoiceAdjustmentDialog.py
* A part of TOP BOOK Reader.
* Licensed under the Massachusetts Institute of Technology (MIT);
* Copyright (C) 2023 Oghenetejiri Peace Onosajerhe.
'''


from wx import (BoxSizer, ALL, CENTER,  EXPAND, HORIZONTAL, LEFT, VERTICAL,
    Button, BU_EXACTFIT, EVT_BUTTON, ID_CANCEL,
    Choice, CB_SORT, Dialog,
    Slider, SL_HORIZONTAL, StaticText,)

from topBookReaderGui.topBookReaderExtras.topBookReaderFunc import createTopBookReaderKeys
from topBookReaderGui.topBookReaderExtras.topBookReaderTts import textToSpeech as voiceChoices

#dialog for the voice settings
class TopBookReaderVoiceAdjustmentDialog(Dialog):
    '''
    this class handles the settings of the text to speech synthesizers
    Accepts two parameters;
    Parent: that requires the topBookReaderPanel object.
    winReg: requires the windows registry object
'''

    def __init__(self, parent, winReg):
        super().__init__(None, -1, title='Voice Adjustment Settings')

        self.__winReg = winReg
        #get the voiceKey and its associated values from the windows registry (voice rate, volume and voice selection index)
        voiceKey =createTopBookReaderKeys(self.__winReg, path='voices')
        defaultRate, defaultVolume, voiceIndex = self.__winReg.QueryValueEx(voiceKey, 'rate')[0], self.__winReg.QueryValueEx(voiceKey, 'volume')[0], self.__winReg.QueryValueEx(voiceKey, 'voice selection index')[0]

        #instantiate the box sizers for the controls
        self.__vSizer1 = BoxSizer(VERTICAL)
        '''self.__vSizer2 = BoxSizer(VERTICAL)
        self.__vSizer3 = BoxSizer(VERTICAL)
        self.__hSizer = BoxSizer(HORIZONTAL)'''

        self.__vSizer1.Add(StaticText(self, -1, 'Reading Voice:'), 0, ALL, 5)
        self.__voiceChoices = Choice(self, -1, choices=list(voiceChoices().keys()), style=CB_SORT)
        self.__vSizer1.Add(self.__voiceChoices  , 0, EXPAND | ALL, 10)
        self.__voiceChoices.SetSelection(int(voiceIndex))

        labelRate = StaticText(self, -1, 'Rate:')
        self.__vSizer1.Add(labelRate, 0, ALL, 5)
        self.__rate = Slider(self, -1, value=int(defaultRate), minValue=0, maxValue=100, style=SL_HORIZONTAL)
        self.__vSizer1.Add(self.__rate, 0, EXPAND | ALL, 10)
        labelVolume = StaticText(self, -1, 'Volume:')
        self.__vSizer1.Add(labelVolume, 0, EXPAND | ALL, 10)
        self.__volume = Slider(self, -1, value=int(defaultVolume), minValue=0, maxValue=100)
        self.__vSizer1.Add(self.__volume, 0, EXPAND | ALL, 10)

        okBtn = Button(self, -1, 'OK')
        self.__vSizer1.Add(okBtn, 0, ALL, 5)
        okBtn.Bind(EVT_BUTTON, self.on_ok)
        cancelBtn = Button(self, ID_CANCEL, 'Cancel')
        self.__vSizer1.Add(cancelBtn, 0, ALL, 5)

        self.__vSizer1.SetSizeHints(self)
        self.SetSizer(self.__vSizer1)

    #events associated with this class

    #event that activates the okay button
    def on_ok(self, event):
        #set the voiceKey registry to write
        voiceKey =createTopBookReaderKeys(self.__winReg, keyAccess='w', path='voices')
        #adjust the voice settings with the highlighted values
        index = self.__voiceChoices.GetSelection()
        rateValue = str(self.__rate.GetValue())
        volumeValue = str(self.__volume.GetValue())
        choices = (('name', self.__voiceChoices.GetString(index)),
    ('rate', rateValue),
    ('volume', volumeValue),
    ('voice selection index', str(index)),)
        for name, value in choices:
            self.__winReg.SetValueEx(voiceKey, name, 0, self.__winReg.REG_SZ, value)
        self.Destroy()
