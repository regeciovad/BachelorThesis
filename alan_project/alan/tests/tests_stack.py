# Advanced Error Recovery during Bottom-Up Parsing
# File: tests_stack.py
# Author: Dominika Regeciova, xregec00@stud.fit.vutbr.cz

from django.test import TestCase
from alan.stack import Stack


class StackMethodTests(TestCase):

    def test_stack_init(self):
        """
            Testing initialization of stack
        """
        stack = Stack()
        output = []
        stack_output = stack.get_stack()
        self.assertEqual(stack_output, output)

    def test_stack_empty(self):
        """
            Testing the stack is empty after initialization
        """
        stack = Stack()
        self.assertTrue(stack.is_empty())

    def test_stack_not_empty(self):
        """
            Testing the stack is not empty after push() and correction of push
        """
        stack = Stack()
        stack.push('42')
        output = ['42']
        stack_output = stack.get_stack()
        self.assertEqual(stack_output, output)
        self.assertFalse(stack.is_empty())

    def test_stack_more_push(self):
        """
            Testing correction of multiple push
        """
        stack = Stack()
        stack.push('42')
        stack.push('14')
        stack.push('1')
        output = ['42', '14', '1']
        stack_output = stack.get_stack()
        self.assertEqual(stack_output, output)
        self.assertFalse(stack.is_empty())

    def test_stack_one_push_one_pop(self):
        """
            Testing correction of pop and is_empty
        """
        stack = Stack()
        stack.push('42')
        output = '42'
        stack_output = stack.pop()
        self.assertEqual(stack_output, output)
        self.assertTrue(stack.is_empty())

    def test_stack_one_push_more_pop(self):
        """
            Testing correction of pop with empty stack
        """
        stack = Stack()
        stack.push('42')
        output = '42'
        stack_output = stack.pop()
        self.assertEqual(stack_output, output)
        self.assertTrue(stack.is_empty())
        output = None
        stack_output = stack.pop()
        self.assertEqual(stack_output, output)
        self.assertTrue(stack.is_empty())

    def test_get_topmost_empty(self):
        """
            Testing correction of get_topmost with empty stack
        """
        stack = Stack()
        output = None
        stack_output = stack.get_topmost()
        self.assertEqual(stack_output, output)
        self.assertTrue(stack.is_empty())

    def test_get_topmost_one(self):
        """
            Testing correction of get_topmost with one item on the stack
        """
        stack = Stack()
        stack.push('42')
        output = '42'
        stack_output = stack.get_topmost()
        self.assertEqual(stack_output, output)
        self.assertFalse(stack.is_empty())

    def test_get_topmost_more(self):
        """
            Testing correction of get_topmost with more items on the stack
        """
        stack = Stack()
        stack.push('42')
        stack.push('14')
        stack.push('1')
        output = '1'
        stack_output = stack.get_topmost()
        self.assertEqual(stack_output, output)
        self.assertFalse(stack.is_empty())
        output = ['42', '14', '1']
        stack_output = stack.get_stack()
        self.assertEqual(stack_output, output)
