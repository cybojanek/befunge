from nose.tools import *
from befunge.BefungeText import BefungeText
from befunge.BefungeCommon import Direction

def strip_program(a):
	# Remove leading and trailing newline
	a = a[1:-2]
	# Remove tabs
	a = a.replace('\t','')
	return a

def test_get():
	# Declare program
	a = strip_program("""
	ABC
	DEF
	""")
	program = BefungeText(text=a)

	assert program._number_of_rows() == 2
	# Get regular values
	assert program.get(0,0) == 'A'
	assert program.get(2,0) == 'C'
	# Check beyond row length
	assert program.get(4,0) == ' '
	# Check beyond row count
	assert program.get(0,3) == ' '
	assert program.get(3,3) == ' '
	# Check that no rows were added by out of bounds requests
	assert program._number_of_rows() == 2

def test_put():
	# Declare program
	a = strip_program("""
	ABC
	""")
	program = BefungeText(text=a)

	assert program._number_of_rows() == 1
	# Get, change, check
	program.put(1,0,'X')
	assert program.get(1,0) == 'X'
	# Put beyond row length
	program.put(4,0,'Z')
	# Check for padding and value
	assert program.get(3,0) == ' '
	assert program.get(4,0) == 'Z'
	# Put beyond row count
	program.put(1,3,'Z')
	assert program.get(1,3) == 'Z'
	assert program.get(0,3) == ' '
	assert program._number_of_rows() == 4

def test_next_pc():
	# Arrows don't actually do much.
	# They're just for clarity
	# Declare program
	a = strip_program("""
	> >
	< <
	""")

	program = BefungeText(text=a)

	# Check regular move right
	assert program.get_next_pc((0,0), Direction.RIGHT) == (1,0)
	# Check right wrap around
	assert program.get_next_pc((2,0), Direction.RIGHT) == (0,0)
	# Check regular move left
	assert program.get_next_pc((1,0), Direction.LEFT) == (0,0)
	# Check left wrap around
	assert program.get_next_pc((0,0), Direction.LEFT) == (2,0)

	b = strip_program("""
	^v

	  @
	^v
	""")
	program = BefungeText(text=b)
	# Check regular move up
	assert program.get_next_pc((0,3), Direction.UP) == (0,2)
	# Check skip up
	assert program.get_next_pc((0,2), Direction.UP) == (0,0)
	# Check up wrap around
	assert program.get_next_pc((0,0), Direction.UP) == (0,3)
	# Chek skip down
	assert program.get_next_pc((1,0), Direction.DOWN) == (1,2)
	# Check regular move down
	assert program.get_next_pc((1,2), Direction.DOWN) == (1,3)
	# Check down wrap around
	assert program.get_next_pc((1,3), Direction.DOWN) == (1,0)




