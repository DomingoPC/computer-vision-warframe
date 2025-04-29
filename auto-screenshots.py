# Reference: https://github.com/sohumcs/auto-clicker/blob/master/auto-clicker.py

from pynput import keyboard, mouse # Monitor and control keyboard and mouse
from threading import Thread # To allow Python to detect key presses while the process is running
import time # Control the cadence of actions
from PIL import ImageGrab # Screenshots

# Scroll and Screenshot
def process():
    count = 0
    while True:
        if activate:
            print('Taking a screenshot')
            name = 'screenshot_' + str(count) + '.png'
            count += 1
            ImageGrab.grab().save(f'screenshots/{name}')
            time.sleep(0.2)

            print('Scrolling')
            mouse_control.scroll(0, -2)
            time.sleep(0.2)

# Detect key press
def on_press(key):
    global activate # to modify var
    try:
        # Press 'f' to start the process
        if key.char.lower() == 'f':
            activate = not activate
            print(f'Active: {activate}')
    except AttributeError:
        print('special key {0} pressed'.format(key))
        if key == keyboard.Key.esc:
            # Stop listener
            return False

def main():
    # Initial message
    print('Press "f" to start scrolling and taking screenshots')
    print('Press "f" again to stop momentarily the process')
    print('Press "esc" to kill the instance')
    
    # Start process thread
    # daemon = True: mark thread as daemon (when the main program exists, it stops too)
    process_thread = Thread(target=process, daemon=True)
    process_thread.start()

    # Collect events until released
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == '__main__':
    # Initialization
    mouse_control = mouse.Controller()
    activate = False

    # Start script
    main()