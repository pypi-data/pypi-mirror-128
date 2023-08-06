import os
import gettext
try:
    t = gettext.translation('base', localedir=os.path.dirname(__file__)+'\\..\\locales', languages=['fr'])
except:
    t = gettext.translation('base', localedir='wolfhece\\locales', languages=['fr'])
t.install()

import wx
from ..PyParams import Wolf_Param

def main():
    ex = wx.App()
    frame = Wolf_Param(None,"Params")
    ex.MainLoop()

if __name__=="__main__":
    main()