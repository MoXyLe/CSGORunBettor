from pywinauto import application
from pywinauto import clipboard
from pywinauto import keyboard
import time

def getCode():
    app = application.Application(backend="uia")
    app.start(r'C:\Users\roofu\Desktop\SDA-1.0.10\Steam Desktop Authenticator.exe',
              timeout=5)
    time.sleep(5)
    keyboard.send_keys("2000{ENTER}")
    time.sleep(7)
    sda = app.window_(title_re="Steam Desktop Authenticator")
    sda.Copy.click()
    code = clipboard.GetData()
    sda.close()
    return code
