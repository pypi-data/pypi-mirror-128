import webbrowser
from pynput.keyboard import Key,Controller

key = Controller()

for i in range(50):
    key.press(Key.media_volume_up)
    key.release(Key.media_volume_up)
webbrowser.open('https://www.youtube.com/watch?v=uKxyLmbOc0Q')
