import unittest
from io import StringIO
from unittest.mock import patch
from hypothesis import strategies as st, given
import math

from gradelang.walk import *
from gradelang.interpreter import interpret


class Test(unittest.TestCase):

    @given(st.integers())
    def test_input(self, x):
        with patch('builtins.input', return_value=x):
            interpret(f'input "Enter a value for variable x: ", x')
        self.assertEqual(state.symbol_table['x'], x)
    
    @patch('sys.stdout', new_callable=StringIO)
    @given(st.integers())
    def test_io(self, stdout, x):
        stdout.seek(0)
        stdout.truncate()
        with patch('builtins.input', return_value=x):
            interpret(
                """
                input "Enter a value for variable x: ", x
                print "The value of variable x is ", x
                """ 
            )
        self.assertEqual(stdout.getvalue().strip(), f'The value of variable x is {x}'.strip())
        stdout.seek(0)
        stdout.truncate()

    @patch('sys.stdout', new_callable=StringIO)
    @given(st.integers())
    def test_if(self, stdout, x):
        stdout.seek(0)
        stdout.truncate()
        with patch('builtins.input', return_value=x):
            interpret(
                """
                input "enter a value: ", a
                if a==5 then
                    print "a is equal to 5"
                else
                    print "a is not equal to 5"
                endif
                """
            )
        self.assertEqual(
            stdout.getvalue().strip(),
            f'a is {"equal" if (x == 5) else "not equal"} to 5',
            f'x = {x}'
        )
        stdout.seek(0)
        stdout.truncate()

    @patch('sys.stdout', new_callable=StringIO)
    def test_while(self, stdout):
        stdout.seek(0)
        stdout.truncate(0)
        interpret(
            """
            a = 1
            while a <= 100
                print a
                a = a + 1
            endwhile
            """
        )
        self.assertEqual(
            stdout.getvalue().strip(),
            '\n'.join([str(x) for x in range(1, 100 + 1)])
        )
        stdout.seek(0)
        stdout.truncate()

    @patch('sys.stdout', new_callable=StringIO)
    def test_for_no_step(self, stdout):
        stdout.seek(0)
        stdout.truncate()
        interpret(
            """
            ' print a list of integers from 1 through 10
            for x = 1 to 10
                print x
            next x
            """
        )
        self.assertEqual(stdout.getvalue().strip(), '\n'.join([str(x) for x in range(1, 10 + 1)]))
        stdout.seek(0)
        stdout.truncate()

    @patch('sys.stdout', new_callable=StringIO)
    def test_for_pos_step(self, stdout):
        stdout.seek(0)
        stdout.truncate()
        interpret(
            """
            ' print a list of integers from 1 through 10
            for x = 1 to 10 step 2
                print x
            next x
            """
        )
        self.assertEqual(stdout.getvalue().strip(), '\n'.join([str(x) for x in range(1, 10 + 1, 2)]))
        stdout.seek(0)
        stdout.truncate(0)

    @patch('sys.stdout', new_callable=StringIO)
    def test_for_neg_step(self, stdout):
        stdout.seek(0)
        stdout.truncate()
        interpret(
            """
            ' print a list of integers from 1 through 10
            for x = 9 to 1 step -2
                print x
            next x
            """
        )
        self.assertEqual(stdout.getvalue().strip(), '\n'.join([str(x) for x in range(9, 1, -2)]))
        stdout.seek(0)
        stdout.truncate()

    @patch('sys.stdout', new_callable=StringIO)
    @given(st.integers(min_value=-10, max_value=10))
    def test_factorial(self, stdout, x):
        stdout.seek(0)
        stdout.truncate()
        with patch('builtins.input', return_value=x):
            interpret(
                """
                ' compute the factorial of a number
                input "Enter a value: ", x
                if x <= 0 then
                    print "illegal input value"
                    end
                endif
                
                ' input ok - continue computation
                y = 1
                for i = 1 to x
                    y = y * i
                next i
                print "The factorial of ",x," is ",y
                """
            )
        self.assertEqual(
            stdout.getvalue().strip(), 
            f'The factorial of {x} is {math.factorial(x)}' if x > 0 else 'illegal input value'
            )
        stdout.seek(0)
        stdout.truncate()


    @patch('sys.stdout', new_callable=StringIO)
    @given(st.integers(), st.integers())
    def test_logical(self, stdout, x, y):
        stdout.seek(0)
        stdout.truncate()
        with patch('builtins.input', side_effect=[x, y]):
            interpret(
                """
                input x
                input y
                z = x & y
                print z
                z = x | y
                print z
                z = !x
                print z
                """
            )
        self.assertEqual(
            stdout.getvalue().strip(),
            '\n'.join([str(int(bool(x) and bool(y))), str(int(bool(x) or bool(y))), str(int(not x))])
        )
