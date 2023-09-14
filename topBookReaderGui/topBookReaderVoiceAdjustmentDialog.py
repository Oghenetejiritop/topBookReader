
'''
* Coding: UTF-8
* Author: Oghenetejiri Peace Onosajerhe (peaceonosajerhe@gmail.com).
* topBookReaderVoiceAdjustmentDialog.py
* A part of TOP BOOK Reader.
* Licensed under the Massachusetts Institute of Technology (MIT);
* Copyright (C) 2023 Oghenetejiri Peace Onosajerhe.
'''


import wx

from topBookReaderGui.topBookReaderExtras.topBookReaderFunc import createTopBookReaderKeys
from topBookReaderGui.topBookReaderExtras.topBookReaderTts import textToSpeech as voiceChoices

#dialog for the voice settings
class TopBookReaderVoiceAdjustmentDialog(wx.Dialog):
    '''
    this class handles the settings of the text to speech synthesizers
    Accepts two parameters;
    Parent: that requires the topBookReaderPanel object.
    winReg: requires the windows registry object
'''

    def __init__(self, parent, winReg):
        super().__init__(None, wx.ID_ANY, title='Voice Adjustment Settings')

        pnl = wx.Panel(self, wx.ID_ANY)
        self.__winReg = winReg

        #instantiate the vertical box sizer for the controls
        self.__vSizer = wx.BoxSizer(wx.VERTICAL)

        #get the voiceKey and its associated values from the windows registry (voice rate, volume and voice selection index)
        voiceKey =createTopBookReaderKeys(self.__winReg, path='voices')
        defaultRate, defaultVolume, voiceIndex = self.__winReg.QueryValueEx(voiceKey, 'rate')[0], self.__winReg.QueryValueEx(voiceKey, 'volume')[0], self.__winReg.QueryValueEx(voiceKey, 'voice selection index')[0]

        label = wx.StaticText(pnl, wx.ID_ANY, 'Select a Reading Voice:')
        self.__voiceChoices = wx.Choice(pnl, wx.ID_ANY, choices=list(voiceChoices().keys()), style=wx.CB_SORT)
        self.__voiceChoices.SetSelection(int(voiceIndex))

        groupVoiceControls = wx.StaticBox(pnl, wx.ID_ANY, 'Voice Controls')
        labelRate = wx.StaticText(groupVoiceControls, wx.ID_ANY, 'Adjust Speech Rate:')
        self.__rate = wx.Slider(groupVoiceControls, wx.ID_ANY, value=int(defaultRate), minValue=0, maxValue=100, style=wx.SL_HORIZONTAL)
        labelVolume = wx.StaticText(groupVoiceControls, wx.ID_ANY, 'Adjust Speech Volue:')
        self.__volume = wx.Slider(groupVoiceControls, wx.ID_ANY, value=int(defaultVolume), minValue=0, maxValue=100)

        okBtn = wx.Button(pnl, wx.ID_ANY, 'OK')
        okBtn.Bind(wx.EVT_BUTTON, self.on_ok)
        cancelBtn = wx.Button(pnl, wx.ID_CANCEL, 'Cancel')


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
