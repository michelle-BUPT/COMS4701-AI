import sys, time, resource
from heapq import heappush, heappop
from Queue import Queue

from collections import deque
# from heapq import heappush
# from heapq import heappop

move = {}
move[-3] = ('Up')
move[-1] = ('Left')
move[1] = ('Right')
move[3] = ('Down')

move_not = {}
move_not[-3] = (0, 1, 2)  # index cannot move up
move_not[-1] = (0, 3, 6)
move_not[1] = (2, 5, 8)
move_not[3] = (6, 7, 8)

direction = [-3, 3, -1, 1] # UDLR

def ram_usage():
    ram = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1000000.0
    return ram

class Solver(object):
    def __init__(self, init_state, solver):
        self.init_state = tuple(init_state)
        self.solver = solver

    def judge_solver(self):

        output = [[], 0, 0, 0, 0, 0]
        start = time.time()
        if self.solver == 'bfs':
            output = self.bfs(output)
        elif self.solver == 'dfs':
            output = self.dfs(output)
        else:
            output = self.ass(output)
        output[5] = time.time() - start


        self.saveResult(output)

    def bfs(self, output):

        frontier = Queue() # frontier represents nodes
        frontier.put(State(self.init_state, None, None)) # change to add a node into frontier
        explored = set()
        frontier_state = set()
        frontier_state.add(self.init_state)

        while frontier:
            node = frontier.get()
            explored.add(node.state)

            if self.goalTest(node):
                output[1] = len(explored) - 1
                output[2] = node.depth
                output[0] = node.recover() # parameter left
                return output

            for neighbors in node.get_neighbors():
                if neighbors.state not in explored and neighbors.state not in frontier_state:
                    frontier.put(neighbors)
                    frontier_state.add(neighbors.state)


            if neighbors is not None:
                output[3] = max(output[3], node.depth + 1)

            output[4] = max(output[4], ram_usage())

        return None

    def dfs(self, output):
        frontier = []
        frontier.append(State(self.init_state, None, None))
        explored = set() # frontier represents collections of states
        frontier_state = set()
        frontier_state.add(self.init_state)

        while frontier:
            node = frontier.pop()
            explored.add(node.state)

            if self.goalTest(node):
                output[1] = len(explored) - 1
                output[2] = node.depth # state.depth
                output[0] = node.recover() # parameter left
                return output


            for neighbors in node.get_neighbors()[::-1]:

                if neighbors.state not in explored and neighbors.state not in frontier_state:
                    frontier.append(neighbors)
                    frontier_state.add(neighbors.state)
                    output[3] = max(output[3], node.depth + 1) ## why cannot add afterwards?????
            # if expanded:
            #     output[3] = max(output[3], node.depth + 1)

            # if neighbors is not None:
            #     output[3] = max(output[3], node.depth + 1)
            output[4] = max(output[4], ram_usage())


        return None

    def ass(self, output):

        # frontier = [(0, State(self.init_state, None, None))]
        frontier = [[0, State(self.init_state, None, None)]]
        explored = set() # frontier represents collections of states
        frontier_state = {}
        # frontier_state[self.init_state] = frontier
        frontier_state[self.init_state] = [0, State(self.init_state, None, None)]
        # i = 0
        while frontier:
            # i += 1

            cost, node = heappop(frontier)
            explored.add(node.state)

            if self.goalTest(node):
                # output[1] = len(explored) - 1 #d##
                # output[1] =
                output[2] = node.depth # state.depth
                output[0] = node.recover() # parameter left
                # print ('ita: ' + str(i))
                return output

            expanded = False
            for neighbors in node.get_neighbors():

                expanded = True
                f = neighbors.depth + neighbors.manh_dist()
                if neighbors.state not in explored and neighbors.state not in frontier_state:
                    heappush(frontier, [f, neighbors])
                    output[3] = max(output[3], node.depth + 1)
                elif neighbors.state not in explored and neighbors.state in frontier_state:
                    frontier_pre = frontier_state[neighbors.state]
                    if frontier_pre[0] <= f:
                        continue
                    else:
                        # frontier.remove((frontier_pre[0], neighbors))
                        frontier.remove((frontier_pre[0], frontier_pre[1]))#still not correct????
                        heappush(frontier, [f, neighbors])

            if expanded:
                output[3] = max(output[3], node.depth + 1)
                output[1] += 1
            output[4] = max(output[4], ram_usage())

        return None


    def goalTest(self, node):
        goalState = tuple([0, 1, 2, 3, 4, 5, 6, 7, 8])
        if node.state == goalState:
            return True
        else:
            return False


    def saveResult(self, output):

        path = []
        for out in output[0]:
            path.append(move[out])

        path.reverse()
        output_file = open('output.txt','w')

        output_file.write("path_to_goal: " + str(path) + '\n')
        output_file.write("cost_of_path: " + str(len(output[0])) + '\n')
        output_file.write("nodes_expanded: " + str(output[1]) + '\n')
        output_file.write("search_depth: " + str(output[2]) + '\n')
        output_file.write("max_search_depth: " + str(output[3]) + '\n')
        output_file.write("running_time: " + str(output[5]) + '\n')
        output_file.write("max_ram_usage: " + str(output[4]) + '\n')

        output_file.close()

class State(object):

    def __init__(self, state, parent, move):
        self.state = tuple(state)
        self.parent = parent
        self.move = move
        self.depth = parent.depth + 1 if parent else 0

    def recover(self):

        path = []
        while self.parent is not None:
            path.append(self.move)
            self = self.parent
        return path


    def get_neighbors(self):
        pos_zero = self.state.index(0)
        neighbors = []
        for off in direction:
            if pos_zero not in move_not[off]:
                neighours_state = self.swap_tile(pos_zero, pos_zero + off)
                neighbors.append(State(tuple(neighours_state), self, off))
        return neighbors

    def manh_dist(self):
        dis = 0
        for inx, sta in enumerate(self.state):
            if inx == sta:
                continue
            dis += abs(sta - inx) / 3 + abs(sta - inx) % 3
        return dis

    def swap_tile(self, m, n):

        neighbors = list(self.state)
        # print (str(m) + ' ' + str(n))
        tmp = neighbors[m]
        neighbors[m] = neighbors[n]
        neighbors[n] = tmp
        return neighbors

if __name__ == '__main__':

    inputState = []
    for i in sys.argv[2].split(','):
        inputState.append(int(i))

    # inputState = [6,1,8,4,0,2,7,3,5]

    # solver = sys.argv[1]
    init_state = map(int, sys.argv[2].split(','))
    # solve = Solver(testcase, 'ass')
    solve = Solver(inputState, sys.argv[1])
    # solve = Solver(testcase, 'bfs')

    solve.judge_solver()
