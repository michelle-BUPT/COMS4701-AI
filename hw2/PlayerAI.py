from random import randint
from BaseAI import BaseAI

import time
import Grid
import math

'''
1. timeout
2. get_neighbors not considered when neighbor is null
3. Best weight to be found
4. terminal states?
'''

INF = float('inf')
MAXDEPTH = 100
class PlayerAI(BaseAI):

    def __init__(self):
        self.startTime = 0;
        self.maxDepth = 0;

    def getMove(self, grid):
        self.startTime = time.clock()

        alpha = -INF
        beta = INF

        for self.maxDepth in xrange(MAXDEPTH):
            tmp_child = self.maximize(grid, alpha, beta, 0)[0]
            # tmp_move = self.maximize(grid, alpha, beta, 0)[0][0]
            tmp_move = tmp_child[0] if tmp_child is not None else None
            if self.timeUP():
                break
            best_move = tmp_move if tmp_move is not None else best_move

        return best_move

    def maximize(self, grid, alpha, beta, depth):
        if self.timeUP():
            return None, -INF

        if depth > self.maxDepth: #Terminal test waited to be finished
            return None, self.get_heuristic(grid)

        maxChild, maxUtility = None, -INF

        for child in self.get_children(grid):
            utility = self.minimize(child[1], alpha, beta, depth + 1)[1]

            if utility > maxUtility:
                maxChild, maxUtility = child, utility

            if maxUtility >= beta:
                break

            if maxUtility > alpha:
                alpha = maxUtility

        return maxChild, maxUtility

    def minimize(self, grid, alpha, beta, depth):
        if self.timeUP():
            return None, -INF

        if depth > self.maxDepth:#Terminal test waited to be finished
            return None, self.get_heuristic(grid)

        minChild, minUtility = None, INF

        for cell in grid.getAvailableCells():

            grid_v2 = grid.clone()
            grid_v4 = grid.clone()

            grid_v2.setCellValue(cell, 2)
            grid_v4.setCellValue(cell, 4)

            utility_v2 = self.maximize(grid_v2, alpha, beta, depth + 1)[1]
            utility_v4 = self.maximize(grid_v4, alpha, beta, depth + 1)[1]

            utility = utility_v2 * 0.9 + utility_v4 * 0.1

            if utility < minUtility:
                # minChild, minUtility = child, utility
                minUtility = utility

            if minUtility <= alpha:
                break;

            if minUtility <  beta:
                beta = minUtility

        return minChild, minUtility

    def timeUP(self):
        if time.clock() - self.startTime > 0.2:
            return True
        else:
            return False


    def get_children(self, grid):
        children = []

        for direction in range(4):
            gridCopy = grid.clone()

            if gridCopy.move(direction): # Returns true or False
                children.append((direction, gridCopy))

        return children


    def get_heuristic(self, grid):
        size = 4
        diff_row = [0.0] * size
        diff_col = [0.0] * size

        smoothness = 1.0
        freeTiles, smoothness, gridValue = 0, 0, []

        weight_mono = 1.0
        weight_smoo = 1.0
        weight_free = 1.0
        weight_max_gridValue = 1.0
        weight_aver = 1.0

        for i in range(size):
            for j in range(size):
                if grid.map[i][j] == 0:
                    freeTiles += 1
                else:
                    gridValue.append(grid.map[i][j])

            for j in range(size - 1):
                diff_row_each = grid.map[i][j + 1] - grid.map[i][j]
                # diff_row[i] += diff_row_each / abs(diff_row_each)
                if diff_row_each == 0:
                    smoothness += 1
                else:
                    smoothness += -math.log(abs(diff_row_each), 2)
                    diff_row[i] += diff_row_each / abs(diff_row_each)

                diff_col_each = grid.map[j + 1][i] - grid.map[j][i]
                # diff_col[i] += diff_col_each / abs(diff_col_each)
                if diff_col_each == 0:
                    smoothness += 1
                else:
                    smoothness += -math.log(abs(diff_col_each), 2)
                    diff_col[i] += diff_col_each / abs(diff_col_each)

        max_gridValue = math.log(max(gridValue), 2)
        aver_gridValue = math.log(sum(gridValue) / float(len(gridValue)), 2)

        # monotonicity = sum(map(abs, diff_row)) * max_gridValue + sum(map(abs, diff_col)) * max_gridValue
        monotonicity = sum(map(abs, diff_row)) + sum(map(abs, diff_col))
        return weight_mono * monotonicity + weight_smoo * smoothness + weight_free * freeTiles \
            + weight_max_gridValue * max_gridValue + weight_aver * aver_gridValue


# if __name__ == '__main__':
