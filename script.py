'''
    This script should download the lastest mars photo made (priority drone>perseverance>curiosity) and use it as desktop background image.

    TODO:
    - install guide
    - .bat for "run on start" thing
    - maybe wait for "connection ready" b4 fail (just ping google at lower rate each time)
    - generate urls and download imgs
    - add some legend to the photo (maybe PIL can do it) (no more needed libs will be awesome)
    - on saturday pic a photo from weird camera (see this)
    - on sudays pic a photo from inactive rover
    - keep log, { images: [{date: ,url:}, {..


    Nasa api: https://api.nasa.gov/mars-photos/api/v1/
    win32 code: https://www.blog.pythonlibrary.org/2014/10/22/pywin32-how-to-set-desktop-background/
    win32: [pywin32-300.win-amd64-py3.7.exe] https://github.com/mhammond/pywin32/releases

    @Author: SERGI
'''

import win32api, win32con, win32gui
import request
#----------------------------------------------------------------------
def setWallpaper(path):
    key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER,"Control Panel\\Desktop",0,win32con.KEY_SET_VALUE)
    win32api.RegSetValueEx(key, "WallpaperStyle", 0, win32con.REG_SZ, "0")
    win32api.RegSetValueEx(key, "TileWallpaper", 0, win32con.REG_SZ, "0")
    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, path, 1+2)

def downloadAndSave(path):
    # https://api.nasa.gov/mars-photos/api/v1/rovers?&api_key=DEMO_KEY
    pass

if __name__ == "__main__":
    path = r'C:\Users\Public\Pictures\img.jpg'
    downloadAndSaveImg(path)
    setWallpaper(path)