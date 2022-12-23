import pystray
import win32gui, win32con
import time
import sys
import os
from threading import Thread
from PIL import Image

status = ["Windows status ", ""]
flags = [True, True, False]
hdl = [0]


image = Image.open(os.path.join(os.path.dirname(__file__), 'setWndAtTop.png'))
icon = pystray.Icon("Always At Top")
icon.icon = image

def update_status():
    i = win32gui.GetForegroundWindow()
    s = win32gui.GetWindowText(i)

    if s.strip():
        style = win32gui.GetWindowLong(hdl[0], win32con.GWL_EXSTYLE)
        f = True if style & win32con.WS_EX_TOPMOST else False
        flags[2] = s != status[1] or f != flags[1]
        flags[1] = f
        if f:
            status[0] = "Stay Top"
            status[1] = s
            hdl[0] = i
        else:
            status[0] = "Not Stay Top"
            status[1] = s
            hdl[0] = i


def set_active_window_alwaytop():
    [x, y, x1, y1] = win32gui.GetWindowRect(hdl[0])
    win32gui.SetWindowPos(hdl[0], win32con.HWND_TOPMOST, x, y, x1-x, y1-y, 0)

def set_active_window_not_alwaytop():
    [x, y, x1, y1] = win32gui.GetWindowRect(hdl[0])
    win32gui.SetWindowPos(hdl[0], win32con.HWND_NOTOPMOST, x, y, x1-x, y1-y, 0)

def stop():
    flags[0] = False
    icon.stop()

item_item1 = pystray.MenuItem(lambda text: status[0] + " - " + status[1], lambda : None)
item_item2 = pystray.MenuItem("Set Always On Top", set_active_window_alwaytop)
item_item3 = pystray.MenuItem("Set Not Always On Top", set_active_window_not_alwaytop)
item_item4 = pystray.MenuItem("Exit", stop)
menu = pystray.Menu(item_item1, item_item2, item_item3, item_item4)

icon.menu = menu

def get_active_window_status():
    while flags[0]:
        update_status()
        if flags[2]:
            icon.update_menu()
            flags[2] = False
        time.sleep(1)

thread1 = Thread(target = get_active_window_status)
thread1.start()
icon.run()


