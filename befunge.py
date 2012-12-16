#!/usr/bin/env python
import sys
import random

class StackException(Exception):
    pass

class IllegalOpCodeException(Exception):
    pass

class BefungeStack(object):
    """Simulates a stack

    """

    def __init__(self):
        self.stack = []

    def push(self,a):
        """Push a value onto the stack

        """
        self.stack.append(a)

    def pop(self):
        """Pop a value from the stack
        Raise StackException on empty stack

        """
        if(len(self.stack) > 0):
            return self.stack.pop()
        else:
            return 0
            #raise StackException("pop from empty stack")

    def peek(self):
        """Return a value form the stack
        Raise StackException on empty stack

        """
        if(len(self.stack) > 0):
            return self.stack[-1]
        else:
            return 0 
            #raise StackException("pop from empty stack")

    def __len__(self):
        return len(self.stack)

    def __str__(self):
        return ','.join([str(x) for x in self.stack])

class BefungeText(object):
    """Holds contents of befunge program.

    """

    def __init__(self, f):
        """Load the program from a file

        Parameters:
        f - file name of program
        """
        self.text = []
        self._load_program(f)

    def _load_program(self, f):
        """Load the contents of file row by row
        Strip whitespace from right side

        Parameters:
        f - file name of program
        """
        for x in open(f, 'r'):
            self.text.append(list(x.rstrip()))

    def _number_of_rows(self):
        """Return the number of rows in the program

        """
        return len(self.text)

    def _length_of_row(self, x):
        """Return the length of the given row

        Parameters:
        x - row number

        """
        return len(self.text[x])

    def _add_row(self, value=None):
        """Add a row to the program
        If value not specified, then empty row added

        Parameters:
        value = list of characters

        """
        if value==None:
            self.text.append([])
        else:
            self.text.append(value)

    def get(self, x, y):
        if(x >= self.number_of_rows() or y >= self.length_of_row(x)):
            return ' '
        else:
            return self.text[x][y]

    def put(self, x, y, z):
        """Implment 'p' command and alter text
        If x and/or y are beyond current program bounds
        add empty rows and whitespace

        Parameters:
        x - row number
        y - column number
        z - value

        """
        # If the put value is beyond our current amount of rows
        if(x >= self._number_of_rows()):
            # Add dummy empty rows until row
            for r in xrange(self._number_of_rows(), x):
                self._add_row()
            # Add row, left padded with whitespace
            self._add_row(list("%s%s" % (" " * (y-1), z)))
        # Else if y is past the current row length
        elif(y >= self.length_of_row(x)):
            # Append whitespace and value
            self.text[x] = list("%s%s%s" % (self.text[x], " " * (y - self._length_of_row(x)), z))
        # Otherwise modify whats currently there
        else:
            self.text[x][y] = z

    def get_next_pc(self, pc, direction):
        """Get the next pc based on direction
        Wrap around in x,y directions
        Skip sparse rows, but not sparse columns

        """
        x, y = pc
        # If left or right, just mod with current row length
        if direction == Direction.RIGHT:
            return (x, (y+1) % self.length_of_row(x))
        # Negative values work the way we want :-)
        elif direction == Direction.LEFT:
            return (x, (y-1) % self.length_of_row(x))
        # Down / up might require row skipping
        else:
            if direction == Direction.DOWN:
                increment = 1
            if direction == Direction.UP:
                increment = -1
            x = (x + increment) % self.number_of_rows()
            # Skip rows while they don't have an opcode at that y
            # We might get stuck here...
            while(y >= self.length_of_row(x)):
                x = (x + increment) % self.number_of_rows()
            return (x,y)

    def __str__(self):
        ret = ''
        for row in self.text:
            ret += '%s\n' % (''.join(row))
        return ret

class Direction():
    LEFT, RIGHT, DOWN, UP = "LEFT", "RIGHT", "DOWN", "UP"

