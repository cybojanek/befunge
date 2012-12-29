from BefungeCommon import Direction


class BefungeText(object):
    """Holds contents of befunge program.

    """

    def __init__(self, name=None, text=None):
        """Load the program from a file

        Parameters:
        name - file name of program
        text - program string with newlines

        """
        self.text = []
        self._load_program(name, text)

    def _load_program(self, name=None, text=None):
        """Load the contents of file row by row
        Strip whitespace from right side

        Parameters:
        name - file name of program
        text - program string with newlines

        """
        if not name == None:
            for x in open(name, 'r'):
                self.text.append(list(x.rstrip()))
        elif not text == None:
            for x in text.split('\n'):
                self.text.append(list(x.rstrip()))

    def _number_of_rows(self):
        """Return the number of rows in the program

        """
        return len(self.text)

    def _length_of_row(self, y):
        """Return the length of the given row

        Parameters:
        y - row number

        """
        return len(self.text[y])

    def _add_row(self, value=None):
        """Add a row to the program
        If value not specified, then empty row added

        Parameters:
        value = list of characters

        """
        if value == None:
            self.text.append([])
        else:
            self.text.append(value)

    def get(self, x, y):
        """Implement 'g' command and get field

        """
        if(y >= self._number_of_rows() or x >= self._length_of_row(y)):
            return ' '
        else:
            return self.text[y][x]

    def put(self, x, y, z):
        """Implment 'p' command and alter text
        If x and/or y are beyond current program bounds
        add empty rows and whitespace

        Parameters:
        x - column number
        y - row number
        z - value

        """
        # If its a visible char, then convert it to that
        if z > 31 and z < 127:
            z = chr(z)
        # If the put value is beyond our current amount of rows
        if(y >= self._number_of_rows()):
            # Add dummy empty rows until row
            for r in xrange(self._number_of_rows(), y):
                self._add_row()
            # Add row, left padded with whitespace
            self._add_row(list("%s" % (" " * (x))) + [z])
        # Else if y is past the current row length
        elif(x >= self._length_of_row(y)):
            # Append whitespace and value
            self.text[y] = self.text[y] + list("%s" % (" " * (x - self._length_of_row(y)))) + [z]
        # Otherwise modify whats currently there
        else:
            self.text[y][x] = z

    def get_next_pc(self, pc, direction, skip=True):
        """Get the next pc based on direction
        Wrap around in x,y directions
        Skip whitesapce by default

        """
        op = ' '
        x, y = pc
        # For befunge98, we skip all whitespace with zero ticks
        while op == ' ':
            # If left or right, just mod with current row length
            if direction == Direction.RIGHT:
                x, y = ((x + 1) % self._length_of_row(y), y)
            # Negative values work the way we want :-)
            elif direction == Direction.LEFT:
                x, y = ((x - 1) % self._length_of_row(y), y)
            elif direction == Direction.DOWN:
                x, y = (x, (y + 1) % self._number_of_rows())
            elif direction == Direction.UP:
                x, y = (x, (y - 1) % self._number_of_rows())
            op = self.get(x, y)
            # Don't skip whitespace
            if not skip:
                break
            #print "%s,%s,%s,%s" % (op, pc, direction, op == ' ')
        return (x, y)

    def jump(self, pc, direction, j):
        """Jump over that many cells

        """
        x, y = pc
        if direction == Direction.RIGHT:
            return ((x + j) % self._length_of_row(y), y)
        elif direction == Direction.LEFT:
            return ((x - j) % self._length_of_row(y), y)
        elif direction == Direction.DOWN:
            return (x, (y + j) % self._number_of_rows())
        elif direction == Direction.UP:
            return (x, (y - j) % self._number_of_rows())

    def __str__(self):
        ret = ''
        for row in self.text:
            ret += '%s\n' % (''.join([str(x) for x in row]))
        return ret
