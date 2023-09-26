
'''
* Coding: UTF-8
* Author: Oghenetejiri Peace Onosajerhe (peaceonosajerhe@gmail.com).
* topBookReaderMenuBar.py
* A part of TOP BOOK Reader.
* Licensed under the Massachusetts Institute of Technology (MIT);
* Copyright (C) 2023 Oghenetejiri Peace Onosajerhe.
'''


from webbrowser import open as webOpener

from wx import (    Bitmap, BITMAP_TYPE_PNG,
    FileDialog, FD_CHANGE_DIR, FD_FILE_MUST_EXIST, FD_SAVE, FD_OVERWRITE_PROMPT, ID_OK,
    MenuBar, Menu, EVT_MENU, EVT_MENU_HIGHLIGHT,
    PrintDialog,)
from wx.adv import AboutDialogInfo, AboutBox

from topBookReaderGui.topBookReaderAddBookmarkDialog import TopBookReaderAddBookmarkDialog
from topBookReaderGui.topBookReaderBookmarkListDialog import TopBookReaderBookmarkListDialog
from topBookReaderGui.topBookReaderDictionaryDialog import TopBookReaderDictionaryDialog
from topBookReaderGui.topBookReaderExitDialog import TopBookReaderExitDialog
from topBookReaderGui.topBookReaderGoToPageDialog import TopBookReaderGoToPageDialog
from topBookReaderGui.topBookReaderTableOfContentDialog import TopBookReaderTableOfContentDialog
from topBookReaderGui.topBookReaderRecommendedDownloadSitesDialog import TopBookReaderRecommendedDownloadSitesDialog
from topBookReaderGui.topBookReaderExtras.topBookReaderFunc import openFileContent