class BefungeProgram(object):
    """Holds the state of a befunge program and runs it

    """
    def __init__(self, f):
        """Initialize text with file, empty stack and (0,0) pc

        Parameters:
        f - file

        """
        self.text = BefungeText(f)
        self.stack = BefungeStack()
        self.pc = (0,0)
        self.direction = Direction.RIGHT
        self.op = ' '
        self.ascii_mode = False
        self.finished = False

    def step(self):
        """Step through another iteration.
        Get pc value and tell handl_operator to run it

        """
        self.op = self.text.get(*self.pc)
        # Not in ascii mode, so check opcode
        if not self.ascii_mode and not self.op in BefungeProgram.op_map:
            raise IllegalOpCodeException('%s,%s: %s' % (self.pc[0],self.pc[1], self.op))
        elif not self.ascii_mode:
            BefungeProgram.op_map[self.op](self)
        # In ascii mode
        else:
            # End ascii mode
            if self.op == '"':
                BefungeProgram.op_toggle_push_ascii(self)
            # Read in with peusdo opcode
            else:
                BefungeProgram.pseudo_op_ascii_mode(self)
        self.pc = self.text.get_next_pc(self.pc, self.direction)


    def run(self):
        while not self.finished:
            self.step()
        print ""
        #print self.stack

    def pseudo_op_ascii_mode(program):
        """Get int value of ascii char at current pc location
        """
        program.stack.push(ord(program.text.get(*program.pc)))

    def op_push_int(program):
        """Push an integer onto the stack
        """
        program.stack.push(int(program.op))

    def op_addition(program):
        """Pop a,b then push a+b
        """
        stack = program.stack
        stack.push(stack.pop() + stack.pop())

    def op_subtraction(program):
        """Pop a,b then push b-a
        """
        stack = program.stack
        a = stack.pop()
        b = stack.pop()
        stack.push(b - a)

    def op_division(program):
        """Pop a,b then push b/a
        """
        stack = program.stack
        a,b = stack.pop(), stack.pop()
        stack.push(b/a)

    def op_multiplication(program):
        """Pop a,b then push a*b
        """
        stack = program.stack
        stack.push(stack.pop() * stack.pop())

    def op_modulo(program):
        """Pop a,b then push b%a
        """
        stack = program.stack
        a,b = stack.pop(), stack.pop()
        stack.push(b%a)

    def op_logical_not(program):
        """Pop a, if a==0 push 1, else push 0
        """
        stack = program.stack
        a = stack.pop()
        if a == 0:
            stack.push(1)
        else:
            stack.push(0)

    def op_greater_than(program):
        """Pop a,b, if b>a push 1, else push 0
        """
        stack = program.stack
        a,b = stack.pop(), stack.pop()
        if b > a:
            stack.push(1)
        else:
            stack.push(0)

    def op_move_right(program):
        """Change direction to right
        """
        program.direction = Direction.RIGHT

    def op_move_left(program):
        """Change direction to right
        """
        program.direction = Direction.LEFT

    def op_move_up(program):
        """Change direction to up
        """
        program.direction = Direction.UP

    def op_move_down(program):
        """Change direction to down
        """
        program.direction = Direction.DOWN

    def op_move_random(program):
        """Change direction to random
        """
        program.direction = [Direction.LEFT, Direction.RIGHT, Direction.UP, Direction.DOWN][random.randint(0,3)]

    def op_move_horizontal(program):
        """Pop value, move right if 0, otherwise left
        """
        if program.stack.pop() == 0:
            program.direction = Direction.RIGHT
        else:
            program.direction = Direction.LEFT

    def op_move_vertical(program):
        """Pop value, move down if 0, otherwise up
        """
        if program.stack.pop() == 0:
            program.direction = Direction.DOWN
        else:
            program.direction = Direction.UP

    def op_toggle_push_ascii(program):
        """Toggle program ascii mode
        """
        program.ascii_mode = not program.ascii_mode

    def op_duplicate(program):
        """Duplicate value on top of stack
        """
        program.stack.push(program.stack.peek())

    def op_swap(program):
        """Swap two values on top of stack
        """
        stack = program.stack
        a, b = stack.pop(), stack.pop()
        stack.push(a)
        stack.push(b)

    def op_pop(program):
        """Pop value from stack
        """
        program.stack.pop()

    def op_print_int(program):
        """Pop a and print as integer
        """
        a = program.stack.pop()
        sys.stdout.write(str(a) + ' ')

    def op_print_chr(program):
        """Pop a and print as chr
        """
        a = program.stack.pop()
        sys.stdout.write(chr(a))

    def op_trampoline(program):
        """Skip next cell
        """
        program.pc = program.text.get_next_pc(program.pc, program.direction)


    def op_input_int(program):
        """Ask user for integer input and push on stack
        """
        is_int = False
        while(not is_int):
            try:
                a = int(raw_input())
                is_int = True
            except ValueError:
                pass
        program.stack.push(a)

    def op_input_chr(program):
        """Ask user for a single char and push on stack
        """
        program.stack.push(ord(raw_input()[0]))

    def op_noop(program):
        """Do nothing
        """
        pass
    
    def op_exit(program):
        """Mark program as finished
        """
        program.finished = True

    """Map operators to function handlers
    """
    op_map = {
        # Integers
        '0': op_push_int, '1': op_push_int, '2': op_push_int, '3': op_push_int,
        '4': op_push_int, '5': op_push_int, '6': op_push_int, '7': op_push_int,
        '8': op_push_int, '9': op_push_int,
        # Math
        '+': op_addition, '-': op_subtraction,
        '*': op_multiplication, '/': op_division, '%': op_modulo,
        # Movement
        '>': op_move_right, '<': op_move_left, '^': op_move_up, 'v': op_move_down,
        '?': op_move_random, '_': op_move_horizontal, '|': op_move_vertical,
        # Stack
        '"': op_toggle_push_ascii, ':': op_duplicate, '\\': op_swap, '$': op_pop,
        # Print
        '.': op_print_int, ',': op_print_chr,
        # Code
        '#': op_trampoline, 'p': None, 'g': None,
        # Input
        '&': op_input_int, '~': op_input_chr,
        ' ': op_noop,
        '@': op_exit
    }


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "befunge.py FILE"
    else:
        p = BefungeProgram(sys.argv[1])
        p.run()
