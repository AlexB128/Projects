# pyinstaller --onefile area_capture.py
import time
import keyboard
import mouse
import win32.win32clipboard as clip
from io import BytesIO
from PIL import ImageGrab
import boto3

idx = 0
rect = [(0,0),(0,0)]

def screen_shot_to_clipboard():
    img = ImageGrab.grab(bbox = [rect[0][0], rect[0][1], rect[1][0], rect[1][1]])
    output = BytesIO()
    img.convert("RGB").save(output, "BMP")
    data = output.getvalue()[14:]
    output.close()

    clip.OpenClipboard()
    clip.EmptyClipboard()
    clip.SetClipboardData(clip.CF_DIB, data)
    clip.CloseClipboard()
    print("Rect {} copied to clipboard".format(rect))

def screen_shot_to_file():
    screen_shot_to_clipboard()
    
    curr_time = time.strftime("_%Y%m%d_%H%M%S")
    img = ImageGrab.grab(bbox = [rect[0][0], rect[0][1], rect[1][0], rect[1][1]])
    filename = "image{}.png".format(curr_time)
    img.save(filename)
    print("{} saved".format(filename))

    file_name = filename
    bucket_name = 'landing-841592256165'

    try:
        s3_client = boto3.client(
            's3',
            aws_access_key_id='AKIA4H4WOW2SVPPVW66K',
            aws_secret_access_key='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'
        )

        response = s3_client.upload_file(file_name, bucket_name, "image.png")
    except Exception as e:
        print( "<p>Error: %s</p>" % str(e) )

def hook_mouse_event():
    print("Hook mouse start")
    mouse.on_button(get_mouse_drag, buttons=('left'), types=('up','down'))

def get_mouse_drag():
    global idx
    rect[idx] = mouse.get_position()

    if idx == 0:
        idx = 1
    else:
        idx = 0
        print("Hook mouse end: {}".format(rect))
        mouse.unhook_all()
        screen_shot_to_file()

if __name__ == "__main__":
    select_rect_keys = "windows+shift+s"
    capture_keys = "ctrl+alt+s"
    end_keys = "shift+esc"
    
    keyboard.add_hotkey(select_rect_keys, hook_mouse_event)
    keyboard.add_hotkey(capture_keys, screen_shot_to_file)
    # wouldn't work with three add_hotkey
    # keyboard.add_hotkey("ctrl+alt+c", screen_shot_to_clipboard)

    print("{:<15} : Select screen area and capture".format(select_rect_keys))
    print("{:<15} : Capture".format(capture_keys))
    print("{:<15} : End the program".format(end_keys))

    keyboard.wait(hotkey='shift+esc')