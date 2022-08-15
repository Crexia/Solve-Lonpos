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


import numpy as np



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
        self.board = np.zeros(board_shape,dtype=int)

        pass



    def rotate_block(self,block):
        r_matrix = np.matrix([[0,-1],
                          [1, 0]])

        # The columns of this matrix are the relative points of the blocks
        c_matrix = np.transpose(np.matrix(self.blocks_dict[block]))

        rotated = r_matrix @ c_matrix

        # We still need to shift the points 
        # Find the minimum of each axis and push it so that the left-top corner is the new origin
        leftmost = min(rotated[0])
        rotated[0] -= min(rotated[0]) * np.ones(1,len(rotated[0]))

        # Find the point with the maximum y which is in the leftmost column and shift accordingly so that this point is the (0,0) now
        rotated[1] -= max([rotated[1][i] for i in range(len(rotated[0])) if rotated[0][i] == leftmost]) * np.ones(1,len(rotated[0]))

        return rotated[:, 0:]

    def is_empty(self,board,position):
        """ Checks if a position in the given board is empty and returns the boolean value
        """
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

        # Iterate through all indicex of a block
        for point in block_points:

            # Return the old board if it is not possible to place and also false to indicate that the operation was failed
            if not self.is_empty(board,point + position):
                return board,False

        new_board[point + position] = block_name

        return new_board, True



    def find_first_empty(self,board):
        """ Find the first empty point in the given board. Iterates through rows and then columns for our heuristic 
    
        """
        shape = board.shape()
        for column in range(shape[1]):
            for row in range(shape[0]):
                position = (row,column)
                if self.is_empty(board,position):
                    return position
        return False    

    def solve(self,board,block_names_set):
        """ Solve the given board with the given blocks recursively
        """

        first_empty = self.find_first_empty(board)

        # If there isn't any empty point in the board return the solution
        if first_empty == False:
            return board    

        # For all remaining blocks in the set:
        for block_name in block_names_set:

            #For all rotations of the block:
            rotated_block_points = self.blocks_dict[block_name]
            for i in range(4):  
                # Try to place the block
                new_board, check = self.place_block(board,block_name,rotated_block_points)

                # If the block is placed
                if check:
                    # Try to solve the new_board with the remaining blocks
                    result = self.solve(new_board, block_names_set.difference(set(block_name)))

                    # If it was possible to fill it return the result
                    if result != False:
                        return result 

                    # If it is not possible with this combination, iterate through other rotations and blocks

                # Rotate the block
                rotated_block_points = self.rotate_block(rotated_block_points)

        return False




    
    
    



   


