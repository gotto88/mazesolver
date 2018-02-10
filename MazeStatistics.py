'''
Created on Dec 19, 2017

@author: gotto
'''

class WalkerStats(object):
    '''
    This class represents the statistic of a MazeWalker and contains methods for detail analysis
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.number_of_tries = 0
        self.number_of_step_forward = 0
        self.number_of_step_back = 0
        
        self.number_of_stacked = 0
        self.number_of_overstep = 0
        self.number_of_restart = 0
        
    def __str__(self):
        
        return  "Number of tries: " + str(self.number_of_tries) + "\n" \
                + "Number of step forward: " + str(self.number_of_step_forward) + "\n" \
                + "Number of step back: " + str(self.number_of_step_back) + "\n" \
                + "Number of stack: " + str(self.number_of_stacked) + "\n" \
                + "Number of overstep: " + str(self.number_of_overstep) + "\n" \
                + "Number of restart: " + str(self.number_of_restart)
                
                