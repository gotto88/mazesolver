'''
Created on Dec 12, 2017

@author: gotto
'''
import unittest
from solver_package import Maze, MazeWalker

class WalkerStartTest(unittest.TestCase):

    matrix1 = [
        [-1,0,0,0,1],
        [1,1,0,0,1],
        [1,1,0,0,1],
        [1,1,0,0,1],
        [1,0,1,0,-2]
    ]
    
    matrix_invalid = [
        [-1,0,0,0,1],
        [1,-1,0,0,1],
        [1,1,0,0,1],
        [1,1,0,0,1],
        [1,0,1,0,-2]
    ]
    
    def setUp(self):
        self.maze1 = Maze.Maze(WalkerStartTest.matrix1)
        self.maze_invalid = Maze.Maze(WalkerStartTest.matrix_invalid)
        self.config1 = MazeWalker.WalkerConfiguration(mode=MazeWalker.WalkMode.TOTTALY_RANDOM,max_num_of_try=100,max_num_of_restart=2)

    def tearDown(self):
        pass

    def test_start_ok(self):
        walker = MazeWalker.MazeWalker(maze=self.maze1, config=self.config1)
        s = walker.starting()
        self.assertEqual(s, (True, "Walker started"), "Walker not started properly!")
    
    def test_start_fails_no_maze_set(self):
        walker = MazeWalker.MazeWalker(config=self.config1)
        s = walker.starting()
        self.assertEqual(s, (False, "Maze not set!"), "Walker should not be started!")
        
    def test_start_fails_invalid_maze_set(self):
        walker = MazeWalker.MazeWalker(maze=self.maze_invalid, config=self.config1)
        s = walker.starting()
        self.assertEqual(s, (False, "Maze not set!"), "Walker should not be started!")
        
    def test_start_param_checks(self):
        walker = MazeWalker.MazeWalker(maze=self.maze1, config=self.config1)
        start_point = [0,0]
        s = walker.starting()
        self.assertEqual(s, (True, "Walker started"), "Walker not started properly!")
        self.assertEqual(walker.startpoint,start_point, 
                         " Start point should be " + str(start_point) +
                         " instead of " + str(walker.startpoint))
        self.assertEqual(walker.current_position,start_point, 
                         " Current position should be " + str(start_point) +
                         " instead of " + str(walker.startpoint))

