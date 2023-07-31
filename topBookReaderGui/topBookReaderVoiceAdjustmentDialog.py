
#dialog box for the voice settings
import wx

class TopBookReaderVoiceAdjustmentDialog(wx.Dialog):
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