import sys, random

from BefungeCommon import OpCodeNotImplemented
from BefungeCommon import Direction, BefungeMode

class BefungeOps(object):
  
    @staticmethod
    def pseudo_op_ascii_mode(program, thread):
        """Get int value of ascii char at current pc location
        """
        thread.stack.push(ord(program.text.get(*thread.pc)))

    def op_push_int(program, thread):
        """Push an integer onto the stack
        """
        # Get int value in base 16
        thread.stack.push(int(thread.op,16))
    
    def op_addition(program, thread):
        """Pop a,b then push a+b
        """
        stack = thread.stack
        stack.push(stack.pop() + stack.pop())
  
    def op_subtraction(program, thread):
        """Pop a,b then push b-a
        """
        stack = thread.stack
        a = stack.pop()
        b = stack.pop()
        stack.push(b - a)
      
    def op_division(program, thread):
        """Pop a,b then push b/a
        """
        stack = thread.stack
        a,b = stack.pop(), stack.pop()
        stack.push(b/a)
       
    def op_multiplication(program, thread):
        """Pop a,b then push a*b
        """
        stack = thread.stack
        stack.push(stack.pop() * stack.pop())
      
    def op_modulo(program, thread):
        """Pop a,b then push b%a
        """
        stack = thread.stack
        a,b = stack.pop(), stack.pop()
        stack.push(b%a)
      
    def op_logical_not(program, thread):
        """Pop a, if a==0 push 1, else push 0
        """
        stack = thread.stack
        a = stack.pop()
        if a == 0:
            stack.push(1)
        else:
            stack.push(0)
       
    def op_greater_than(program, thread):
        """Pop a,b, if b>a push 1, else push 0
        """
        stack = thread.stack
        a,b = stack.pop(), stack.pop()
        if b > a:
            stack.push(1)
        else:
            stack.push(0)
       
    def op_move_right(program, thread):
        """Change direction to right
        """
        thread.direction = Direction.RIGHT
     
    def op_move_left(program, thread):
        """Change direction to right
        """
        thread.direction = Direction.LEFT
     
    def op_move_up(program, thread):
        """Change direction to up
        """
        thread.direction = Direction.UP
      
    def op_move_down(program, thread):
        """Change direction to down
        """
        thread.direction = Direction.DOWN
       
    def op_move_random(program, thread):
        """Change direction to random
        """
        thread.direction = Direction.ALL[random.randint(0,len(Direction.ALL)-1)]
       
    def op_move_horizontal(program, thread):
        """Pop value, move right if 0, otherwise left
        """
        if thread.stack.pop() == 0:
            thread.direction = Direction.RIGHT
        else:
            thread.direction = Direction.LEFT
      
    def op_move_vertical(program, thread):
        """Pop value, move down if 0, otherwise up
        """
        if thread.stack.pop() == 0:
            thread.direction = Direction.DOWN
        else:
            thread.direction = Direction.UP

    def op_turn_left(program, thread):
        """Turn left on z-axis
        """
        thread.direction = Direction.TURN_LEFT[thread.direction]

    def op_turn_right(program, thread):
        """Turn right on z-axis
        """
        thread.direction = Direction.TURN_RIGHT[thread.direction]

    def op_move_turn(program, thread):
        """Pop a,b, if a<b then [ elif b>a then ] else nothing
        """
        stack = thread.stack
        b,a = stack.pop(), stack.pop()
        if a < b:
            BefungeOps.op_map['['](program, thread)
        elif b < a:
            BefungeOps.op_map[']'](program, thread)
        else:
            pass

    def op_toggle_push_ascii(program, thread):
        """Toggle program ascii mode
        """
        if thread.mode == BefungeMode.ASCII:
            thread.mode = BefungeMode.OP
        else:
            thread.mode = BefungeMode.ASCII
       
    def op_duplicate(program, thread):
        """Duplicate value on top of stack
        """
        thread.stack.push(thread.stack.peek())
      
    def op_swap(program, thread):
        """Swap two values on top of stack
        """
        stack = thread.stack
        a, b = stack.pop(), stack.pop()
        stack.push(a)
        stack.push(b)
      
    def op_pop(program, thread):
        """Pop value from stack
        """
        thread.stack.pop()

    def op_clear_stack(program, thread):
        """Clear all values from stack
        """
        thread.stack.clear()
       
    def op_print_int(program, thread):
        """Pop a and print as integer
        """
        a = str(thread.stack.pop()) + ' '
        if program.show_steps:
            program.stdout_log += a
        else:
            sys.stdout.write(a)
      
    def op_print_chr(program, thread):
        """Pop a and print as chr
        """
        a = chr(thread.stack.pop())
        if program.show_steps:
            program.stdout_log += a
        else:
            sys.stdout.write(a)
      
    def op_trampoline(program, thread):
        """Skip next cell
        """
        thread.pc = program.text.get_next_pc(thread.pc, thread.direction)
      
    def op_put(program, thread):
        """Pop y,x,v and put value v at position x,y
        """
        stack = thread.stack
        y,x,v = stack.pop(), stack.pop(), stack.pop()
        program.text.put(y,x,v)
      
    def op_get(program, thread):
        """Pop y,x and push ascii value of that char onto stack
        """
        stack = thread.stack
        y,x = stack.pop(), stack.pop()
        v = program.text.get(x,y)
        if type(v) is str:
            stack.push(ord(v))
        else:
            stack.push(v)
      
    def op_input_int(program, thread):
        """Ask user for integer input and push on stack
        """
        is_int = False
        while(not is_int):
            try:
                a = int(raw_input())
                is_int = True
            except ValueError:
                pass
        thread.stack.push(a)
    
    def op_input_chr(program, thread):
        """Ask user for a single char and push on stack
        """
        thread.stack.push(ord(raw_input()[0]))
     
    def op_noop(program, thread):
        """Do nothing
        """
        pass
         
    def op_split(program, thread):
        """Create andother thread with same PC but opposite direction
        """
        program.split(thread)

    def op_exit(program, thread):
        """Mark program as finished
        """
        thread.mode = BefungeMode.FINISHED
      
    def op_not_implemented(program, thread):
        """Raise error for non-implemented opcodes
        """
        raise OpCodeNotImplemented('%s,%s: %s' % (thread.pc[0], thread.pc[1], thread.op))

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
        '!': op_logical_not, '`': op_greater_than, 'm': op_not_implemented,
        # Movement
        '>': op_move_right, '<': op_move_left, '^': op_move_up, 'v': op_move_down,
        '[': op_turn_left, ']': op_turn_right, 'w': op_move_turn,
        'h': op_not_implemented, 'l': op_not_implemented,
        '_': op_move_horizontal, '|': op_move_vertical,
        '?': op_move_random,
        # PC
        '#': op_trampoline, ';': op_not_implemented,
        'j': op_not_implemented,'k': op_not_implemented,
        # Stack
        ':': op_duplicate, '\\': op_swap, 
        '$': op_pop, 'n': op_clear_stack,
        'u': op_not_implemented,
        # I/O
        '.': op_print_int, ',': op_print_chr,
        '&': op_input_int, '~': op_input_chr,
        '=': op_not_implemented,
        'i': op_not_implemented, 'o': op_not_implemented,
        # Storage
        'p': op_put, 'g': op_get,
        's': op_not_implemented,
        # Thread
        't': op_split, '@': op_exit,
        # Misc
        '\'': op_not_implemented,
        '(': op_not_implemented, ')': op_not_implemented,
        '{': op_not_implemented, '}': op_not_implemented,
        '"': op_toggle_push_ascii,
        ' ': op_noop,
        'x': op_not_implemented,
        'y': op_not_implemented,
        'z': op_not_implemented,
        'r': op_not_implemented,
        'q': op_not_implemented
    }