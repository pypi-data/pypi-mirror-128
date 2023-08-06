import wx
from .PyParams import Wolf_Param

def main():
    ex = wx.App()
    frame = Wolf_Param(None,"Params")
    ex.MainLoop()

if __name__=="__main__":
    main()