# -----------------------------------------------------------
# Solve-Lonpos : a brute-force solver for a physical puzzle called Lonpos
#
# MIT License
#
# Copyright (c) 2022 Umut Yigit Dural

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# -----------------------------------------------------------

# Güneşime <3

import numpy as np
from colored import fg, bg, attr
import random

class LonposSolver():

    # We define the dictionary of blocks as set of vectors
    # For example:
    #----O  
    #---OOO     : (0,0),(1,0),(2,0),(1,1),(1,-1)
    #----O
    #
    # Idea: Use the leftmost point of a block as relative origin and fill the board from left to right. 
    # This way

    def __init__(self,blocks_dict,board_shape) -> None:

        self.blocks_dict = blocks_dict
        self.board_shape = board_shape
        self.empty_board = np.zeros(board_shape,dtype=int)

    def rotate_block(self,block_points):
        r_matrix = np.array([[0,-1],
                          [1, 0]])

        # The columns of this matrix are the relative points of the blocks
        c_matrix = np.transpose(np.array(block_points))

        rotated = r_matrix @ c_matrix

        # We still need to shift the points 
        # Find the minimum of each axis and push it so that the left-top corner is the new origin
        leftmost = min(rotated[1])

        # Find the point with the maximum y which is in the leftmost column and shift accordingly so that this point is the (0,0) now
        rotated[0] += (abs(min([rotated[0][i] for i in range(len(rotated[1])) if rotated[1][i] == leftmost])) * np.ones((1,len(rotated[0])),dtype=int)).flatten()

        rotated[1] += (abs(leftmost) * np.ones((1,len(rotated[1])), dtype = int)).flatten()
       
        return [tuple(column) for column in np.transpose(rotated)]

    def is_valid(self,board,position):
        """ Checks if a position is in the given board and the place in this position is empty and returns the boolean value
        """
        if position[0] >= self.board_shape[0] or position[1] >= self.board_shape[1] or position[0]<0 or position[1]<0:
            return False

        return board[position] == 0

    def place_block(self,board,block_name,block_points,position):
        """ Places the block if it's possible in the given position, returns a new board, if not possible returns False

        :param board:
        :type board:
        :param block_name: 
        :type block_name: 
        :param block_points: the points of the block relative to the origin (pivot) of this block
        :type block_points: list of tuples
        :param position: a tuple of x and y coordinate in the board
        :type position: tuple
        :return: the new board with the block placed in the given position
        :rtype: np.matrix | boolean
        """ 
        new_board = board.copy()

        v_position = np.array(position) 

        # Iterate through all indicex of a block
        for point in block_points:
            # Return the old board if it is not possible to place and also false to indicate that the operation was failed
            v_point = np.array(point)
            if not self.is_valid(board, tuple(v_point + v_position)):
                return board , False
            new_board[tuple(v_point + v_position)] = block_name
        return new_board, True

    def find_first_empty(self,board):
        """ Find the first empty point in the given board. Iterates through rows and then columns for our heuristic 
        """
        shape = np.shape(board)
        for column in range(shape[1]):
            for row in range(shape[0]):
                position = (row,column)
                if self.is_valid(board,position):
                    return position
        return None   

    def __solve(self,board,block_names_set):
        """ Solve the given board with the given blocks recursively
        """
        first_empty = self.find_first_empty(board)

        # If there isn't any empty point in the board return the solution
        if first_empty is None:
            return board    

        if len(block_names_set) == 0:
            return None

        # For all remaining blocks in the set:
        for block_name in block_names_set:
            #For all rotations of the block:
            rotated_block_points = self.blocks_dict[block_name]
            for i in range(4):  
                # Try to place the block
                new_board, check = self.place_block(board,block_name,rotated_block_points,first_empty)
                
                # If the block is placed
                if check:
                    # Try to solve the new_board with the remaining blocks
                    result = self.__solve(new_board, block_names_set.difference(set([block_name])))
                    
                    # If it was possible to fill it return the result
                    if result is not None:
                        return result 

                    # If it is not possible with this combination, iterate through other rotations and blocks

                # Rotate the block
                rotated_block_points = self.rotate_block(rotated_block_points)
        return None

    def solve(self,board = None, blocks_left = None):
        if board is None or blocks_left is None:
            result = self.__solve(self.empty_board,set(self.blocks_dict.keys())) 
        else:
            result = self.__solve(board,blocks_left) 

        if result is not None:
            return result
        return False

    def fill_board(self,blocks):
        pass

    
    def draw_board(self,board):
        """Converts the given board matrix into a colored representation of the board 
        
        """
        colored_board = list()
        color_dict= dict()

        for row in board:
            colored_row = ""
            for entry in row:
                if entry == 0:
                    symbol = "-"
                else:
                    symbol = "O"
                if entry not in color_dict:
                    color_dict[entry] = random.randint(0,255)
                colored_row +=  fg(color_dict[entry]) + symbol
                colored_row += attr('reset')
            print(colored_row)
            colored_board.append(colored_row)
        return colored_board     


        








    



   


