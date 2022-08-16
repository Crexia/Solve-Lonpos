from lonpos import LonposSolver
from colored import fg, bg, attr

blocks_dict = {1:[(0,0),(1,0),(1,1)], 
                2:[(0,0),(0,1),(1,0),(0,2)],
                3:[(0,0),(0,1),(1,1),(1,0)],
                13:[(0,0),(0,1),(-1,1),(1,0)],
                4:[(0,0),(0,1),(0,2),(0,3)],
                5:[(0,0),(0,1),(0,2),(1,2),(1,3)],
                16:[(0,0),(1,0),(1,1),(2,1),(3,1)],
                6:[(0,0),(1,0),(1,1),(2,1),(2,2)],
                7:[(0,0),(0,1),(1,0),(1,1),(0,2)],
                8:[(0,0),(0,1),(0,2),(1,1),(-1,1)],
                9:[(0,0),(1,0),(0,1),(0,2),(1,2)],
                10:[(0,0),(0,1),(0,2),(0,3),(1,2)],
                15:[(0,0),(0,1),(0,2),(0,3),(1,1)],
                11:[(0,0),(1,0),(2,0),(0,1),(0,2)],
                12:[(0,0),(1,0),(0,1),(0,2),(0,3)],
                14:[(0,0),(1,0),(1,1),(1,2),(1,3)],
                }


my_solver = LonposSolver(blocks_dict=blocks_dict, board_shape= (5,11))

# new_board, check = my_solver.place_block(my_solver.board,1,blocks_dict[1],(0,0))

# print( new_board)

solution = my_solver.solve()
print(solution)
my_solver.draw_board(solution)



# print(my_solver.rotate_block(blocks_dict[12]))

    
    