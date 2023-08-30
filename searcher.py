#
# searcher.py (Final project)
#
# classes for objects that perform state-space search on Eight Puzzles  
#

import random
from state import *

class Searcher:
    """ A class for objects that perform random state-space
        search on an Eight Puzzle.
        This will also be used as a superclass of classes for
        other state-space search algorithms.
    """
    
    def __init__(self, depth_limit):
        """ constructs a new Searcher object by initializing the following 
            attributes: states, num_tested, & depth_limit.
        """


        self.states = []
        self.num_tested = 0
        self.depth_limit = depth_limit

    def __repr__(self):
        """ returns a string representation of the Searcher object
            referred to by self.
        """
        s = type(self).__name__ + ': '
        s += str(len(self.states)) + ' untested, '
        s += str(self.num_tested) + ' tested, '
        if self.depth_limit == -1:
            s += 'no depth limit'
        else:
            s += 'depth limit = ' + str(self.depth_limit)
        return s
    
    def add_state(self, new_state):
        """ takes a single State object called new_state and adds it to the 
            Searcher‘s list of untested states.
        """
        self.states += [new_state]
        
    def should_add(self, state):
        """ takes a State object called state and returns True if the called 
            Searcher should add state to its list of untested states, 
            and False otherwise.
        """
        if self.depth_limit != -1 and state.num_moves > self.depth_limit:
            return False
        elif state.creates_cycle():
            return False
        return True
        
    def add_states(self, new_states):
        """ takes a list State objects called new_states, and that processes 
            the elements of new_states one at a time.
        """
        for s in new_states:
            if self.should_add(s):
                self.add_state(s)
        
    def next_state(self):
        """ chooses the next state to be tested from the list of 
            untested states, removing it from the list and returning it
        """
        s = random.choice(self.states)
        self.states.remove(s)
        return s

    def find_solution(self, init_state):
        """ performs a full state-space search that begins at the specified 
            initial state init_state and ends when the goal state is found or 
            when the Searcher runs out of untested states.
        """
        self.add_state(init_state)
        while self.states != []:
            s = self.next_state()
            self.num_tested += 1
            if s.is_goal():
                return s
            else:
                self.add_states(s.generate_successors())
        return None


class BFSearcher(Searcher):
    """ A class for searcher objects that perform breadth-first search (BFS) 
        instead of random search.
    """
    
    def next_state(self):
        """ overrides the next_state method that is inherited from Searcher. 
            Rather than choosing at random from the list of untested states, 
            this version of next_state should follow FIFO ordering.
        """
        s = self.states[0]
        self.states.remove(s)
        return s
        
class DFSearcher(Searcher):
    """ A class for searcher objects that perform depth-first search (DFS) 
        instead of random search.
    """
    
    def next_state(self):
        """ very similar to the method written for the BFSearcher Class but 
            instead follows LIFO ordering.
        """
        s = self.states[-1]
        self.states.remove(s)
        return s
    

def h0(state):
    """ a heuristic function that always returns 0 """
    return 0

def h1(state):
    """ a heuristic function that always returns the number of misplaced tiles
        in the Board object associated with the State.
    """
    return state.board.num_misplaced()

def h2(state):
    """ a heuristic function that always returns the number of misplaced tiles
        in the column of the Board object associated with the State.
    """
    return state.board.new_misplaced()

class GreedySearcher(Searcher):
    """ A class for objects that perform an informed greedy state-space
        search on an Eight Puzzle.
    """
    def __init__(self, heuristic):
        """ constructs a new GreedySearcher object.
        """
        super().__init__(-1)
        self.heuristic = heuristic
        

    def __repr__(self):
        """ returns a string representation of the GreedySearcher object
            referred to by self.
        """
        s = type(self).__name__ + ': '
        s += str(len(self.states)) + ' untested, '
        s += str(self.num_tested) + ' tested, '
        s += 'heuristic ' + self.heuristic.__name__
        return s
    
    def priority(self, state):
        """ computes and returns the priority of the specified state,
            based on the heuristic function used by the searcher
        """
        return -1 * self.heuristic(state)
    
    def add_state(self, state):
        """ overrides the add_state method that is inherited from 
            Searcher. Rather than simply adding the specified state to the 
            list of untested states, the method should add a sublist that is a 
            [priority, state] pair, where priority is the priority of state 
            that is determined by calling the priority method.
        """
        self.states += [[self.priority(state), state]]
        
    def next_state(self):
        """ overrides the next_state method that is inherited from Searcher. 
            This version of next_state should choose one of the states with 
            the highest priority.
        """
        s = max(self.states)
        self.states.remove(s)
        return s[1]
    
class AStarSearcher(GreedySearcher):
    """ A class for searcher objects that perform A* search.
    """
    
    def priority(self, state):
        """ computes and returns the priority of the specified state,
            based on the heuristic function used by the searcher.
        """
        return -1 * (self.heuristic(state) + state.num_moves)
      
    