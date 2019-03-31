### Imports
import numpy as np
import time
import random

################################################################################
### Tetraminos
T = 1 ; S = 2 ; Z = 3 ; J = 4 ; L = 5 ; I = 6 ; O = 7

class Tetra:
    ### Init
    def __init__(self, color = None, rot = None, anchor = None):
        if color is None: color = self._gen_random_color()
        if rot is None: rot = self._gen_random_rot()
        if anchor is None: anchor = self._gen_random_start()
        self._shape_from_color(color, rot)
        self.anchor = anchor

    ### Properties
    @property
    def anchor(self): return self._anchor
    @anchor.setter
    def anchor(self,a): self._anchor = a
    @property
    def shape(self): return self._shape
    @shape.setter
    def shape(self,shape): self._shape = shape

    ### Function
    def _shape_from_color(self, color, rot  = 0):
        assert 1 <= color <= 7
        tetra_list = [ [], # element zero for convenience ; so that tetraminos(J) outputs a J
        	[[1, 1, 1],
             [0, 1, 0]],
        	[[0, 2, 2],
        	 [2, 2, 0]],
        	[[3, 3, 0],
        	 [0, 3, 3]],
        	[[4, 0, 0],
        	 [4, 4, 4]],
        	[[0, 0, 5],
        	 [5, 5, 5]],
        	[[6, 6, 6, 6]],
        	[[7, 7],
        	 [7, 7]]]
        self.shape = tetra_list[color]
        self.rot_l(rot)

    def _gen_random_color(self): return random.randint(1,7)
    def _gen_random_rot(self): return random.randint(0,3)
    def _gen_random_start(self): return (0,random.randint(3,6))

    def get_full_pose(self):
        pose = []
        for (i,j),cell in np.ndenumerate(self.shape):
            if cell != 0:
                if pose == []: pose = np.matrix([self.anchor[0]+i, self.anchor[1]+j]).transpose()
                else         : pose = np.hstack([pose, np.matrix([self.anchor[0]+i, self.anchor[1]+j]).transpose()])
        return pose

    def rot_l(self, n = 1): self.shape = np.rot90(self.shape,n)
    def rot_r(self, n = 1): self.shape = np.rot90(self.shape,-n)

    def _move(self, move):
        assert move == (0,1) or move == (1,0) or move == (0,-1)
        print (self.anchor)
        self.anchor += move
        print (self.anchor)

    def fall(self): self._move((1,0))
    def move_l(self): self._move((0,-1))
    def move_r(self): self._move((0,1))

### Board
rows = 20
cols = 10
def new_board(rows = rows,cols = cols):
    return np.zeros((rows,cols), dtype=np.uint8)

def remove_line(board, i):
    return np.delete(board, i, axis=0)

def add_line(board):
    assert board.shape[0] < rows
    return np.concatenate((np.zeros((1,cols), dtype=np.uint8),board), axis=0)

# def create_tetra(board, tetras = tetraminos, start = None):
#     if start is None: start = random.randint(round(board.shape[1]*40/100), round(board.shape[1]*70/100)) - round(len(tetra[0])-1)
#     for i,row in enumerate(tetra):
#         for j,cell in enumerate(row):
#             board[i,start+j] = cell
#     return (board,(0,start))


################################################################################
### Main
board = new_board()
tetra = Tetra(L)
tetra.move_l()
# print (board)

# while 1:
#     time.sleep(1)
#     move = (0,1)
#     board, pose = move_tetra(board, tetra, pose, move)
#     print(board)
#
#
