import time, termcolor, random, sys

from BefungeStack import BefungeStack
from BefungeText import BefungeText
from BefungeCommon import Direction, Color
from BefungeCommon import IllegalOpCodeException, OpCodeNotImplemented

class BefungeProgram(object):
    """Holds the state of a befunge program and runs it

    """
    def __init__(self, f, show_steps=False, operations_per_second=0):
        """Initialize text with file, empty stack and (0,0) pc

        Parameters:
        f - file
        show_steps - output program status, default=False
        operations_per_second - how many befunge ops a second, default=unlimited

        """
        self.text = BefungeText(f)
        self.stack = BefungeStack()
        self.pc = (0,0)
        self.direction = Direction.RIGHT
        self.op = ' '
        self.ascii_mode = False
        self.finished = False
        self.show_steps = show_steps
        self.operations_per_second = operations_per_second
        self.stdout_log = ''

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
        """Step through program

        """
        while not self.finished:
            if self.show_steps:
                self.show_program()
            if self.operations_per_second != 0:
                time.sleep(1.0/self.operations_per_second)
            self.step()
        print ""

    def show_program(self):
        """Print terminal colored program status

        """
        # Divider
        print Color.blue('#'*80)
        # Code header
        print "%s" % Color.yellow_dark("Code:")
        # Code
        for i in xrange(len(self.text.text)):
            row = self.text.text[i]
            # This line contains our pc
            if self.pc[1] == i:
                # Make copy and replace pc with highlighted pc
                row = row[::]
                row[self.pc[0]] = Color.grey_on_green(row[self.pc[0]])
            print ''.join([str(x) for x in row])
        # Stack
        print "%s %s" % (Color.yellow_dark("Stack N:"), self.stack)
        print "%s %r" % (Color.yellow_dark("Stack A:"), self.stack)
        # Aggregated stdout
        print "%s %s" % (Color.yellow_dark("Stdout:"), self.stdout_log),
        print ""

    def pseudo_op_ascii_mode(program):
        """Get int value of ascii char at current pc location
        """
        program.stack.push(ord(program.text.get(*program.pc)))

    def op_push_int(program):
        """Push an integer onto the stack
        """
        # Get int value in base 16
        program.stack.push(int(program.op,16))

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
        program.direction = Direction.ALL[random.randint(0,len(Direction.ALL)-1)]

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
        a = str(program.stack.pop()) + ' '
        if program.show_steps:
            program.stdout_log += a
        else:
            sys.stdout.write(a)

    def op_print_chr(program):
        """Pop a and print as chr
        """
        a = chr(program.stack.pop())
        if program.show_steps:
            program.stdout_log += a
        else:
            sys.stdout.write(a)

    def op_trampoline(program):
        """Skip next cell
        """
        program.pc = program.text.get_next_pc(program.pc, program.direction)

    def op_put(program):
        """Pop y,x,v and put value v at position x,y
        """
        stack = program.stack
        y,x,v = stack.pop(), stack.pop(), stack.pop()
        program.text.put(y,x,v)

    def op_get(program):
        """Pop y,x and push ascii value of that char onto stack
        """
        stack = program.stack
        y,x = stack.pop(), stack.pop()
        v = program.text.get(x,y)
        if type(v) is str:
            stack.push(ord(v))
        else:
            stack.push(v)

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

    def op_not_implemented(program):
        """Raise error for non-implemented opcodes
        """
        raise OpCodeNotImplemented('%s,%s: %s' % (self.pc[0], self.pc[1], self.op))

    """Map operators to function handlers
    """
    op_map = {
        # Integers
        '0': op_push_int, '1': op_push_int, '2': op_push_int, '3': op_push_int,
        '4': op_push_int, '5': op_push_int, '6': op_push_int, '7': op_push_int,
        '8': op_push_int, '9': op_push_int, 'a': op_push_int, 'b': op_push_int,
        'b': op_push_int, 'c': op_push_int, 'd': op_push_int, 'e': op_push_int,
        'f': op_push_int,
        # Math
        '+': op_addition, '-': op_subtraction,
        '*': op_multiplication, '/': op_division, '%': op_modulo,
        # Logic
        '!': op_logical_not, '`': op_greater_than, 'w': op_not_implemented,
        # Movement
        '>': op_move_right, '<': op_move_left, '^': op_move_up, 'v': op_move_down,
        '?': op_move_random, '_': op_move_horizontal, '|': op_move_vertical,
        '[': op_not_implemented, ']': op_not_implemented,
        'h': op_not_implemented, 'l': op_not_implemented, 'm': op_not_implemented,
        # PC
        '#': op_trampoline, ';': op_not_implemented,
        'j': op_not_implemented,'k': op_not_implemented,
        # Stack
        ':': op_duplicate, '\\': op_swap, 
        '$': op_pop, 'n': op_not_implemented,
        'u': op_not_implemented,
        # I/O
        '.': op_print_int, ',': op_print_chr,
        '&': op_input_int, '~': op_input_chr,
        '=': op_not_implemented,
        'i': op_not_implemented, 'o': op_not_implemented,
        # Storage
        'p': op_put, 'g': op_get,
        's': op_not_implemented,
        # Misc
        '\'': op_not_implemented,
        '(': op_not_implemented, ')': op_not_implemented,
        '{': op_not_implemented, '}': op_not_implemented,
        '"': op_toggle_push_ascii,
        ' ': op_noop,
        'x': op_not_implemented,
        'y': op_not_implemented,
        'z': op_not_implemented,
        't': op_not_implemented,
        'r': op_not_implemented,
        'q': op_not_implemented, '@': op_exit
    }