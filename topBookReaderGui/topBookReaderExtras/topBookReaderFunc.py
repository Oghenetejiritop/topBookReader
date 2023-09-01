
'''
* Coding: UTF-8
* Author: Oghenetejiri Peace Onosajerhe (peaceonosajerhe@gmail.com).
* topBookReaderFunc.py
* A part of TOP BOOK Reader.
* Licensed under the Massachusetts Institute of Technology (MIT);
* Copyright (C) 2023 Oghenetejiri Peace Onosajerhe.
'''


#module with other functional operations
from json import load as jsonLoad
from os import  makedirs, path
from pickle import dump, load

from pyttsx3 import init as tts

from topBookReaderGui.topBookReaderExtras.topBookReaderSupport import SerializedFontData

emptyString = ''

#the function the handles the writing and reading of topBookReader serialised files
def topBookReaderPath(dir=emptyString, file=emptyString, content=None):
    fullPath = f'{dir}/{file}'
    if content != None:
        newFile = open(fullPath, 'wb')
        dump(content, newFile)
        newFile.close()
    else:
        existingFile = open(fullPath, 'rb')
        value = load(existingFile)
        existingFile.close()
        return value

#create the topBookReader paths
def createTopBookReaderPaths(topBookReaderDirectory):
    fontObject = SerializedFontData()
    #variable to the serialised paths
    filesAndContents = (('topBookReaderRecentBookInfo.pkl', {}),
        ('topBookReaderRecentList.pkl', []),
        ('topBookReaderBookmarksHistory.pkl', {}),
        ('topBookReaderFont.pkl', fontObject),)

    #create the .topBookReader directory and its serialized files if doesn't exist
    if not path.exists(topBookReaderDirectory):
        makedirs(topBookReaderDirectory)

    for file, content in filesAndContents:
        if not path.exists(f'{topBookReaderDirectory}/{file}'):
            topBookReaderPath(topBookReaderDirectory, file, content)

#for the topBookReader dictionary feature
def topBookReaderWordMeaning(word):
    dictPath = open('resources/lib/dictionary.json', 'r')
    wordList = jsonLoad(dictPath)
    dictPath.close()
    meaning = wordList.get(word.lower(), f'{word.capitalize()} not found in the dictionary!')
    return f'{meaning}'

#get the content from an opened file
def openFileContent(path):
    with open(path, 'r') as file:
        content = file.read()
    return content

#function that gets rid of unwanted characters in a given string
def unwantedCharRemover(value, unwanted):
    for char in unwanted:
        value = value.replace(char, ' ')
    return value

#function that converts text to speech
def textToSpeech(text):
    engine = tts()
    engine.say(text)
    engine.runAndWait()