class WalkerMovingTest(unittest.TestCase):
    
    matrix1 = [
        [-1,0,0,0,1],
        [1,0,1,0,1],
        [1,1,0,0,1],
        [1,1,0,0,1],
        [1,0,1,0,-2]
    ]

    def setUp(self):
        self.maze1 = Maze.Maze(WalkerMovingTest.matrix1)
        self.config1 = MazeWalker.WalkerConfiguration(mode=MazeWalker.WalkMode.TOTTALY_RANDOM,max_num_of_try=100,max_num_of_restart=2)

    def tearDown(self):
        pass

    def test_next_points(self):
        walker = MazeWalker.MazeWalker(maze=self.maze1, config=self.config1)
        walker.starting()
        walker.current_position = [2,2]
        directions = [0,1,2,3]
        next_points = [walker.next_point(x) for x in directions]
        expected = [[1,2],[2,3],[3,2],[2,1]]
        self.assertEqual(next_points, expected, 
                         "Next points should be " + str(expected) +
                         "Instead of " + str(next_points))
    
    def test_inverse_direction(self):
        walker = MazeWalker.MazeWalker(maze=self.maze1, config=self.config1)
        directions = [0,1,2,3]
        inv_directios = [walker.inverse_direction(x) for x in directions]
        expected = [2,3,0,1]
        self.assertEqual(inv_directios, expected, 
                         "Next points should be " + str(expected) +
                         "Instead of " + str(inv_directios))
    
    def test_move_forward_right_check_params(self):
        walker = MazeWalker.MazeWalker(maze=self.maze1, config=self.config1)
        walker.starting()
        walker.move_forward(1)
        result = [walker.current_position,walker.road,walker.last_try,walker.first_try_from_here,walker.num_of_try_from_here]
        expected = [[0,1],[-1,1],1,[1,-1],[1,0]]
        self.assertEqual(result,expected,
                         "Params should be " + str(expected) +
                         "Instead of " + str(result))
        
    def test_move_forward_right_then_back(self):
        walker = MazeWalker.MazeWalker(maze=self.maze1, config=self.config1)
        walker.starting()
        walker.move_forward(1)
        walker.step_back()
        result = [walker.current_position,walker.road,walker.last_try,walker.first_try_from_here,walker.num_of_try_from_here]
        expected = [[0,0],[-1],1,[1],[1]]
        self.assertEqual(result,expected,
                         "Params should be " + str(expected) +
                         "Instead of " + str(result))
        
    def test_move_forward_right_then_stay(self):
        walker = MazeWalker.MazeWalker(maze=self.maze1, config=self.config1)
        walker.starting()
        walker.move_forward(1)
        walker.stay(2)
        result = [walker.current_position,walker.road,walker.last_try,walker.first_try_from_here,walker.num_of_try_from_here]
        expected = [[0,1],[-1,1],2,[1,2],[1,1]]
        self.assertEqual(result,expected,
                         "Params should be " + str(expected) +
                         "Instead of " + str(result))
        
    def test_move_to_finish(self):
        walker = MazeWalker.MazeWalker(maze=self.maze1, config=self.config1)
        walker.starting()
        directions = [1,1,1,2,2,3,2,1,2,1]
        [walker.move_forward(d) for d in directions]
        result = [walker.current_position,walker.road,walker.last_try,walker.first_try_from_here,walker.num_of_try_from_here]
        expected = [[4,4],[-1,1,1,1,2,2,3,2,1,2,1],1,[1,1,1,2,2,3,2,1,2,1,-1],[1,1,1,1,1,1,1,1,1,1,0]]
        self.assertEqual(result,expected,
                         "Params should be " + str(expected) +
                         "Instead of " + str(result))
    
    def test_move_to_finish_with_try_direction(self):
        walker = MazeWalker.MazeWalker(maze=self.maze1, config=self.config1)
        walker.starting()
        directions = [1,1,1,2,2,3,2,1,2,1]
        [walker.try_direction(d) for d in directions]
        result = [walker.current_position,walker.road,walker.last_try,walker.first_try_from_here,walker.num_of_try_from_here]
        expected = [[4,4],[-1,1,1,1,2,2,3,2,1,2,1],1,[1,1,1,2,2,3,2,1,2,1,-1],[1,1,1,1,1,1,1,1,1,1,0]]
        self.assertEqual(result,expected,
                         "Params should be " + str(expected) +
                         "Instead of " + str(result))
      
    def test_move_to_finish_with_try_direction_with_stay(self):
        walker = MazeWalker.MazeWalker(maze=self.maze1, config=self.config1)
        walker.starting()
        directions = [1,1,1,1,2,3,1,2,3,2,1,2,1]
        [walker.try_direction(d) for d in directions]
        result = [walker.current_position,walker.road,walker.last_try,walker.first_try_from_here,walker.num_of_try_from_here]
        expected = [[4,4],[-1,1,1,1,2,2,3,2,1,2,1],1,[1,1,1,1,3,3,2,1,2,1,-1],[1,1,1,2,3,1,1,1,1,1,0]]
        self.assertEqual(result,expected,
                         "Params should be " + str(expected) +
                         "Instead of " + str(result))

