
'''
* Coding: UTF-8
* Author: Oghenetejiri Peace Onosajerhe (peaceonosajerhe@gmail.com).
* topBookReaderSupport.py
* A part of TOP BOOK Reader.
* Licensed under the Massachusetts Institute of Technology (MIT);
* Copyright (C) 2023 Oghenetejiri Peace Onosajerhe.
'''


#module with supportive classes
from threading import Event, Thread
from time import sleep
from wx import Bitmap, BITMAP_TYPE_PNG

from topBookReaderGui.topBookReaderExtras.topBookReaderTts import textToSpeech as tts

class UniqueList:
    '''
    this class functions like a set (stores only unique items).
    Accepts two parameters;
    bookFile: requires the FileValidator object
    list: takes a List as an argument
    '''

    def __init__(self, bookFile, list):

        self.__bookFile = bookFile
        self.__list = list

    def append(self, item):    #append item to the list uniquely
        #remove an existing item from the list and inserts it at position 0
        if item in self.__list:
            self.__list.remove(item)
        self.__list.insert(0, item)

    def delete(self, index):    #delete an item from the list
        self.__list.pop(index)

    def clearAll(self):    #clear all items from the list
        self.__list.clear()

    def numList(self, limit=15):    #add a number to each item of the list and set a limit to its items
        newList = []
        for number, item in enumerate(self.__list):
            self.__bookFile.insertFileTemp(item)
            if number == limit:
                break
            newList.append(f'{number + 1}. {self.__bookFile.getFileTempName()} - File Path: {self.__bookFile.getTempFileSource()}: {item}')
        return newList

    def selectItem(self, index):    #access the highlighted index value
        return self.__list[index]

    #checks if the list is empty
    def isEmpty(self):
        return len(self.__list) == 0

    def output(self):    #return the list
        return self.__list


#customising the python thread
class SpeechThreadControls(Thread):
    '''
    this class extends from the Thread class; enabling it to handle pause and resume functions on the text to speech function.
    Accepts four parameters;
    target: requires a function.
    args: requires list of function arguments.
    btn: requires the wx.Button object
    winReg: requires the windows registry object
    '''

    def __init__(self, target=None, args=(), btn=None, winReg=None):
        super().__init__(group=None, target=None, name=None, args=(), kwargs=None,daemon=True)

        self.__target = target    #holds the targeted function
        self.__targ1 = args[0]    #stores the first argument
        self.__winReg = winReg
        self.__btn = btn
        self.__event = Event()    #instantiates the Event object

    #overwrite the run method of the Thread class
    def run(self):
        self.__btn.SetLabel('&Pause')    #changes the btn label to pause
        i = 0
        while True:
            #pause the thread operation and resets i to 0 when i is equivalent to the length of targ1
            if i == len(self.__targ1):
                i = 0
                self.pause()

            #sleep for a second if the event is set
            if self.__event.is_set():
                sleep(1)
            else:    #otherwise, invoke the targeted function
                self.__functionNotifier()
                self.__target(self.__targ1[i], self.__targ2, self.__targ3, self.__targ4)
                i+=1

    #method that resumes the operation when the event is cleared
    def resume(self):
        self.__event.clear()
        icon = Bitmap('resources/icons/pause.png', BITMAP_TYPE_PNG)
        self.__btn.SetBitmap(icon)
        self.__btn.SetLabel('&Pause')    #changes the btn label to pause

    #the method that pauses the operation when the event is set
    def pause(self):
        self.__event.set()
        icon = Bitmap('resources/icons/play.png', BITMAP_TYPE_PNG)
        self.__btn.SetBitmap(icon)
        self.__btn.SetLabel('&Play Aloud')    #changes the btn label to play

    #method that notifies for a function update
    def __functionNotifier(self):
        from topBookReaderGui.topBookReaderExtras.topBookReaderFunc import createTopBookReaderKeys
        #invoke the createKeys function
        voiceKey = createTopBookReaderKeys(self.__winReg, path='voices')
        #update the last three arguments of the targeted function
        name, rate, volume = self.__winReg.QueryValueEx(voiceKey, 'name')[0], self.__winReg.QueryValueEx(voiceKey, 'rate')[0], self.__winReg.QueryValueEx(voiceKey, 'volume')[0]
        #invoke the tts function
        speech = tts()
        speechOutput = speech[name]
        self.__targ2 = speechOutput[1]
        self.__targ3 = rate
        self.__targ4 = volume
