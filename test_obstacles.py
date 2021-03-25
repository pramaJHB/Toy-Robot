import unittest
import random
from maze import obstacles


class MyTestWorld(unittest.TestCase):
    def test_get_obstacles(self):
        obstacles.random.randint = lambda a, b: 2
        output = obstacles.get_obstacles()
        self.assertEqual([(2, 2), (2, 2)], output)


    def test_obstacle_at_destination(self):
        obstacles.obstacles_list = [(100, 100), (-50, 50), (200, -200), (-300, -300)]
        output = obstacles.is_position_blocked(202, -197)
        self.assertEqual(True, output)

    
    def test_no_obstacle_at_destination(self):
        obstacles.obstacles_list = [(100, 100), (-50, 50), (200, -200), (-300, -300)]
        output = obstacles.is_position_blocked(10, 10)
        self.assertEqual(False, output)


    def test_obstacle_in_path_x(self):
        obstacles.obstacles_list = [(100, 100), (-50, 50), (200, -200), (-300, -300)]
        output = obstacles.is_path_blocked(102, 0, 102, 150)
        self.assertEqual(True, output)
    

    def test_obstacle_in_path_y(self):
        obstacles.obstacles_list = [(100, 100), (-50, 50), (200, -200), (-300, -300)]
        output = obstacles.is_path_blocked(100, -198, 250, -198)
        self.assertEqual(True, output)
    

    def test_no_obstacle_in_path_x(self):
        obstacles.obstacles_list = [(100, 100), (-50, 50), (200, -200), (-300, -300)]
        output = obstacles.is_path_blocked(10, 10, 10, 20)
        self.assertEqual(False, output)


    def test_no_obstacle_in_path_y(self):
        obstacles.obstacles_list = [(100, 100), (-50, 50), (200, -200), (-300, -300)]
        output = obstacles.is_path_blocked(0, 25, 25, 25)
        self.assertEqual(False, output)


if __name__ == '__main__':
    unittest.main()