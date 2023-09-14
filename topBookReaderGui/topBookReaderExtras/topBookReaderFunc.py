
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
from wx import Font, FONTFAMILY_DEFAULT, FONTSTYLE_SLANT, FONTWEIGHT_NORMAL

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
    fontObject =     Font(12, FONTFAMILY_DEFAULT, FONTSTYLE_SLANT, FONTWEIGHT_NORMAL)
    #variable to the serialised paths
    filesAndContents = (('topBookReaderRecentBookInfo.pkl', {}),
        ('topBookReaderRecentList.pkl', []),
        ('topBookReaderBookmarksHistory.pkl', {}),
        ('topBookReaderFont.pkl', [fontObject.GetPointSize(), fontObject  .GetFamily(), fontObject  .GetStyle(), fontObject  .GetWeight(), 'Blue']),)

    #create the .topBookReader directory and its serialized files if doesn't exist
    if not path.exists(topBookReaderDirectory):
        makedirs(topBookReaderDirectory)

    for file, content in filesAndContents:
        if not path.exists(f'{topBookReaderDirectory}/{file}'):
            topBookReaderPath(topBookReaderDirectory, file, content)

#function that handles the topBookReader windows registry keys
def createTopBookReaderKeys(winReg, keyAccess='r', path=''):
    accesses = {'r': winReg.KEY_READ, 'w': winReg.KEY_WRITE} 
    try:
        key = winReg.OpenKey(winReg.HKEY_CURRENT_USER, f'Software\\TOPBookReader\\{path}', access=accesses[keyAccess])
    except:
        key = winReg.CreateKey(winReg.HKEY_CURRENT_USER, f'Software\\TOPBookReader\\{path}')
        if path.endswith('voices'):
            keyNameValue = (('name', 'Microsoft Zira Desktop - English (United States)'),
            ('rate', '25'),
            ('volume', '40'),
            ('voice selection index','2'),)
            for name, value in keyNameValue:
                winReg.SetValueEx(key, name, 0,winReg.REG_SZ, value)
    return key

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
