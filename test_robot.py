import unittest
from unittest.mock import patch
from io import StringIO
import sys
import robot


class MyTestRobot(unittest.TestCase):
    @patch('sys.stdin', StringIO('Bender\n'))
    def test_get_robot_name(self):
        output = robot.get_robot_name()
        self.assertEqual('Bender', output)


    @patch('sys.stdin', StringIO('\nBender\n'))
    def test_get_name_empty_then_valid(self):
        output = robot.get_robot_name()
        self.assertEqual('Bender', output)

    
    @patch('sys.stdin', StringIO('ForWard 10\n'))
    def test_get_command_camelcase(self):
        output = robot.get_command('Bender')
        self.assertEqual('forward 10', output)

    
    @patch('sys.stdin', StringIO('Jump\nreplay 5-2\n'))
    def test_get_command_invalid_then_valid(self):
        output = robot.get_command('Bender')
        self.assertEqual('replay 5-2', output)


    def test_split_command_forward(self):
        output = robot.split_command_input('forward 5')
        self.assertEqual(('forward', '5'), output)
    

    def test_split_command_left(self):
        output = robot.split_command_input('left')
        self.assertEqual(('left', ''), output)
    

    def test_valid_command_valid(self):
        output = robot.valid_command('forward 10')
        self.assertEqual(True, output)

    
    def test_valid_command_replay(self):
        output = robot.valid_command('replay 4')
        self.assertEqual(True, output)

    
    def test_valid_command_invalid(self):
        output = robot.valid_command('run 20')
        self.assertEqual(False, output)

    
    def test_valid_command_replay_range(self):
        output = robot.valid_command('replay 7-4')
        self.assertEqual(True, output)


    def test_valid_command_replay_range_invalid(self):
        output = robot.valid_command('replay f-c')
        self.assertEqual(False, output)    


    def test_is_int_invalid(self):
        output = robot.is_int('x')
        self.assertEqual(False, output)
    

    def test_is_int_valid(self):
        output = robot.is_int('17')
        self.assertEqual(True, output)

    
    def test_do_sprint(self):
        output = robot.do_sprint('Bender', 5)
        self.assertEqual((True, ' > Bender moved forward by 1 steps.'), output)


if __name__ == '__main__':
    unittest.main()