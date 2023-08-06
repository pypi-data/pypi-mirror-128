
import os
import gettext
try:
    t = gettext.translation('base', localedir=os.path.dirname(__file__)+'\\..\\locales', languages=['fr'])
except:
    t = gettext.translation('base', localedir='wolfhece\\locales', languages=['fr'])
t.install()

import wx
from ..PyGui import HydrologyModel

def main(strmydir=''):
    ex = wx.App()
    exLocale = wx.Locale()
    exLocale.Init(wx.LANGUAGE_ENGLISH)
    mydro=HydrologyModel()
    ex.MainLoop()

if __name__=='__main__':
    main()