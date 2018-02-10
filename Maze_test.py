'''
Created on Dec 10, 2017

@author: gotto
'''
import unittest
from solver_package import Maze

class MazeValidityTestCase(unittest.TestCase):
    
    standard_matrix_4x4 = [
        [-1,0,0,1],
        [1,1,0,1],
        [1,1,0,1],
        [1,0,0,-2]
    ]
    
    matrix_with_2_endpoint_4x4 = [
        [-1,0,0,1],
        [1,1,0,1],
        [1,0,0,1],
        [1,0,-2,-2]
    ]
    
    matrix_contains_invalid_fields_4x4 = [
        [-1,0,-5,1],
        [1,1,0,1],
        [1,6,0,1],
        [1,0,0,-2]
    ]
    
    matrix_with_2_startpoint_4x4 = [
        [-1,0,0,1],
        [1,1,0,1],
        [1,-1,0,1],
        [1,0,0,-2]
    ]
     

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_invalid_maze(self):
        invalid_maze = Maze.Maze(self.matrix_contains_invalid_fields_4x4)
        self.assertEqual(invalid_maze.validity, Maze.Validity.INVALID, "Maze must be invalid")
        
    def test_check_invalid_maze(self):
        invalid_maze = Maze.Maze(self.matrix_contains_invalid_fields_4x4)
        invalid_maze.validity = Maze.Validity.UNKNOWN
        self.assertEqual(invalid_maze.check_matrix(), Maze.Validity.INVALID, "Maze must be invalid")
        
    def test_invalid_2startpoint_maze(self):
        invalid_maze_2startpoint = Maze.Maze(self.matrix_with_2_startpoint_4x4)
        self.assertEqual(invalid_maze_2startpoint.validity, Maze.Validity.INVALID, "Maze must be invalid")
        
    def test_valid_maze(self):
        valid_maze = Maze.Maze(self.standard_matrix_4x4)
        self.assertEqual(valid_maze.validity, Maze.Validity.VALID, "Maze must be valid")
        
    def test_check_valid_maze(self):
        valid_maze = Maze.Maze(self.standard_matrix_4x4)
        valid_maze.validity = Maze.Validity.UNKNOWN
        self.assertEqual(valid_maze.check_matrix(), Maze.Validity.VALID, "Maze must be valid")
        
    def test_valid_2endpoint_maze(self):
        invalid_maze_2startpoint = Maze.Maze(self.matrix_with_2_endpoint_4x4)
        self.assertEqual(invalid_maze_2startpoint.validity, Maze.Validity.VALID, "Maze must be valid")
        
class MazeGetPointsTestCase(unittest.TestCase):
    
    standard_matrix_start_and_finsih_in_corners_5x5 = [
        [-1,0,0,0,1],
        [1,1,0,0,1],
        [1,1,0,0,1],
        [1,1,0,0,1],
        [1,0,1,0,-2]
    ]
    
    standard_matrix_start_and_finish_in_middle_5x5 = [
        [0,0,0,0,1],
        [1,1,-1,0,1],
        [1,1,0,-2,1],
        [1,1,0,0,1],
        [1,0,1,0,1]
    ]
    
    matrix_with_2_endpoint_5x5 = [
        [-1,0,0,1,1],
        [1,1,0,0,1],
        [1,-2,0,0,1],
        [1,1,0,0,1],
        [1,0,0,-2,1]
    ]
     

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_start_point_1(self):
        maze = Maze.Maze(self.standard_matrix_start_and_finsih_in_corners_5x5)
        start_point = maze.get_start_point()
        self.assertEqual(start_point, (0,0), "Start point should be (0,0) instead of " + str(start_point))
        
    def test_start_point_2(self):
        maze = Maze.Maze(self.standard_matrix_start_and_finish_in_middle_5x5)
        start_point = maze.get_start_point()
        self.assertEqual(start_point, (1,2), "Start point should be (0,0) instead of " + str(start_point))
        
    def test_end_point_1(self):
        maze = Maze.Maze(self.standard_matrix_start_and_finsih_in_corners_5x5)
        end_point = maze.get_end_points()
        self.assertEqual(end_point, [(4,4)], "Finish point should be (4,4) instead of " + str(end_point))
        
    def test_end_point_2(self):
        maze = Maze.Maze(self.standard_matrix_start_and_finish_in_middle_5x5)
        end_point = maze.get_end_points()
        self.assertEqual(end_point, [(2,3)], "Finish point should be (2,3) instead of " + str(end_point))
        
    def test_multiply_end_point_1(self):
        maze = Maze.Maze(self.matrix_with_2_endpoint_5x5)
        end_point = maze.get_end_points()
        self.assertEqual(end_point, [(2,1),(4,3)], "Finish points should be [(2,1),(4,3)] instead of " + str(end_point))
    
    def test_get_inner_fields(self):
        maze = Maze.Maze(self.standard_matrix_start_and_finsih_in_corners_5x5)
        fields = [
            [0,0],
            [0,1],
            [1,0],
            [4,4],
        ]
        expected_result = [-1,0,1,-2]
        result = [maze.get_field(x) for x in fields]
        self.assertEqual(result,expected_result,
            "Some fields not match\n" +
            "expected: " + str(expected_result) + "\n" +
            "get: " + str(result))

    def test_get_fields_outside_the_area(self):
        maze = Maze.Maze(self.standard_matrix_start_and_finsih_in_corners_5x5)
        fields = [
            [ 0, 5],
            [ 5, 0],
            [-1, 0],
            [ 2,-2],
        ]
        expected_result = [1,1,1,1]
        result = [maze.get_field(x) for x in fields]
        self.assertEqual(result,expected_result,
            "Some fields not match\n" +
            "expected: " + str(expected_result) + "\n" +
            "get: " + str(result))

    
if __name__ == "__main__":
    unittest.main()