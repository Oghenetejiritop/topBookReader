
'''
* Coding: UTF-8
* Author: Oghenetejiri Peace Onosajerhe (peaceonosajerhe@gmail.com).
* topBookReaderRecommendedDownloadSitesDialog.py
* A part of TOP BOOK Reader.
* Licensed under the Massachusetts Institute of Technology (MIT);
* Copyright (C) 2023 Oghenetejiri Peace Onosajerhe.
'''

from webbrowser import open as webOpener

from  wx import (BoxSizer, ALL, CENTER,  EXPAND, HORIZONTAL, LEFT, VERTICAL,
    Button, BU_EXACTFIT, EVT_BUTTON,
    Dialog, StaticText, ID_CANCEL,
    TextCtrl, EVT_TEXT_ENTER, TE_AUTO_URL, TE_PROCESS_ENTER, TE_MULTILINE, TE_READONLY, TE_RICH2,)

#dialog that highlights sites to download books
class TopBookReaderRecommendedDownloadSitesDialog(Dialog):
    '''
    this class recommends book sites.
    Has  no parameter.
    '''

    def __init__(self):
        super().__init__(None, title='Recommended Book Sites')

        #instantiate the vertical box sizer
        vSizer = BoxSizer(VERTICAL)

        urls = '''Looking for  your favourite books with no stress? Search no further by  visitting Z-Library and get your books for free | https://www.z-lib.is/
    Like to convert your document to any other media formats? You can visit   Zamzar | https://www.zamzar.com/
        '''

        label = StaticText(self, -1, 'Notable Sites')
        vSizer.Add(label, 0, ALL | LEFT, 5)
        self.__siteDisplay= TextCtrl(self, -1, urls, size=(500, 400), style=(TE_AUTO_URL | TE_PROCESS_ENTER | TE_READONLY | TE_MULTILINE | TE_RICH2))
        vSizer.Add(self.__siteDisplay, 0, ALL | LEFT, 10)
        self.Bind(EVT_TEXT_ENTER, self.on_visitSite, self.__siteDisplay)
  
        cancelBtn = Button(self, ID_CANCEL, 'Cancel')
        vSizer.Add(cancelBtn, 0, ALL | LEFT, 5)

        vSizer.SetSizeHints(self)
        self.SetSizer(vSizer)

    #event associated with this class
    #event that opens the website when clicked
    def on_visitSite(self, event):
        #get the whole content from the display and slice
        text = self.__siteDisplay.GetValue()
        charPos = self.__siteDisplay.GetInsertionPoint()
        text = text[charPos:]
        #find the position of the vertical bar and add 2
        #slice off the url
        startLinkPos = text.find('|') + 2
        endLinkPos = text.find('\n')
        site = text[startLinkPos:endLinkPos]

        #visit the site if highlighted
        if site.startswith('h'):
            webOpener(site)
        else:    #if no more links revert to the last link as default
            webOpener('https://www.zamzar.com/')
