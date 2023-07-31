
#for the main application
from wx import App

#import the ebar frame here
from topBookReaderGui.topBookReaderFrame import TopBookReaderFrame

if __name__ == '__main__':
    app = App()
    frame = TopBookReaderFrame()
    app.MainLoop()