#menubar for the application
class TopBookReaderMenuBar(MenuBar):
    '''
    this class controls the menubar component that houses the (file, edit, pages/bookmark, menu items and so on).
    Has  a parameter (parent)  that requires the topBookReaderFrame object.
    '''

    def __init__(self, parent):
        super().__init__()

        self.__parent = parent
        #reference the toolbar object
        self.__toolBar = self.__parent.toolBar
        self.__addTools(self.__toolBar)    #adds the tools to the toolBar
        self.__displayedContent = self.__parent.pnl.cloneDisplayedText()    #gets the reference to the displayedContent component of the app

        self.__menuDict = {}    #a dictionary that will be holding each menu  and its menu items (children)

        #invoke the menu items to the screen
        self.__createMenuItem()    #invoke the menu items to the screen

    #methods defined

    #method that decides the boolean state of a menu item
    def __getMenuState(self):
        #store either True or False values in these instance variables when the following conditions are met;
        #(if a document is opened); (if a portion of text is selected) and (if the contentDisplay area is editable).
        self.__isBookOpenedDecider = False if self.__parent.pnl.isBookOpened() else True
        self.__selectionDecider = True if self.__displayedContent.GetStringSelection() else False
        self.__editableDecider =True if self.__displayedContent.IsEditable() else False

    #method that returns the label and event handler of each tool
    def __toolBarInfo(self):
        return (
        ('Open A Document', 'open', self.on_openDocument),
        ('Exit Program', 'exit', self.on_exit),
        ('Add To Bookmark...', 'bookmark', self.on_addToBookmarks),
        ('View Bookmark History...', 'bookmarkHistory', self.on_viewBookmarks),
        ('Font Adjustments...', 'font', self.on_adjustFont),
        ('Access Word In Dictionary...', 'dictionary', self.on_dictionary),
        )

    #method that implements the toolbar component; 
    #accepts four parameters: toolBar (the ToolBar object), id (-1), label (str) and evtHandler (event handler)
    def __implementTool(self, toolBar, id, label, icon,  evtHandler):
        tool = toolBar.AddTool( id, label, icon, label)
        self.__parent.Bind(EVT_MENU, evtHandler, tool)
        toolBar.AddSeparator()

    #create the toolbar on the screen
    def __addTools(self, toolBar):
        #unpack the .__toolBarInfo()
        for label, icon, evtHandler in self.__toolBarInfo():
            bmp = Bitmap(f'resources/icons/{icon}.png', BITMAP_TYPE_PNG)    #gets the bitmap icon
            self.__implementTool(toolBar, -1, label, bmp, evtHandler)    #implements the tool
        toolBar.Realize()

    #method that returns the menu item and its submenu components (label and event handler)
    def __menuInfo(self):
        return (
        ('&File',    #for the file menu item
            (('&Open Document...\tctrl+o', self.on_openDocument),
            ('&Save File...\tctrl+s', self.on_saveFile),
            ('&Print File...\tctrl+p', self.on_printFile),
            ('&Exit Program...\talt+f4', self.on_exit),)),

        ('&Edit',    #for the edit menu item
            (('&Copy Content\tctrl+c', self.on_copy),
            ('C&ut Content\tctrl+x', self.on_cut),
            ('&Paste Content\tctrl+v', self.on_paste),
            ('&Undo \tctrl+z', self.on_undo),)),

        ('Pages/&Bookmarks',    #for the pages/bookmarks menu item
            (('&Add To Bookmarks...\tctrl+b', self.on_addToBookmarks),
            ('&View Bookmarks...\tctrl+shift+b', self.on_viewBookmarks),
            ('&Go To Page...\tctrl+g', self.on_goToPage),
            ('Vie&w Table Of Content...\tctrl+shift+t', self.on_viewBookContent),)),

        ('Vie&w',    #for the view menu item
            (('&Zoom In \talt+i', self.on_zoomIn),
            ('&Zoom Out\talt+o', self.on_zoomOut),
            ('&Adjust Fonts...\tctrl+f', self.on_adjustFont),)),

        ('&Advance',    #for the advance menu item
            (('&Access Dictionary Meaning...\tctrl+d', self.on_dictionary),
            ('&Download More Books Through Here\tctrl+r', self.on_downloadBook),)),

        ('&Help',    #for the help menu item
            (('&About TOP Book Reader...\tctrl+shift+a', self.on_about),
            ('&User\'s Guide\tf1', self.on_userGuide),
            ('&View License...\tctrl+shift+l', self.on_license),
            ('&Check For Update...\tf2', self.on_appUpdate),
            ('&Visit Website\tctrl+w', self.on_website),)),
        )

    #method that creates each menu item and adds it to the menubar
    def __createMenuItem(self):
        counter = 0    #set a unique id for each parent menu

        #unpack the __menuInfo
        for menuItemLabel,  menuItemInfo in self.__menuInfo():
            menu= Menu()    #creates a new menu
            self.__menuDict[counter] = [menu]    #store each menu and its menu items in a dictionary

            #unpack each menu's child item label and its event handler
            for item in menuItemInfo:
                menuChildItem = menu.Append(-1, item[0])
                self.__menuDict[counter].append(menuChildItem)    #appends each menuChildItem to its respective dictionary key address

                #invoke each menu update event handler for their current state of operation
        #the state update for the edit menu items
                self.__parent.Bind(EVT_MENU_HIGHLIGHT, self.on_updateEditMenuState, menuChildItem) if menuItemLabel.startswith('&E') else None
        #the status update for the pages/bookmarks menu items
                self.__parent.Bind(EVT_MENU_HIGHLIGHT, self.on_updatePagesBookmarksMenuState, menuChildItem) if menuItemLabel.startswith('P') else None
        #the status update for the help menu items
                self.__parent.Bind(EVT_MENU_HIGHLIGHT, self.on_updateHelpMenuState, menuChildItem) if menuItemLabel.startswith('&H') else None

                #bind each menu item child's event to the frame
                self.__parent.Bind(EVT_MENU, item[1], menuChildItem)
            menu.AppendSeparator()    #create a demarcation from each menu item collection
            self.Append(menu, menuItemLabel)
            counter += 1    #increments counter by 1


    #events associated with this class

    #file menu item
    #event that handles the opening of documents
    def on_openDocument(self, event):    #select a file using this dialog
        #set the wild card
        wildcard = 'Supported Files (*.docx;*.epub;*.pdf;*.rtf;*.txt)|*.docx;*.epub;*.pdf;*.rtf;*.txt|Word Document (*.docx)|*.docx|Electronic Publisher (*.epub)|*.epub|Portible Document Format (*.pdf)|*.pdf|Rich Text Format (*.rtf)|*.rtf|Text File (*.txt)|*.txt'
        dlg = FileDialog(None, 'Open A Book', wildcard=wildcard, style=FD_CHANGE_DIR | FD_FILE_MUST_EXIST)
        if dlg.ShowModal() == ID_OK:
            self.__parent.pnl.displayContent(dlg.GetPath())
            dlg.Destroy()

    #event that handles the saving of plain text file
    def on_saveFile(self, event):
        wildcard = 'Text File (*.txt)|*.txt'    #set the wild card to a text file
        dlg = FileDialog(None, 'Save File Content', wildcard=wildcard, style=(FD_CHANGE_DIR | FD_SAVE|FD_OVERWRITE_PROMPT))
        #save the text on the displayedContent into a text file
        if dlg.ShowModal() == ID_OK:
            path = dlg.GetPath()
            savedFile = self.__displayedContent.SaveFile(path)
            dlg.Destroy()

    #event that handles the printing out of documents
    def on_printFile(self, event):
        dlg = PrintDialog(None)
        dlg.ShowModal()
        dlg.Destroy()

    #event that handles the exitting action
    def on_exit(self, event):
        #close the window if there's no book opened
        if self.__parent.pnl.isBookOpened():
            self.__parent.Close(True)
            return

        #otherwise, prompt for a confirmation before closed
        dlg = TopBookReaderExitDialog(self.__parent)
        dlg.ShowModal()

    #for the edit menu item
    #event that handles the copying of text
    def on_copy(self, event):
        self.__displayedContent.Copy()

    #event that handles the cutting of text
    def on_cut(self, event):
        self.__displayedContent.Cut()

    #event that handles the pasting of text
    def on_paste(self, event):
        self.__displayedContent.Paste()

    #event that undoes an action
    def on_undo(self, event):
        self.__displayedContent.Undo()

    #event that serve as status update to the edit menu state
    def on_updateEditMenuState(self, event):
        editMenuItems = self.__menuDict[1]    #gets the menu references of the edit menu item
        self.__getMenuState()   #calls the .__menuState() method to determine its deciders

        #iterate through each edit menu item reference to access its state (deciders)
        #to determine if the item is either enabled or disabled.
        for menuObj in editMenuItems[1:3]:
            editMenuItems[0].Enable(menuObj.GetId(), self.__selectionDecider)

        for menuObj in editMenuItems[3:]:
            editMenuItems[0].Enable(menuObj.GetId(), self.__editableDecider)

    #for the pages/bookmarks menu item
    #event that performs the bookmark action
    def on_addToBookmarks(self, event):
        dlg = TopBookReaderAddBookmarkDialog(self.__parent)
        dlg.ShowModal()
        dlg.Destroy()

    #event that handles the viewing of bookmarks
    def on_viewBookmarks(self, event):
        dlg = TopBookReaderBookmarkListDialog(self.__parent)
        dlg.ShowModal()
        dlg.Destroy()

    #event that handles the goto page feature
    def on_goToPage(self, event):
        dlg = TopBookReaderGoToPageDialog(self.__parent)
        dlg.ShowModal()
        dlg.Destroy()

    #event that handles the table of content of a document
    def on_viewBookContent(self, event):
        dlg = TopBookReaderTableOfContentDialog(self.__parent.pnl.getFileName())
        dlg.ShowModal()
        dlg.Destroy()

    #event that serve as status update to the pages/bookmarks menu state
    def on_updatePagesBookmarksMenuState(self, event):
        pageBookmarksMenuItems = self.__menuDict[2]    #gets the menu references of the pages/bookmarks menu item
        self.__getMenuState()   #calls the .__menuState() method to determine its deciders

        #access each pages/bookmarks menu item reference to determine its state (deciders)
        #to know if the item is either enabled or disabled.
        pageBookmarksMenuItems[0].Enable(pageBookmarksMenuItems[1].GetId(), self.__selectionDecider and self.__isBookOpenedDecider)
        pageBookmarksMenuItems[0].Enable(pageBookmarksMenuItems[2].GetId(), self.__isBookOpenedDecider)
        pageBookmarksMenuItems[0].Enable(pageBookmarksMenuItems[3].GetId(), self.__isBookOpenedDecider)
        pageBookmarksMenuItems[0].Enable(pageBookmarksMenuItems[4].GetId(), self.__isBookOpenedDecider)

    #for the pview menu item
    #event that performs the zoom in action
    def on_zoomIn(self, event):
        self.__displayedContent.zoomIn()

    #event that performs the zoom out action
    def on_zoomOut(self, event):
        self.__displayedContent.zoomOut()

    #event that performs the adjusting of fonts feature
    def on_adjustFont(self, event):
        self.__displayedContent.adjustFont()

    #for the advance menu item
    #event that handles the mini dictionary feature
    def on_dictionary(self, event):
        dlg = TopBookReaderDictionaryDialog()
        dlg.ShowModal()
        dlg.Destroy()

    #event that handles the downloading of books feature
    def on_downloadBook(self, event):
        dlg = TopBookReaderRecommendedDownloadSitesDialog()
        dlg.ShowModal()
        dlg.Destroy()


    #for the help menu item
    #event that pops up with the about box dialog
    def on_about(self, event):
        content = openFileContent('resources/lib/about.txt')
        aboutAppInfo = AboutDialogInfo()
        aboutAppInfo.SetName('TOP Book Reader ')
        aboutAppInfo.SetVersion('1.0')
        aboutAppInfo.SetDescription(content)
        aboutAppInfo.AddDeveloper('Oghenetejiri Peace Onosajerhe.')
        aboutAppInfo.SetCopyright('(C) 2023 Oghenetejiri Peace Onosajerhe')
        AboutBox(aboutAppInfo)

    #event that accesses the user's guide
    def on_userGuide(self, event):
        webOpener('file://e:/topBookReader/docs/userGuide.html')

    #event that pops up with the license notice
    def on_license(self, event):
        content = openFileContent('resources/lib/license.txt')
        aboutAppLicense = AboutDialogInfo()
        aboutAppLicense.SetName('TOP Book Reader License Notice')
        aboutAppLicense.SetDescription(content)
        AboutBox(aboutAppLicense)

    #event that carries out the app update process
    def on_appUpdate(self, event):
        pass

    #event that accesses the website
    def on_website(self, event):
        webOpener('https://github.com/Oghenetejiritop/topBookReader/')
    #event that serve as status update to the pages/bookmarks menu state
    def on_updateHelpMenuState(self, event):
        helpMenuItems = self.__menuDict[5]    #gets the menu references of the help menu item
        helpMenuItems[0].Enable(helpMenuItems[4].GetId(), False)
