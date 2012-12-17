from nose.tools import *
from befunge.BefungeStack import BefungeStack

def test_push():
	stack = BefungeStack()
	stack.push(1)
	stack.push(2)
	assert len(stack) == 2
	assert stack.stack[0] == 1
	assert stack.stack[1] == 2

def test_pop():
	stack = BefungeStack()
	stack.push(1)
	assert stack.pop() == 1
	assert stack.pop() == 0

def test_peek():
	stack = BefungeStack()
	stack.push(1)
	assert stack.peek() == 1
	assert stack.peek() == 1
	assert len(stack) == 1

def test_clear():
	stack = BefungeStack()
	stack.push(1)
	assert len(stack) == 1
	stack.clear()
	assert len(stack) == 0