import time

from BefungeStack import BefungeStack
from BefungeText import BefungeText
from BefungeCommon import Direction, Color, BefungeMode
from BefungeCommon import IllegalOpCodeException
from BefungeOps import BefungeOps


class BefungeThread(object):
    """Holds the state of a befunge thread
    Stack, pc, direction, op, mode

    """

    def __init__(self, pc, direction):
        self.stack = BefungeStack()
        self.pc = pc
        self.direction = direction
        self.op = ' '
        self.mode = BefungeMode.OP


class BefungeProgram(object):
    """Holds the state of a befunge program and runs it

    """
    def __init__(self, name=None, text=None, show_steps=False, operations_per_second=0):
        """Initialize text with file, empty stack and (0,0) pc

        Parameters:
        f - file
        show_steps - output program status, default=False
        operations_per_second - how many befunge ops a second, default=unlimited

        """
        self.threads = [BefungeThread((0, 0), Direction.RIGHT)]
        self.text = BefungeText(name, text)
        self.stdout_log = ''
        self.show_steps = show_steps
        self.operations_per_second = operations_per_second

    def step(self, steps=1):
        """Step through another iteration.
        Get pc value and tell handl_operator to run it

        """
        for step in range(steps):
            # Make duplicate in case we split
            # TODO: Is there a nicer way?
            for thread in self.threads[:]:
                thread.op = self.text.get(*thread.pc)
                # In op mode, so check opcode
                if thread.mode == BefungeMode.OP and not thread.op in BefungeOps.op_map:
                    raise IllegalOpCodeException('%s,%s: %s' % (self.pc[0], self.pc[1], self.op))
                elif thread.mode == BefungeMode.OP:
                    BefungeOps.op_map[thread.op](self, thread)
                # In ascii mode
                elif thread.mode == BefungeMode.ASCII:
                    # End ascii mode
                    if thread.op == '"':
                        BefungeOps.op_map['"'](self, thread)
                    # Read in with peusdo opcode
                    else:
                        BefungeOps.pseudo_op_ascii_mode(self, thread)
                thread.pc = self.text.get_next_pc(thread.pc, thread.direction)
                # Skip jump_overs with zero ticks
                # Handled here, so that next op is highlighted
                # instea of first ;
                while self.text.get(*thread.pc) == ';':
                    BefungeOps.op_map[';'](self, thread)
            # Clear out finished threads
            self.threads = [thread for thread in self.threads if not thread.mode == BefungeMode.FINISHED]

    def split(self, thread):
        """Create another thread with same PC but opposite direction

        """
        # Get opposite direction
        direction = Direction.OPPOSITE[thread.direction]
        # Get next position, otherwise child thread will be on 't' op again
        pc = self.text.get_next_pc(thread.pc, direction)
        # Prepend child
        self.threads.insert(0, BefungeThread(pc, direction))

    def run(self):
        """Step through program

        """
        while len(self.threads) > 0:
            if self.show_steps:
                self.show_program()
            if self.operations_per_second != 0:
                time.sleep(1.0 / self.operations_per_second)
            self.step()
        print("")

    def show_program(self):
        """Print terminal colored program status

        """
        # Divider
        print(Color.blue('#' * 80))
        # Code header
        print("%s" % Color.yellow_dark("Code:"))
        # Code
        # Rows with pcs
        pcs = {}
        for thread in self.threads:
            row = thread.pc[1]
            if row in pcs:
                pcs[row].append(thread.pc[0])
            else:
                pcs[row] = [thread.pc[0]]
        # Loop throw rows of code
        for i in range(len(self.text.text)):
            row = self.text.text[i]
            # This line contains our pc
            if i in pcs:
                # Make copy and replace pc with highlighted pc
                row = row[::]
                for pc in pcs[i]:
                    row[pc] = Color.grey_on_green(row[pc])
            print(''.join([str(x) for x in row]))
        # Stack
        for thread in self.threads:
            print("%s %s" % (Color.yellow_dark("Stack N:"), thread.stack))
            print("%s %r" % (Color.yellow_dark("Stack A:"), thread.stack))
        # Aggregated stdout
        print("%s %s" % (Color.yellow_dark("Stdout:"), self.stdout_log), end="")
        print("")
