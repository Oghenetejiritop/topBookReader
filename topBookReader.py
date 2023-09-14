
#for the main application
from wx import (App,
    Bitmap, BITMAP_TYPE_PNG,
    Yield,)
from wx.adv import (Sound, SplashScreen,
    SPLASH_CENTRE_ON_SCREEN, SPLASH_TIMEOUT,)

if __name__ == '__main__':
    app = App()
    from topBookReaderGui.topBookReaderFrame import TopBookReaderFrame    #imports the topBookReaderFrame here
    #play the startup sound file of the app
    sound = Sound('resources/sounds/startup.wav')
    sound.Play()
    #display the app icon
    appIcon = Bitmap('resources/icons/startSplash.png', BITMAP_TYPE_PNG)
    splash = SplashScreen(appIcon, SPLASH_CENTRE_ON_SCREEN | SPLASH_TIMEOUT, 6000, None, -1)
    Yield()
    frame = TopBookReaderFrame()
    app.MainLoop()