'''
Created on Nov 21, 2017

@author: Otto Peter Guraly

'''

import numpy as np

class Solvability(object):
        
        UNKNOWN = 0
        SOLVABLE = 1
        UNSOLVABLE = 2
        
class Validity(object):
        
        UNKNOWN = 0
        VALID = 1
        INVALID = 2

class Maze(object):
    '''
    This class represents a maze. The map of the maze is represented by a 2 dimension numpy array of integers.
    for example:
    [[-1,0,0],
     [1,1,0],
     [1,0,-2]]
    The meaning of integers in the arrays:
     -1: start point
     -2: goal point
      1: wall
      0: empty
    The Maze 
    '''
    
    valid_fields = set([-2,-1,0,1])

    maze_fields_maps = {
        -2 : 'finish',
        -1 : 'start',
         0 : 'empty',
         1 : 'wall'
    }
        
    
    def __init__(self, matrix):
        '''
        Constructor of the maze
        @params
        matrix: 
        x0:
        y0:
        '''
        self.matrix = np.array(matrix)
        self.validity = Validity.UNKNOWN
        self.solvable = Solvability.UNKNOWN
        self.startpoint = ()
        self.endpoints = []
        self.check_matrix()
        
    def set_matrix(self,matrix):
        """
        Set the matrix of the maze
        """
        self.matrix = np.array(matrix)
        self.validity = Validity.UNKNOWN
        self.solvable = Solvability.UNKNOWN
        self.startpoint = ()
        self.endpoints = []
        self.check_matrix()
        pass
        
    def check_matrix(self):
        """
        This function check if the maze is valid. The matrix should met the following criteria:
          - All value is match one from valid_fields
          - There is only one start point (-1)
          - There is at least one endpoint (-2) 
        """
        if self.validity != Validity.UNKNOWN:
            return self.validity
        
        number_of_start = 0
        
        it = np.nditer(self.matrix, flags=['multi_index'])
        
        while not it.finished:
            if int(it[0]) not in self.valid_fields:
                self.validity = Validity.INVALID
                return self.validity
            if it[0] == -1:
                number_of_start += 1
                if (number_of_start > 1):
                    self.validity = Validity.INVALID
                    return self.validity
                self.startpoint = it.multi_index
            if it[0] == -2:
                self.endpoints.append(it.multi_index)
            it.iternext()
            
        if len(self.endpoints) > 0 and number_of_start == 1:
            self.validity = Validity.VALID
        else:
            self.validity = Validity.INVALID
            
        return self.validity
    
    def get_start_point(self):
        """ Return with the coordinates of the starting point, if start point not specified try to find it"""
        if self.validity != Validity.VALID:
            return ()
        if self.startpoint != ():
            return self.startpoint
        else:
            self.find_start_point()
        return self.startpoint
    
    def find_start_point(self):
        """ Find the start point from the matrix and set it """
        it = np.nditer(self.matrix, flags=['multi_index'])
        
        while not it.finished:
            if it[0] == -1:
                self.startpoint = it.multi_index
                break
            it.iternext()
        
    def get_end_points(self):
        """ Return with the coordinates of the finish points, if no finish point specified try to find them """
        if self.validity != Validity.VALID:
            return []
        if self.endpoints != []:
            return self.endpoints
        else:
            self.find_end_points()
        return self.endpoints
    
    def find_end_points(self):
        """ Find the finish point from the matrix and set it """
        it = np.nditer(self.matrix, flags=['multi_index'])
        
        while not it.finished:
            if it[0] == -2:
                self.endpoints.append(it.multi_index)
            it.iternext()
    
    def get_field(self, corr):
        """ Return with the value of the specified field, if point is outside of the matrix return with 1 (wall) """
        if corr[0] < 0 or corr[1] < 0:
            return 1
        try:
            result = self.matrix[corr[0]][corr[1]]
            return result
        except IndexError:
            return 1