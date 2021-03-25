import unittest
from io import StringIO
import sys
import robot
from world.text import world


class MyTestWorld(unittest.TestCase):
    def test_position_allowed_valid(self):
        output = world.is_position_allowed(75, 50)
        self.assertEqual(True, output)


    def test_position_allowed_out_of_safezone(self):
        output = world.is_position_allowed(50, 425)
        self.assertEqual(False, output)
    

    def test_update_position_valid(self):
        world.position_x = 50
        world.position_y = 25
        world.current_direction_index = 0
        output = world.update_position(10)
        self.assertEqual(True, output)


    def test_update_position_out_of_safezone(self):
        world.position_x = 50
        world.position_y = 25
        world.current_direction_index = 0
        output = world.update_position(400)
        self.assertEqual(False, output)


    def test_forward_normal(self):
        output = world.do_forward('Bender', 17)
        self.assertEqual((True, ' > Bender moved forward by 17 steps.'), output)

    
    def test_forward_out_safezone(self):
        output = world.do_forward('Bender', 500)
        self.assertEqual((True, 'Bender: Sorry, I cannot go outside my safe zone.'), output)


    def test_back_normal(self):
        output = world.do_back('Bender', 42)
        self.assertEqual((True, ' > Bender moved back by 42 steps.'), output)

    
    def test_back_out_safezone(self):
        output = world.do_back('Bender', 12345)
        self.assertEqual((True, 'Bender: Sorry, I cannot go outside my safe zone.'), output)


    def test_turn_right(self):
        output = world.do_right_turn('Awesom-O')
        self.assertEqual((True, ' > Awesom-O turned right.'), output)

    
    def test_turn_left(self):
        output = world.do_left_turn('Awesom-O')
        self.assertEqual((True, ' > Awesom-O turned left.'), output)


    def test_is_position_allowed_true(self):
        ouput = world.is_position_allowed(10, 10)
        self.assertEqual(True, ouput)

    
    def test_is_position_allowed_outside(self):
        output = world.is_position_allowed(501, 0)
        self.assertEqual(False, output)
    

    def test_mazerun(self):
        world.reset_globals()
        output = world.do_mazerun('Bender', '')
        self.assertEqual((True, 'Bender: I am at the top edge.'), output)


    def test_mazerun(self):
        world.reset_globals()
        output = world.do_mazerun('Bender', 'top')
        self.assertEqual((True, 'Bender: I am at the top edge.'), output)

    
    def test_mazerun_bottom(self):
        world.reset_globals()
        output = world.do_mazerun('Bender', 'bottom')
        self.assertEqual((True, 'Bender: I am at the bottom edge.'), output)
    

    def test_mazerun_left(self):
        world.reset_globals()
        output = world.do_mazerun('Bender', 'left')
        self.assertEqual((True, 'Bender: I am at the left edge.'), output)
    

    def test_mazerun_right(self):
        world.reset_globals()
        output = world.do_mazerun('Bender', 'right')
        self.assertEqual((True, 'Bender: I am at the right edge.'), output)


if __name__ == '__main__':
    unittest.main()