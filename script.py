'''
    This script should download a photo from mars made by perseverance and use it as desktop background image.

    TODO:
    - install guide
    - .bat for "run on start" thing
    - maybe wait for "connection ready" b4 fail (just ping google at lower rate each time)
    - generate urls and download imgs
    - add some legend to the photo (maybe PIL can do it) (no more needed libs will be awesome)
    - on saturday pic a photo from weird camera (see this)
    - on sudays pic a photo from inactive rover
    - on fridays from curiosity

    - keep log, { images: [{date: ,url:}, {..


    Nasa api: https://api.nasa.gov/mars-photos/api/v1/
    win32 code: https://www.blog.pythonlibrary.org/2014/10/22/pywin32-how-to-set-desktop-background/
    win32: [pywin32-300.win-amd64-py3.7.exe] https://github.com/mhammond/pywin32/releases
    PIL code: https://stackoverflow.com/a/65139335/13771772

    @Author: SERGI
'''

import win32api, win32con, win32gui
import requests
from random import randrange
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
#----------------------------------------------------------------------
api_key = "DEMO_KEY"

def getMaxSol(rover):
    x = requests.get("https://api.nasa.gov/mars-photos/api/v1/rovers/"+rover+"/?api_key="+api_key).json()
    return x["rover"]["max_sol"]


def getInfo(sol, cameras):
    rd = randrange(len(cameras))
    x = requests.get("https://api.nasa.gov/mars-photos/api/v1/rovers/perseverance/photos?camera="+cameras[rd]+"&sol="+str(sol)+"&api_key="+api_key).json()
    return x["photos"]

def downloadImg(url,path):
    x = requests.get(url)
    open(path, 'wb').write(x.content)

def waterMark(info, path):
    
    image = Image.open(path)
    width, height = image.size 

    draw = ImageDraw.Draw(image)

    text = info["rover"]["name"] +"\n"
    text += "sol" + info["sol"] + "\n"
    text += info["id"] + "\n"
    text += info["camera"]["fullname"] +"\n"
    text += info["earth_date"]

    textwidth, textheight = draw.textsize(text)
    margin = 10
    x = width - textwidth - margin
    y = height - textheight - margin

    draw.text((x, y), text)

    image.save(path)

def isFriday():
    curiosity_cool_cameras = ["NAVCAM","RHAZ"]
    max_sol = getMaxSol("perseverance")
    return getInfo(sol = max_sol, cameras = curiosity_cool_cameras)

def isSaturday():
    #none of these works.. :c )
    perseverance_weird_cameras = ["REAR_HAZCAM_LEFT","REAR_HAZCAM_RIGHT"]
    return notWeekend()

    pass

def isSunday():
    inactive_rovers = ["Spirit","Opportunity"]
    pass

def notWeekend():
    perseverance_normal_cameras = ["NAVCAM_RIGHT"]
    max_sol = getMaxSol("perseverance")
    return getInfo(sol = max_sol, cameras = perseverance_normal_cameras)


choose_photo = {
    1:notWeekend,
    2:notWeekend,
    3:notWeekend,
    4:notWeekend,
    5:isFriday,
    6:isSaturday,
    7:isSunday,
}


def setWallpaper(path):
    key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER,"Control Panel\\Desktop",0,win32con.KEY_SET_VALUE)
    win32api.RegSetValueEx(key, "WallpaperStyle", 0, win32con.REG_SZ, "0")
    win32api.RegSetValueEx(key, "TileWallpaper", 0, win32con.REG_SZ, "0")
    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, path, 1+2)

def downloadAndSave(path):
    # https://api.nasa.gov/mars-photos/api/v1/rovers?&api_key=DEMO_KEY
    # get date and check what to do
    weekday = datetime.isoweekday(datetime.now())
    info = choose_photo[weekday]
    rd = randrange(len(info))
    url = info[rd]["img_src"]
    downloadImg(url, path)
    waterMark(info[rd], path)


if __name__ == "__main__":
    path = r'C:\Users\Public\Pictures\img.jpg'
    downloadAndSave(path)
    setWallpaper(path)