class WalkerSolutionTest(unittest.TestCase):

    matrix1 = [
        [-1,0,0,0,1],
        [1,0,1,0,1],
        [1,1,0,0,1],
        [1,1,0,0,1],
        [1,0,1,0,-2]
    ]
    
    matrix_with_circle = [
        [-1,0,0,0,1],
        [1,0,1,0,1],
        [1,0,0,0,1],
        [1,1,0,0,1],
        [1,0,1,0,-2]
    ]
    
    matrix_unsolvable = [
        [-1,0,0,0,1],
        [1,0,1,0,1],
        [1,1,0,0,1],
        [1,1,0,1,1],
        [1,0,1,0,-2]
    ]
    
    matrix_unsolvable_with_circle = [
        [-1,0,0,0,1],
        [1,0,1,0,1],
        [1,0,0,0,1],
        [1,1,0,1,1],
        [1,0,1,0,-2]
    ]

    def setUp(self):
        self.maze1 = Maze.Maze(WalkerSolutionTest.matrix1)
        self.maze_with_circle = Maze.Maze(WalkerSolutionTest.matrix_with_circle)
        self.maze_unsolvable = Maze.Maze(WalkerSolutionTest.matrix_unsolvable)
        self.maze_unsolvable_with_circle = Maze.Maze(WalkerSolutionTest.matrix_unsolvable_with_circle)
        
        self.config_rand1 = MazeWalker.WalkerConfiguration(mode=MazeWalker.WalkMode.TOTTALY_RANDOM, \
                                                           max_num_of_try=1000,\
                                                           max_num_of_restart=0 \
                                                           )
        self.config_rand_no_retry = MazeWalker.WalkerConfiguration(mode=MazeWalker.WalkMode.RANDOM_DEPT_WALK_NO_RETRY, \
                                                                   max_num_of_try=1000, \
                                                                   max_num_of_restart=0 \
                                                                   )
        self.config_deterministic = MazeWalker.WalkerConfiguration(mode=MazeWalker.WalkMode.DETERMINISTIC, \
                                                                   max_num_of_try=1000, \
                                                                   max_num_of_restart=0 \
                                                                   )

    def tearDown(self):
        pass

    def test_find_solution_totally_random(self):
        walker = MazeWalker.MazeWalker(maze=self.maze1, config=self.config_rand1)
        sol = walker.find_solution()
        self.assertEqual(sol[0], 'Success', "Solution not find!")
        
    def test_find_solution_random_no_retry(self):
        walker = MazeWalker.MazeWalker(maze=self.maze1, config=self.config_rand_no_retry)
        sol = walker.find_solution()
        self.assertEqual(sol[0], 'Success', "Solution not find!")
        
    def test_find_solution_deterministic(self):
        walker = MazeWalker.MazeWalker(maze=self.maze1, config=self.config_deterministic)
        sol = walker.find_solution()
        self.assertEqual(sol[0], 'Success', "Solution not find!")
        
    def test_find_solution_with_cycl_totally_random(self):
        walker = MazeWalker.MazeWalker(maze=self.maze_with_circle, config=self.config_rand1)
        sol = walker.find_solution()
        self.assertEqual(sol[0], 'Success', "Solution not find!")
        
    def test_find_solution_with_cycl_random_no_retry(self):
        walker = MazeWalker.MazeWalker(maze=self.maze_with_circle, config=self.config_rand_no_retry)
        sol = walker.find_solution()
        self.assertEqual(sol[0], 'Success', "Solution not find!")
        
    def test_find_solution_with_cycl_deterministic(self):
        walker = MazeWalker.MazeWalker(maze=self.maze_with_circle, config=self.config_deterministic)
        sol = walker.find_solution()
        self.assertEqual(sol[0], 'Success', "Solution not find!")
        
    def test_unsolvable_totally_random(self):
        walker = MazeWalker.MazeWalker(maze=self.maze_unsolvable, config=self.config_rand1)
        sol = walker.find_solution()
        self.assertEqual(sol[0], 'Stacked', "Should stacked!")
        self.assertEqual(sol[3], 'Max number of restart exceeded!', "Should stacked!")
        
    def test_unsolvable_random_no_retry(self):
        walker = MazeWalker.MazeWalker(maze=self.maze_unsolvable, config=self.config_rand_no_retry)
        sol = walker.find_solution()
        self.assertEqual(sol[0], 'Stacked', "Should stacked!")
        self.assertEqual(sol[3], 'Walker stacked!', "Should stacked!")
        
    def test_unsolvable_deterministic(self):
        walker = MazeWalker.MazeWalker(maze=self.maze_unsolvable, config=self.config_deterministic)
        sol = walker.find_solution()
        self.assertEqual(sol[0], 'Stacked', "Should stacked!")
        self.assertEqual(sol[3], 'Walker stacked!', "Should stacked!")

    def test_unsolvable_with_cycl_totally_random(self):
        walker = MazeWalker.MazeWalker(maze=self.maze_unsolvable_with_circle, config=self.config_rand1)
        sol = walker.find_solution()
        self.assertEqual(sol[0], 'Stacked', "Should stacked!")
        self.assertEqual(sol[3], 'Max number of restart exceeded!', "Should stacked!")
        
    def test_unsolvable_with_cycl_random_no_retry(self):
        walker = MazeWalker.MazeWalker(maze=self.maze_unsolvable_with_circle, config=self.config_rand_no_retry)
        sol = walker.find_solution()
        self.assertEqual(sol[0], 'Stacked', "Should stacked!")
        self.assertEqual(sol[3], 'Walker stacked!', "Should stacked!")
        
    def test_unsolvable_with_cycl_deterministic(self):
        walker = MazeWalker.MazeWalker(maze=self.maze_unsolvable_with_circle, config=self.config_deterministic)
        sol = walker.find_solution()
        self.assertEqual(sol[0], 'Stacked', "Should stacked!")
        self.assertEqual(sol[3], 'Walker stacked!', "Should stacked!")

if __name__ == "__main__":
    unittest.main()