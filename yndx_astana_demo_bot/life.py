import sys

import matplotlib

# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')

import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation
from matplotlib.colors import ListedColormap


class Ocean(object):
    _water = 0
    _stone = 1
    _fish = 2
    _shrimp = 3

    def __init__(self, array, rows_num, cols_num):
        self._array = array
        self._rows_num = rows_num
        self._cols_num = cols_num

    def _ind_ok(self, r, c):
        return r >= 0 and r < self._rows_num and c >= 0 and \
            c < self._cols_num

    def __str__(self):
        res = ''
        for i in range(self._rows_num):
            for j in self._array[i]:
                res += str(j) + ' '
            res += '\n'
        return res

    def _count_neighbors(self):
        fishes_num = [[0] * self._cols_num for j in range(self._rows_num)]
        shrimps_num = [[0] * self._cols_num for j in range(self._rows_num)]
        neighbor_r = [-1, -1, -1, 0, 0, 1, 1, 1]
        neighbor_c = [-1, 0, 1, -1, 1, -1, 0, 1]
        for i in range(self._rows_num):
            for j in range(self._cols_num):
                if self._array[i][j] == self._fish:
                    for k in range(8):
                        if self._ind_ok(i + neighbor_r[k], j + neighbor_c[k]):
                            fishes_num[i + neighbor_r[k]][j + neighbor_c[k]]\
                               += 1
                if self._array[i][j] == self._shrimp:
                    for k in range(8):
                        if self._ind_ok(i + neighbor_r[k], j + neighbor_c[k]):
                            shrimps_num[i + neighbor_r[k]][j + neighbor_c[k]]\
                               += 1
        return fishes_num, shrimps_num

    def upd(self):
        fishes_num, shrimps_num = self._count_neighbors()
        next_gen = [[0] * self._cols_num for j in range(self._rows_num)]
        for i in range(self._rows_num):
            for j in range(self._cols_num):
                if self._array[i][j] == self._stone:
                    next_gen[i][j] = self._stone
                if self._array[i][j] == self._fish:
                    if fishes_num[i][j] != 2 and fishes_num[i][j] != 3:
                        next_gen[i][j] = self._water
                    else:
                        next_gen[i][j] = self._fish
                if self._array[i][j] == self._shrimp:
                    if shrimps_num[i][j] != 2 and shrimps_num[i][j] != 3:
                        next_gen[i][j] = self._water
                    else:
                        next_gen[i][j] = self._shrimp
                if self._array[i][j] == self._water:
                    if fishes_num[i][j] == 3:
                        next_gen[i][j] = self._fish
                    else:
                        if shrimps_num[i][j] == 3:
                            next_gen[i][j] = self._shrimp
                        else:
                            next_gen[i][j] = self._water
        self._array = next_gen


def read_data():
    gen_num = int(sys.stdin.readline())
    rows_cols_num = sys.stdin.readline()
    rows_num, cols_num = rows_cols_num.split(' ')
    rows_num = int(rows_num)
    cols_num = int(cols_num)
    array = [[] for i in range(rows_num)]
    for i in range(rows_num):
        row = sys.stdin.readline()
        row = row.split(' ')
        for num in row:
            array[i].append(int(num))
    return gen_num, rows_num, cols_num, array



def get_val():
    x = np.random.uniform(100)
    if x <= 20:
        return 2
    if x <= 35:
        return 3
    if x <= 40:
        return 1
    return 0

def life_gif(fname, rows_num, cols_num, gen):
    rows_num = min(rows_num, 100)
    cols_num = min(cols_num, 100)
    gen= min(gen, 100)
    array = [[get_val() for j in range(rows_num)] for i in range(cols_num)]
    ocean = Ocean(array, rows_num, cols_num)
    
    def animate(hz):
        ocean.upd()
        sns.heatmap(ocean._array,cmap=ListedColormap(['#66b3ff','#00001a','#ff668f','#006600']), square=True, cbar=False)
    def init():
        sns.heatmap(ocean._array,cmap=ListedColormap(['#66b3ff','#00001a','#ff668f','#006600']), square=True, cbar=False)


    for i in range(50):
        ocean.upd()
        
    ocean = Ocean(array, rows_num, cols_num)

    fig, _ = plt.subplots(figsize=(20,20))

    ani = matplotlib.animation.FuncAnimation(fig, animate, init_func=init,  frames=gen)
    ani.save(fname, writer='imagemagick', fps=4)


if __name__ == '__main__':
    life_gif(sys.argv[1], 30, 30, 10)

