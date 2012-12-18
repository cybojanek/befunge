from nose.tools import *
from befunge.BefungeProgram import BefungeProgram
from befunge.BefungeCommon import Direction

def strip_program(a):
	# Remove leading and trailing newline
	a = a[1:-2]
	# Remove tabs
	a = a.replace('\t','')
	return a

def test_stack():
	a = strip_program("""
	12:$\\n
	""")
	program = BefungeProgram(text=a)
	stack_list = program.threads[0].stack.stack
	# 1,2
	program.step(2)
	assert stack_list == [1,2]
	# Duplicate
	program.step()
	assert stack_list == [1,2,2]
	# Pop
	program.step()
	assert stack_list == [1,2]
	# Swap
	program.step()
	assert stack_list == [2,1]
	# Clear
	# Note: on clear we lose referene to previous list
	program.step()
	assert program.threads[0].stack.stack == []

def test_ints():
	a = strip_program("""
	0123456789abcdef
	""")
	program = BefungeProgram(text=a)
	# Loop through all int values and check that they
	# were correctly pushed
	for x in range(16):
		program.step()
		stack = program.threads[0].stack
		assert len(stack) == x + 1
		assert stack.peek() == x

def test_math():
	a = strip_program("""
	43+6-7*3/b+6%
	""")
	program = BefungeProgram(text=a)
	stack = program.threads[0].stack
	# Addition
	program.step(3)
	assert len(stack) == 1
	assert stack.peek() == 4 + 3
	# Subtraction
	program.step(2)
	assert len(stack) == 1
	assert stack.peek() == 7 - 6
	# Multiplication
	program.step(2)
	assert len(stack) == 1
	assert stack.peek() == 7
	# Division
	program.step(2)
	assert len(stack) == 1
	assert stack.peek() == 7/3
	# Modulus
	program.step(4)
	assert len(stack) == 1
	assert stack.peek() == (2+11) % 6

def test_pc():
	a = strip_program("""
	# # # # 1;Whatever;2j789
	""")
	program = BefungeProgram(text=a)
	thread = program.threads[0]
	# Trampolines
	program.step(4)
	assert thread.pc == (8,0)
	# Jump_over
	program.step()
	assert thread.pc == (19,0)
	# Jump by two
	program.step(2)
	assert thread.pc == (23,0)

def test_logic():
	a = strip_program("""
	0!!5+!5-!
	""")
	program = BefungeProgram(text=a)
	stack = program.threads[0].stack
	# Not zero
	program.step(2)
	assert len(stack) == 1
	assert stack.peek() == 1
	# Not one
	program.step(1)
	assert len(stack) == 1
	assert stack.peek() == 0
	# Not five
	program.step(3)
	assert len(stack) == 1
	assert stack.peek() == 0
	# Not negative five
	program.step(3)
	assert len(stack) == 1
	assert stack.peek() == 0

def test_movement():
	# This is kind of a repeat of text_tests.test_next_pc
	# but it makes sure that it actually reads the arrows
	a = strip_program("""
	>v
	^<
	""")
	program = BefungeProgram(text=a)
	thread = program.threads[0]
	# Check >
	program.step()
	assert thread.pc == (1,0)
	assert thread.direction == Direction.RIGHT
	# Check v
	program.step()
	assert thread.pc == (1,1)
	assert thread.direction == Direction.DOWN
	# Check <
	program.step()
	assert thread.pc == (0,1)
	assert thread.direction == Direction.LEFT
	# Check v
	program.step()
	assert thread.pc == (0,0)
	assert thread.direction == Direction.UP

def test_movement_logic():
	a = strip_program("""
	>1#v_
	   _v
	    1
	    #
	    >|
	    |1
	""")
	program = BefungeProgram(text=a)
	thread = program.threads[0]
	# Check left _
	program.step(5)
	assert thread.pc == (3,1)
	# Check right _
	program.step(2)
	assert thread.pc == (4,2)
	# Check up |
	program.step(3)
	assert thread.pc == (4,4)
	# Check down |
	program.step(2)
	assert thread.pc == (5,5)

def test_movement_random():
	# Make two threaded random generators
	# and chek that their stacks contain 
	# at least a zero and one
	a = strip_program("""
	v
	#
	>   v
	t  0
	  1?<
	   ^
	 ^
	>?1
	 0
	""")
	program = BefungeProgram(text=a)
	# Small chance that we won't have a zero and one
	program.step(500)
	for stack in [thread.stack for thread in program.threads]:
		zero, one = False, False
		# Loop while we haven't found zero,one and we have stuff to pop
		while (not zero or not one) and len(stack)>0:
			rand = stack.pop()
			if rand == 0:
				zero = True
			elif rand == 1:
				one = True
		assert (zero,one) == (True,True)

def test_movement_turns():
	a = strip_program("""
	 ]  ]    10w
	[]  ][     0
	[    [     1
	           w 11w 1
	""")
	program = BefungeProgram(text=a)
	thread = program.threads[0]
	# > ] v
	program.step(2)
	assert thread.pc == (1,1)
	# v ] <
	program.step()
	assert thread.pc == (0,1)
	# < [ v
	program.step()
	assert thread.pc == (0,2)
	# v [ >
	program.step()
	assert thread.pc == (5,2)
	# > [ ^
	program.step()
	assert thread.pc == (5,1)
	# ^ [ <
	program.step()
	assert thread.pc == (4,1)
	# < ] ^
	program.step()
	assert thread.pc == (4,0)
	# ^ ] >
	program.step()
	assert thread.pc == (9,0)
	# 10w ]
	program.step(3)
	assert thread.pc == (11,1)
	# 01w [
	program.step(3)
	assert thread.pc == (13,3)
	# 11w
	program.step(3)
	assert thread.pc == (17,3)