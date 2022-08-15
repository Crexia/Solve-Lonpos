# -----------------------------------------------------------
# Lonpos-solver : a brute-force solver for a puzzle called Lonpos
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

# We define the dictionary of blocks as set of vectors
# For example:
#----O  
#---OOO     : (0,0),(1,0),(2,0),(1,1),(1,-1)
#----O
#
# Idea: Use the leftmost point of a block as relative origin and fill the board from left to right. 
# This way

blocks_dict = {1:[(0,0),(0,1)]}


board = np.zeros((5,11),dtype=int)

print(board[(1,1)])


def rotate_block(block):
    r_matrix = np.matrix([[0,-1],
                          [1, 0]])

    # The columns of this matrix are the relative points of the blocks
    c_matrix= np.transpose(np.matrix(blocks_dict[block]))

    rotated = r_matrix @ c_matrix

    # We still need to shift the points 
    # Find the minimum of each axis and push it so that the left-top corner is the new origin
    leftmost = min(rotated[0])
    rotated[0] -= min(rotated[0]) * np.ones(1,len(rotated[0]))

    # Find the point with the maximum y which is in the leftmost column and shift accordingly so that this point is the (0,0) now
    rotated[1] -= max([rotated[1][i] for i in range(len(rotated[0])) if rotated[0][i] == leftmost]) * np.ones(1,len(rotated[0]))

    return rotated[:, 0:]

def is_empty(board,position):
### Checks if a position in the given board is empty and returns the boolean value
    return board[position] == 0


def place_block(board,block_name,block_points,position):
    """ Places the block if it's possible in the given position, returns a new board """ 

    new_board = board.copy()

    # Iterate through all indicex of a block
    for point in block_points:

        # Return the old board if it is not possible to place and also false to indicate that the operation was failed
        if not is_empty(board,point + position):
          return board,False

        new_board[point + position] = block_name


    return new_board, True



def find_first_empty(board):
    """ Find the first empty point in the given board. Iterates through rows and then columns for our heuristic 
    
    """
    shape = board.shape()
    for column in range(shape[1])
        for row in range(shape[0]):
            position = (row,column)
            if is_empty(board,position):
                return position
    return False

def solve(board,block_names_set):

    first_empty = find_first_empty(board)

    if first_empty == False:
        return board    

    for block_name in block_names_set:
        rotated_block_points = blocks_dict[block_name]
        for i in range(4):  

            new_board, check = place_block(board,block_name,rotated_block_points)

            if check:
                result = solve(new_board, block_names_set.difference(set(block_name)))
                if result != False:
                    return result 

            rotated_block_points = rotate_block(rotated_block_points)
    return False




    
    
    



   


