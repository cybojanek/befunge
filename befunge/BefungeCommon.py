import termcolor

class StackException(Exception):
    pass

class IllegalOpCodeException(Exception):
    pass

class OpCodeNotImplemented(Exception):
    pass

class Direction():
    LEFT, RIGHT, DOWN, UP = "LEFT", "RIGHT", "DOWN", "UP"
    ALL = [LEFT,RIGHT,DOWN,UP]
    OPPOSITE = {
        LEFT: RIGHT,
        RIGHT: LEFT,
        UP: DOWN,
        DOWN: UP
    }
    TURN_LEFT = {
        LEFT: DOWN,
        RIGHT: UP,
        UP: LEFT,
        DOWN: RIGHT
    }
    TURN_RIGHT = {
        LEFT: UP,
        RIGHT: DOWN,
        UP: RIGHT,
        DOWN: LEFT
    }

class BefungeMode(object):
    OP, ASCII, JUMP, FINISHED = "OP", "ASCII", "JUMP", "FINISHED"

class Color():
    @staticmethod
    def blue(x):
        return termcolor.colored(x, 'blue')
    @staticmethod
    def grey_on_green(x):
        return termcolor.colored(x, 'grey', 'on_green')
    @staticmethod
    def yellow_dark(x):
        return termcolor.colored(x, 'yellow', attrs=['dark'])