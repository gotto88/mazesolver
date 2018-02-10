'''
Created on Nov 21, 2017

@author: gotto
'''

import numpy as np

from solver_package import MazeStatistics
from solver_package import Maze

class WalkMode(object):
        
        UNKNOWN = -1
        DETERMINISTIC = 0
        TOTTALY_RANDOM = 1
        RANDOM_DEPT_WALK_NO_RETRY = 2
        
class WalkerConfiguration(object):
    
    def __init__(self, **params):
        self.mode = WalkMode.UNKNOWN
        self.maximum_number_of_tries = 0
        self.maximum_number_of_restart = 0
        
        if 'mode' in params:
            self.mode = params['mode']
        if 'max_num_of_try' in params:
            self.maximum_number_of_tries = params['max_num_of_try']
        if 'max_num_of_restart' in params:
            self.maximum_number_of_restart = params['max_num_of_restart']
        
class MazeWalker(object):
    '''
    This class represents a walker on maze
    '''
    direction_map = {
        'invalid' : -1,
        'up' : 0,
        'right' : 1,
        'down' : 2,
        'left' : 3 
    }
    
    action_map = {
        'start' : 0,
        'stay' : 1,
        'forward' : 2,
        'back' : 3
    }
    
    marks = set(['in road', 'visited'])

    def __init__(self, **params):
        '''
        Constructor of MazeWalker. In the costructor the following can be specifiled:
        maze :  
        '''
        
        #Corresponding maze
        self.current_maze = None
        self.map_of_maze = None
        if 'maze' in params:
            self.set_maze(params['maze'])
        
        #Dynamic attributes
        self.num_of_restarts = 0
        self.isstacked = False
        self.startpoint = []
        self.current_position = []
        self.last_try = -1
        self.last_action = None
        
        #History
        self.tries_from_start = []
        self.road = []
        self.first_try_from_here = []
        self.num_of_try_from_here = []
        
        #Configuration
        self.config = WalkerConfiguration()
        if 'config' in params:
            self.set_config(params['config'])
        
        #Statistic
        self.stat = MazeStatistics.WalkerStats()
        
    
    #Setting methods
    def set_config(self, config):
        ''' Setting the walking mode '''
        self.config = config
    
    def set_maze(self, maze):
        ''' Set the maze in which the '''
        if maze.validity == Maze.Validity.VALID:
            self.current_maze = maze
            self.map_of_maze = maze.matrix.tolist()
            self.clean_map()
                    
    def clean_map(self):
        ''' Remove all marks from the map '''
        for i in range(len(self.map_of_maze)):
            for j in range(len(self.map_of_maze[i])):
                self.map_of_maze[i][j] = set()
                
    #Starting
    def starting(self):
        ''' Move the walker to the start point of the maze and clear the history''' 
        if self.current_maze is not None:
            self.startpoint = list(self.current_maze.get_start_point())
        else:
            return (False, "Maze not set!")
        if self.startpoint != []:
            self.move_to_start()
            self.clear_history()
            self.clean_map()
            self.tries_from_start = set([0,1,2,3])
            return (True, "Walker started")
        else:
            return (False, "Start point not found!")
    
    def restart(self):
        ''' Put the walker back to the start point of the maze and clear the history'''
        if self.startpoint != []:
            self.move_to_start()
            self.clear_history()
            self.tries_from_start = set([0,1,2,3])
            return (True, "Walker restarted")
        else:
            return (False, "Start point not found!")
        self.stat.number_of_restart += 1
    
    def move_to_start(self):
        self.current_position = self.startpoint
        pass
    
    def clear_history(self):
        self.last_try = -1
        self.last_action = self.action_map['start']
        self.road = [-1]
        self.first_try_from_here = [-1]
        self.num_of_try_from_here = [0]
        self.isstacked = False
        
        self.stat.number_of_tries = 0
        self.stat.number_of_step_forward = 0
        self.stat.number_of_step_back = 0
    
    #Moving
    def move_forward(self, direction):
        self.last_try = direction
        if self.first_try_from_here[-1] == -1:
            self.first_try_from_here[-1] = direction
        self.num_of_try_from_here[-1] += 1
        
        self.last_action = self.action_map['forward']
        self.current_position = self.next_point(direction)
        self.mark_current_point_in_map('in road')
        
        self.road.append(direction)
        self.first_try_from_here.append(-1)
        self.num_of_try_from_here.append(0)
        
        self.stat.number_of_tries += 1
        self.stat.number_of_step_forward += 1
        
    def stay(self, direction):
        self.last_try = direction
        if self.first_try_from_here[-1] == -1:
            self.first_try_from_here[-1] = direction
        self.num_of_try_from_here[-1] += 1
        
        self.last_action = self.action_map['stay']
        
        self.stat.number_of_tries += 1
    
    def step_back(self):
        self.last_try = self.road[-1]
        
        self.last_action = self.action_map['back']
        self.demark_current_point_in_map('in road')
        self.current_position = self.next_point(self.inverse_direction(self.road[-1]))
        
        self.road.pop()
        self.first_try_from_here.pop()
        self.num_of_try_from_here.pop()
        
        self.stat.number_of_tries += 1
        self.stat.number_of_step_back += 1
    
    def try_direction(self, direction):
        next_point = self.next_point(direction)
        next_field = self.current_maze.get_field(next_point)
        if next_field in [-1,1]:
            self.stay(direction)
        elif next_field == 0:
            if 'in road' in self.get_point_in_map(next_point):
                self.stay(direction)
            else:
                self.move_forward(direction)
        elif next_field == -2:
            self.move_forward(direction)
    
    def next_point(self, direction):
        return [self.current_position[0] + (direction%2-1)*(1-direction), self.current_position[1] + (direction%2)*(2-direction)]
        
    def get_point_in_map(self, position):
        return self.map_of_maze[position[0]][position[1]]
        
    def mark_current_point_in_map(self, mark):
        if mark in self.marks:
            self.map_of_maze[self.current_position[0]][self.current_position[1]].add(mark)
        
    def demark_current_point_in_map(self, mark):
        if mark in self.marks:
            self.map_of_maze[self.current_position[0]][self.current_position[1]].remove(mark)
    
    @staticmethod
    def inverse_direction(direction):
        return (direction+2)%4
    
    def is_back(self, direction):
        return abs(self.road[-1]-direction) == 2
    
    #Direction choose
    def choose_new_direction(self):
        probs = [0,0,0,0]
        is_possible_direction = True
        
        if self.config.mode == WalkMode.TOTTALY_RANDOM:
            probs = [0.25,0.25,0.25,0.25]
            
        elif self.config.mode == WalkMode.DETERMINISTIC:
            if self.num_of_try_from_here[-1] >= 3:
                is_possible_direction = False
            else:
                from_dir = self.inverse_direction(self.road[-1])
                probs = [1 if i == (from_dir+self.num_of_try_from_here[-1]+1)%4 else 0 for i,pp in enumerate(probs)]
                
        elif self.config.mode == WalkMode.RANDOM_DEPT_WALK_NO_RETRY:
            if self.num_of_try_from_here[-1] >= 3:
                is_possible_direction = False
            else:
                from_dir = self.inverse_direction(self.road[-1])
                dirs = [from_dir,self.first_try_from_here[-1],self.last_try]
                probs = [1.0/(3-self.num_of_try_from_here[-1]) if i not in dirs[:self.num_of_try_from_here[-1]+1] else 0 for i,pp in enumerate(probs)]
        
        if is_possible_direction:
            return np.random.choice(4, 1, p=probs)[0]
        else:
            return -1
    
    def choose_new_direction_from_start(self):
        l = len(self.tries_from_start)
        if l == 0:
            return -1
        probs = [0,0,0,0]
        probs = [1.0/l if i in self.tries_from_start else 0 for i,pp in enumerate(probs)]
        return np.random.choice(4, 1, p=probs)[0]
    
    #Stepping
    def new_step(self):
        if self.last_action == MazeWalker.action_map['start'] or self.current_position == self.startpoint:
            direction = self.choose_new_direction_from_start()
            if direction == -1:
                self.isstacked = True
            else:
                self.try_direction(direction)
                if self.config.mode != WalkMode.TOTTALY_RANDOM:
                    self.tries_from_start.remove(direction)
        else:
            direction = self.choose_new_direction()
            if direction == -1 or self.is_back(direction):
                self.step_back()
            else:
                self.try_direction(direction)
    
    #Complete simulation
    def find_solution(self):
        st = self.starting()
        if st[0]:
            while True:
                self.new_step()
                if tuple(self.current_position) in self.current_maze.get_end_points():
                    return ('Success', self.road, self.stat, 'OK')
                if self.isstacked:
                    return ('Stacked', None, self.stat, 'Walker stacked!')
                if self.stat.number_of_tries > self.config.maximum_number_of_tries:
                    if self.stat.number_of_restart >= self.config.maximum_number_of_restart:
                        return ('Stacked', None, self.stat, 'Max number of restart exceeded!')
                    else:
                        re_st = self.restart()
                        if not re_st[0]:
                            return ('Error', None, None, re_st[1])
        else:
            return ('Error', None, None, st[1])
        