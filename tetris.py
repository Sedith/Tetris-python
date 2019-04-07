####################################################################################################
### Imports
import numpy as np
import time
import random


####################################################################################################
### Defines
T = 1 ; S = 2 ; Z = 3 ; J = 4 ; L = 5 ; I = 6 ; O = 7
down = (1,0) ; left = (0,-1) ; right = (0,1) ; rot = (-1,0)
moves = [down, left, right, rot]


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
        if anchor is None: anchor = (0,0)
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
    def move_d(self): self.move(down)
    def move_l(self): self.move(left)
    def move_r(self): self.move(right)
    def move(self, m):
        if m == rot:
            self.rot_l()
        else:
            self.anchor = (self.anchor[0]+m[0], self.anchor[1]+m[1])

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
    def remove_line(self, i_list):
        for i in reversed(sorted(i_list)): self.grid = np.delete(self.grid, i, axis=0)
    def fill_grid(self):
        if self.grid.shape[0] < self.rows:
            self.grid = np.concatenate((np.full((self.rows-self.grid.shape[0],self.cols), '-', dtype=np.unicode_),self.grid), axis=0)

    # Draw or undraw tetramino
    def _draw_tetra(self):
        pose = self.tetra.get_full_pose()
        for cell in pose: self.grid[cell] = self.tetra.get_color()
    def _undraw_tetra(self):
        pose = self.tetra.get_full_pose()
        for cell in pose: self.grid[cell] = '-'

    # Collision checks
    # either :
    # - pass tetra to tes as arg, then if it is none test for spawning
    # - check if move is none, then check accordingly
    # first is somehow cleaner here but requires changes in other functions
    # in order to make the translation for rotation, output the colliding
    # cells (or just an indication of where is the collision and how much
    # to shift). Then make translation accordingly and change and check again.
    def _check_coll(self, m):
        assert m == left or m == right or m == down or m == rot
        next_tetra = Tetra(self.tetra.shape, self.tetra.anchor)
        next_tetra.move(m)
        next_pose = next_tetra.get_full_pose()
        curr_pose = self.tetra.get_full_pose()
        coll = False
        for cell in next_pose:
            if cell[1] < 0 or cell[1] > self.cols-1 or cell[0] > self.rows-1: coll = True ; break
            if cell not in curr_pose and self.grid[cell] != '-': coll = True ; break
        return coll

    # Tetramino management
    def _spawn_tetra(self):
        offset = 1
        tries = 10
        for i in range(tries):
            spawn = (0,random.randint(offset, self.cols-offset-1))
            tetra = Tetra(anchor=spawn)
            pose = tetra.get_full_pose()
            coll = False
            for cell in pose:
                if cell[1] < 0 or cell[1] > self.cols-1: coll = True ; break
                if cell and self.grid[cell] != '-': coll = True ; break
            if not coll: self.tetra = tetra ; break

    def _remove_tetra(self):
        self.tetra = None
        i_list = []
        for i,row in enumerate(self.grid):
            full = True
            for cell in row:
                if cell == '-':
                    full = False
                    break
            if full: i_list.append(i)
        self.remove_line(i_list)
        self.fill_grid()

    # Tetramino updates
    # Having next tetra preview is quite easy
    # Scoring is updated when removing lines, very easy to implement
    # Check online how score is computed in other games ?
    def update(self, m):
        assert m == left or m == right or m == down or m == rot
        if not self._check_coll(m):
            self._undraw_tetra()
            self.tetra.move(m)
            self._draw_tetra()
        elif m == down:
            self._remove_tetra()
            self._spawn_tetra()
            if self.tetra is None : return True
            else: self._draw_tetra()

    # To string
    def __str__(self):
        return str(self.grid)


####################################################################################################
### Main
rows = 20
cols = 10

board = Board(rows, cols)
print(board, '\n\n\n')

# How to keyboard control ? Either :
# - having a runing clock and test it every loop if it time is dividable by
#   given period of fall, if so fall else check for keyboard else loop
# - have 2 threads, one for fall and one for fall and one for control
# first may result in some keyboard lag in controling, but probably much easier
# to implement than second which i don't even know if is doable
while 1:
    time.sleep(0.15)
    if board.update(moves[random.randint(0,3)]) is True: break
    # if board.update(left) is True: break
    print(board, '\n\n\n')
    if board.update(down) is True: break
    print(board, '\n\n\n')
