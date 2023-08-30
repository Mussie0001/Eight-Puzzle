#
# board.py 
#
# A Board class for the Eight Puzzle
#

# a 2-D list that corresponds to the tiles in the goal state
GOAL_TILES = [['0', '1', '2'],
              ['3', '4', '5'],
              ['6', '7', '8']]

GOAL_COL = [['0', '3', '6'], 
            ['1', '4', '7'], 
            ['2', '5', '8']]
class Board:
    """ A class for objects that represent an Eight Puzzle board.
    """
    def __init__(self, digitstr):
        """ a constructor for a Board object whose configuration
            is specified by the input digitstr
            input: digitstr is a permutation of the digits 0-9
        """
        # check that digitstr is 9-character string
        # containing all digits from 0-9
        assert(len(digitstr) == 9)
        for x in range(9):
            assert(str(x) in digitstr)

        self.tiles = [[' '] * 3 for x in range(3)]
        self.blank_r = -1
        self.blank_c = -1

        for r in range(3):
            for c in range(3):
                self.tiles[r][c] = (digitstr[3 * r + c])
                if self.tiles[r][c] == '0':
                    self.blank_r = r
                    self.blank_c = c


    
    def __repr__(self):
        """ returns a string representation of a Board object.
        """
        s = ''
        for r in range(3):
            for c in range(3):
                if self.tiles[r][c] == '0':
                    s += '_ '
                else:
                    s += str(self.tiles[r][c]) + ' '
            s += '\n'
        return s
    
    def move_blank(self, direction):
        """ takes as input a string direction that specifies the direction in 
            which the blank should move, and that attempts to modify the 
            contents of the called Board object accordingly.
        """
        
        
        for r in range(3):
            for c in range(3):
                if self.tiles[r][c] == "0":
                    
                    if direction == 'up':
                        if r != 0:
                            self.tiles[r][c] = self.tiles[r - 1][c]
                            self.tiles[r - 1][c] = "0"
                            self.blank_r = r - 1
                            return True
                        
                    elif direction == 'down':
                        if r != 2:
                            self.tiles[r][c] = self.tiles[r + 1][c]
                            self.tiles[r + 1][c] = "0"
                            self.blank_r = r + 1
                            return True
                    elif direction == 'left':
                        if c != 0:
                            self.tiles[r][c] = self.tiles[r][c - 1]
                            self.tiles[r][c - 1] = "0"
                            self.blank_c = c - 1
                            return True
                    elif direction == 'right':
                        if c != 2:
                            self.tiles[r][c] = self.tiles[r][c + 1]
                            self.tiles[r][c + 1] = "0" 
                            self.blank_c = c + 1
                            return True
                    else:
                        return False
                        
        
      

    def digit_string(self):
        """ creates and returns a string of digits that corresponds to the 
            current contents of the called Board object’s tiles attribute.
        """
        
        digit_string = ''
        
        for r in range(3):
            for c in range(3):
                if self.tiles[r][c] == '_':
                    digit_string += '0'
                else:
                    digit_string += str(self.tiles[r][c])
                    
        return digit_string
        
    def copy(self):
        """ returns a newly-constructed Board object that is a deep copy of 
            the called object.
        """
        copy = Board(self.digit_string())
        return copy
    
    def num_misplaced(self):
        """ counts and returns the number of tiles in the called Board object 
            that are not where they should be in the goal state.
        """
        num = 0
        for r in range(len(self.tiles)):
            for c in range(len(self.tiles)):
                if self.tiles[r][c] != GOAL_TILES[r][c]:
                    if self.tiles[r][c] != '0':
                        num += 1
        return num
    
    def new_misplaced(self):
        """ counts and returns the number of misplaced tiles in the column.
        """
        returnnum = 0
        for r in range(3):
            for c in range(3):
                if self.tiles[r][c] not in GOAL_TILES[r] and self.tiles[r][c] != '0':
                    returnnum += 1
                if self.tiles[c][r] not in GOAL_COL[r]:
                    returnnum += 1
                    
        if self.tiles[0][0] != '0':
            returnnum -= 1
        return returnnum
    
    def __eq__(self, other):
        """ return True if the called object (self) and the argument (other) 
            have the same values for the tiles attribute, and False otherwise.
        """
        if self.digit_string() == other.digit_string():
            return True
        else:
            return False
        
    