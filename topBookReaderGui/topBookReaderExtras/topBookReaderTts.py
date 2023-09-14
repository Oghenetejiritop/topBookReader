
'''
* Coding: UTF-8
* Author: Oghenetejiri Peace Onosajerhe (peaceonosajerhe@gmail.com).
* topBookReaderTts.py
* A part of TOP BOOK Reader.
* Licensed under the Massachusetts Institute of Technology (MIT);
* Copyright (C) 2023 Oghenetejiri Peace Onosajerhe.
'''

#module that handles the text to speech functionalities
from time import sleep
import ctypes
from gtts import gTTS
from pyttsx3 import init as msTts
from wx import MessageDialog, ICON_EXCLAMATION

try:
    clientLib = ctypes.windll.LoadLibrary('accessibility_service/nvdaControllerClient/nvdaControllerClient32.dll')
except:
    clientLib = ctypes.windll.LoadLibrary('accessibility_service/nvdaControllerClient/nvdaControllerClient64.dll')

def nvdaSpeak(text):
    clientLib.nvdaController_speakText(text)

def textToSpeech():
    return {'Google Text To Speech (GTTS)': (googleTts, 0),
    'Microsoft Hazel Desktop - English (Great Britain)': (microsoftTts, 0),
    'Microsoft Zira Desktop - English (United States)': (microsoftTts, 1),}

#the google text to speech function
def googleTts(text, voice, rate, volume):
    try:
        tts = gTTS(text)
        tts.save('talk.mp3')
    except:
        msg = 'The google TTS requires the internet to function.'
        dlg = MessageDialog(None, msg, 'Connection Error!', style=ICON_EXCLAMATION)
        dlg.ShowModal()
        dlg.Destroy()

#the microsoft text to speech function
def microsoftTts(text, voice, rate, volume):
    tts = msTts()
    voices = tts.getProperty('voices')
    tts.setProperty('voice', voices[voice].id)
    tts.setProperty('rate', int(rate) *5)
    tts.setProperty('volume', int(volume) /100)
    tts.say(text)
    tts.runAndWait()
