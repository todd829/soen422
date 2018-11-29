from pynput import keyboard
import sys


move = {
    'up': False,
    'left': False,
    'down': False,
    'right': False
}


def on_press(key):

    key_press = {
        keyboard.KeyCode.from_char('w'): 'up',
        keyboard.KeyCode.from_char('a'): 'left',
        keyboard.KeyCode.from_char('s'): 'down',
        keyboard.KeyCode.from_char('d'): 'right'
    }

    if key in key_press.keys():
        if move[key_press[key]] == False:
            move[key_press[key]] = True
            print('press', move)


def on_release(key):

    if key == keyboard.Key.esc:
        end()

    key_release = {
        keyboard.KeyCode.from_char('w'): 'up',
        keyboard.KeyCode.from_char('a'): 'left',
        keyboard.KeyCode.from_char('s'): 'down',
        keyboard.KeyCode.from_char('d'): 'right'
    }

    if key in key_release.keys():
        if move[key_release[key]] == True:
            move[key_release[key]] = False
            print('release', move)


def end():
    sys.exit(1)


if __name__ == '__main__':
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
