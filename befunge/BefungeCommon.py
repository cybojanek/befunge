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

class BefungeMode(object):
    OP, ASCII, FINISHED = "OP", "ASCII", "FINISHED"

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