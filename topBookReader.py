
from sys import argv
from wx import App

#for the main application

#subclass the wx.App class
class TopBookReaderApp(App):
    pass

if __name__ == '__main__':
    app = TopBookReaderApp()
    from topBookReaderGui.topBookReaderFrame import TopBookReaderFrame    #imports the topBookReaderFrame here
        #takes the 2nd commandline arg for the file path if does exist
    file = argv[1] if len(argv) > 1 else ''
    frame = TopBookReaderFrame(file)
    app.MainLoop()
