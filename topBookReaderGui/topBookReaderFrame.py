
'''
* Coding: UTF-8
* Author: Oghenetejiri Peace Onosajerhe (peaceonosajerhe@gmail.com).
* topBookReaderFrame.py
* A part of TOP BOOK Reader.
* Licensed under the Massachusetts Institute of Technology (MIT);
* Copyright (C) 2023 Oghenetejiri Peace Onosajerhe.
'''


from time import sleep
from wx import (Bitmap, BITMAP_TYPE_PNG,
    Frame,)
from wx.adv import (Sound, SplashScreen,
    SPLASH_CENTRE_ON_SCREEN, SPLASH_TIMEOUT,)

from topBookReaderGui.topBookReaderMenubar import TopBookReaderMenuBar
from topBookReaderGui.topBookReaderPanel import TopBookReaderPanel

#the main frame/window of the app
class TopBookReaderFrame(Frame):
    '''
    this class serves as the main window of the app.
    Has  a parameter (file)  that requires a string.
    '''

    def __init__(self, file):
        super().__init__(None, -1, 'TOP Book Reader', size=(800, 600))

        #play the startup sound file of the app
        sound = Sound('resources/sounds/startup.wav')
        sound.Play()
        #display the app icon
        appIcon = Bitmap('resources/icons/startUpIcon.png', BITMAP_TYPE_PNG)
        startSplash = SplashScreen(appIcon, SPLASH_CENTRE_ON_SCREEN | SPLASH_TIMEOUT, 4000, None, -1)
        self.SetSize(startSplash.GetSize())
        sleep(4)

        self.Maximize()    #maximizes the window by default
        #instantiate the toolbar object
        self.toolBar = self.CreateToolBar()
        self.pnl = TopBookReaderPanel(self)    #instantiates the TopBookReaderPanel object
        #open the file through the app if clicked
        file = file
        if file:
            self.pnl.displayContent(file)

        #instantiate the EbarMenuBar object
        self.__menuBar = TopBookReaderMenuBar(self)
        self.SetMenuBar(self.__menuBar)    #add it to the main window
        self.Show()
