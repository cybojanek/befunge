class BefungeStack(object):
    """Simulates a stack

    """

    def __init__(self):
        self.clear()

    def push(self,a):
        """Push a value onto the stack

        """
        self.stack.append(a)

    def pop(self):
        """Pop a value from the stack
        Return 0 on empty stack

        """
        if(len(self.stack) > 0):
            return self.stack.pop()
        else:
            return 0

    def peek(self):
        """Return a value form the stack
        Return 0 on empty stack

        """
        if(len(self.stack) > 0):
            return self.stack[-1]
        else:
            return 0 

    def clear(self):
        """Clear contents of stack

        """
        self.stack = []

    def __len__(self):
        return len(self.stack)

    def __str__(self):
        """Comma seperated values

        """
        return ','.join([str(x) for x in self.stack])

    def __repr__(self):
        """Comma seperated values: ASCII if visible

        """
        return ','.join([repr(chr(x)) if x<=255 and x>=0 else str(x) for x in self.stack])
