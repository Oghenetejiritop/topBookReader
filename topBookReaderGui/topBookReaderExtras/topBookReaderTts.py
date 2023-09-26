
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
#from wx import MessageDialog, ICON_EXCLAMATION

#gets if the platform is 32 bits or 64 bits
try:
    clientLib = ctypes.windll.LoadLibrary('accessibility_service/nvdaControllerClient/nvdaControllerClient32.dll')
except:
    clientLib = ctypes.windll.LoadLibrary('accessibilityService/nvdaControllerClient/nvdaControllerClient64.dll')

#this function handles the announcement of pages using the ncdaControllerClient.dll file
def nvdaSpeak(text):
    #gets if the platform is 32 bits or 64 bits
    try:
        clientLib = ctypes.windll.LoadLibrary('accessibilityService/nvdaControllerClient/nvdaControllerClient32.dll')
    except:
        clientLib = ctypes.windll.LoadLibrary('accessibilityService/nvdaControllerClient/nvdaControllerClient64.dll')
    clientLib.nvdaController_speakText(text)

#function that convert text to speech with the highlighted engine
def textToSpeech():
    return {'Microsoft Hazel Desktop - English (Great Britain)': (microsoftTts, 0),
    'Microsoft Zira Desktop - English (United States)': (microsoftTts, 1),}

#the google text to speech function is for future release 
'''def googleTts(text, voice, rate, volume):
    try:
        tts = gTTS(text)
        tts.save('talk.mp3')
    except:
        msg = 'The google TTS requires the internet to function.'
        dlg = MessageDialog(None, msg, 'Connection Error!', style=ICON_EXCLAMATION)
        dlg.ShowModal()
        dlg.Destroy()'''

#the microsoft text to speech function; set its properties (voice, rate and volume)
def microsoftTts(text, voice, rate, volume):
    tts = msTts()
    voices = tts.getProperty('voices')
    tts.setProperty('voice', voices[voice].id)
    tts.setProperty('rate', int(rate) *5)
    tts.setProperty('volume', int(volume) /100)
    tts.say(text)
    tts.runAndWait()
