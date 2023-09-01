
'''
* Coding: UTF-8
* Author: Oghenetejiri Peace Onosajerhe (peaceonosajerhe@gmail.com).
* topBookReaderVoiceAdjustmentDialog.py
* A part of TOP BOOK Reader.
* Licensed under the Massachusetts Institute of Technology (MIT);
* Copyright (C) 2023 Oghenetejiri Peace Onosajerhe.
'''


import wx

#dialog for the voice settings
class TopBookReaderVoiceAdjustmentDialog(wx.Dialog):
    '''
    this class handles the settings of the text to speech synthesizers
    Has one parameter (parent) that requires the topBookReaderPanel object.
    '''

    def __init__(self, parent):
        super().__init__(None, wx.ID_ANY, title='Voice Adjustment Settings')

        pnl = wx.Panel(self, wx.ID_ANY)

        voiceChoices = ('Google TTS', 'Elequent TTS', 'Microsoft Speech API', 'ESpeak Engine')
        label = wx.StaticText(pnl, wx.ID_ANY, 'Select a Reading Voice:')
        self.__voiceChoices = wx.Choice(pnl, wx.ID_ANY, choices=voiceChoices, style=wx.CB_SORT)

        groupVoiceControls = wx.StaticBox(pnl, wx.ID_ANY, 'Voice Controls')

        labelRate = wx.StaticText(groupVoiceControls, wx.ID_ANY, 'Adjust Speech Rate:')
        self.__rate = wx.Slider(groupVoiceControls, wx.ID_ANY, value=10, minValue=0, maxValue=100, style=wx.SL_HORIZONTAL)

        labelVolume = wx.StaticText(groupVoiceControls, wx.ID_ANY, 'Adjust Speech Volue:')
        self.__volume = wx.Slider(groupVoiceControls, wx.ID_ANY, value=25, minValue=0, maxValue=100)

        okBtn = wx.Button(pnl, wx.ID_OK, 'OK')
        cancelBtn = wx.Button(pnl, wx.ID_CANCEL, 'Cancel')