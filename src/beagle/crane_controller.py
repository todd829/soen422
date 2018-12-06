from pynput import keyboard
import sys


class MoveStrategy:

    def start(self):
        pass
    
    def stop(self):
        pass

    def is_moving(self):
        pass


class MoveUpStrategy(MoveStrategy):

    def __init__(self):
        self._is_moving = False

    def start(self):
        self._is_moving = True
        # TODO Add implementation
        print("\nstart moving up\n");
    
    def stop(self):
        self._is_moving = False
        # TODO Add implementation
        print("\nstop moving up\n");
    
    def is_moving(self):
        return self._is_moving


class MoveLeftStrategy(MoveStrategy):

    def __init__(self):
        self._is_moving = False

    def start(self):
        self._is_moving = True
        # TODO Add implementation
        print("\nstart moving left\n");
    
    def stop(self):
        self._is_moving = False
        # TODO Add implementation
        print("\nstop moving left\n");
    
    def is_moving(self):
        return self._is_moving


class MoveDownStrategy(MoveStrategy):

    def __init__(self):
        self._is_moving = False

    def start(self):
        self._is_moving = True
        # TODO Add implementation
        print("\nstart moving down\n");
    
    def stop(self):
        self._is_moving = False
        # TODO Add implementation
        print("\nstop moving down\n");
    
    def is_moving(self):
        return self._is_moving


class MoveRightStrategy(MoveStrategy):

    def __init__(self):
        self._is_moving = False

    def start(self):
        self._is_moving = True
        # TODO Add implementation
        print("\nstart moving right\n");
    
    def stop(self):
        self._is_moving = False
        # TODO Add implementation
        print("\nstop moving right\n");
    
    def is_moving(self):
        return self._is_moving
        

class MovementCommand:

    def __init__(self):
        self.move_up = MoveUpStrategy()
        self.move_left = MoveLeftStrategy()
        self.move_down = MoveDownStrategy()
        self.move_right = MoveRightStrategy()

        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()

    def on_press(self, key):

        move_by_key_press = {
            keyboard.KeyCode.from_char('w'): self.move_up,
            keyboard.KeyCode.from_char('a'): self.move_left,
            keyboard.KeyCode.from_char('s'): self.move_down,
            keyboard.KeyCode.from_char('d'): self.move_right
        }

        if key in move_by_key_press.keys():
            if move_by_key_press[key].is_moving() == False:
                move_by_key_press[key].start()
                # print('press', move)

    def on_release(self, key):

        if key == keyboard.Key.esc:
            self.end()

        move_by_key_release = {
            keyboard.KeyCode.from_char('w'): self.move_up,
            keyboard.KeyCode.from_char('a'): self.move_left,
            keyboard.KeyCode.from_char('s'): self.move_down,
            keyboard.KeyCode.from_char('d'): self.move_right
        }

        if key in move_by_key_release.keys():
            if move_by_key_release[key].is_moving() == True:
                move_by_key_release[key].stop()
                # print('release', move)

    def end(self):
        sys.exit(1)


if __name__ == '__main__':
    MovementCommand()
    
