####################################################################################################
### Imports
import numpy as np
import time
import random


####################################################################################################
### Defines
T = 1 ; S = 2 ; Z = 3 ; J = 4 ; L = 5 ; I = 6 ; O = 7
down = (1,0) ; left = (0,-1) ; right = (0,1) ; rot = (-1,0)


####################################################################################################
### Tetraminos
class Tetra:
    ### Init
    def __init__(self, shape = None, anchor = None):
        if shape is None:
            color = self._gen_random_color()
            rot = self._gen_random_rot()
            self._shape_from_color(color, rot)
        else:
            self.shape = shape
        if anchor is None: anchor = self._gen_random_start()
        self.anchor = anchor

    ### Properties
    @property
    def anchor(self): return self._anchor
    @anchor.setter
    def anchor(self,v): self._anchor = v
    @property
    def shape(self): return self._shape
    @shape.setter
    def shape(self,v): self._shape = v

    ### Shape generator
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

    # Random generation of tetramino
    def _gen_random_color(self): return random.randint(1,7)
    def _gen_random_rot(self): return random.randint(0,3)
    def _gen_random_start(self): return (0,random.randint(3,6))

    # Movement functions
    def rot_l(self, n = 1): self.shape = np.rot90(self.shape,n)
    def rot_r(self, n = 1): self.shape = np.rot90(self.shape,-n)
    def move(self, m): self.anchor = (self.anchor[0]+m[0], self.anchor[1]+m[1])
    def move_d(self): self.move(down)
    def move_l(self): self.move(left)
    def move_r(self): self.move(right)

    # Status computation
    def get_full_pose(self):
        pose = []
        for (i,j),cell in np.ndenumerate(self.shape):
            if cell != 0:
                pose.append((self.anchor[0]+i, self.anchor[1]+j))
        return pose
    def get_color(self): return np.amax(self.shape)

    # To string
    def __str__(self):
        return str(self.shape)+'  @ '+str(self.anchor)


####################################################################################################
### Board
class Board:
    ### Init
    def __init__(self, rows = None, cols = None):
        self.rows = rows
        self.cols = cols
        self.grid = np.full((rows,cols), '-', dtype=np.unicode_)
        self.tetra = Tetra()
        self._draw_tetra()

    # Properties
    @property
    def rows(self): return self._rows
    @rows.setter
    def rows(self,v): self._rows = v
    @property
    def cols(self): return self._cols
    @cols.setter
    def cols(self,v): self._cols = v
    @property
    def grid(self): return self._grid
    @grid.setter
    def grid(self,v): self._grid = v

    # Lines management
    def remove_line(self, i):
        self.grid = np.delete(self.grid, i, axis=0)
    def fill_grid(self):
        assert self.grid.shape[0] < self.rows
        self.grid = np.concatenate((np.full((self.rows-self.grid.shape[0],cols), '-', dtype=np.unicode_),grid), axis=0)

    # Draw or undraw tetramino
    def _draw_tetra(self):
        pose = self.tetra.get_full_pose()
        for cell in pose: self.grid[cell] = self.tetra.get_color()
    def _undraw_tetra(self):
        pose = self.tetra.get_full_pose()
        for cell in pose: self.grid[cell] = '-'

    # Collision checks
    def _check_coll(self, m):
        assert m == left or m == right or m == down
        next_tetra = Tetra(self.tetra.shape, self.tetra.anchor)
        next_tetra.move(m)
        next_pose = next_tetra.get_full_pose()
        curr_pose = self.tetra.get_full_pose()
        coll = False
        for cell in next_pose:
            if cell[1] < 0 or cell[1] > self.cols-1 or cell[0] > self.rows-1: coll = True ; break
            if cell not in curr_pose and self.grid[cell] != '-': coll = True ; break
        return coll

    # Tetramino updates
    def update(self, m):
        assert m == left or m == right or m == down
        if not self._check_coll(m):
            self._undraw_tetra()
            self.tetra.move(m)
            self._draw_tetra()
        elif m == down:
            if self.tetra.anchor[0] != 0:
                self.tetra = Tetra()
                self._draw_tetra()
            else:
                return True

    # To string
    def __str__(self):
        return str(self.grid)


####################################################################################################
### Main
rows = 20
cols = 10

board = Board(rows, cols)
print(board, '\n\n\n')


while 1:
    time.sleep(0.05)
    if board.update(down) is True: break
    print(board, '\n\n\n')
