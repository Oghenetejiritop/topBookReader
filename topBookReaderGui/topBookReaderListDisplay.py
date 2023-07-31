
#for the list control display
import wx
import wx.lib.mixins.listctrl as listControl

#create the list control
class TopBookReaderListDisplay(wx.ListView, listControl.ListCtrlAutoWidthMixin):

    def __init__(self, parent, *args):
        wx.ListView.__init__(self, parent, wx.ID_ANY, style=(wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.LC_HRULES | wx.LC_VRULES))
        listControl.ListCtrlAutoWidthMixin.__init__(self)

        #insert the respective columns
        for number, column in enumerate(args):
            self.InsertColumn(number, column)
