from collections import deque
import time
import sys
import random
from heapq import heappush, heappop

def print_puzzle(size, board):
    x = 0
    for i in range(0, len(board), size):
        print(board[i: i + size])


def find_goal(board):
    board = board.replace('.', '')
    temp = sorted(board)
    str1 = ''.join(sorted(temp))
    return str1.strip() + '.'


def swap(board, index1, index2):
    board = list(board)
    board[index1], board[index2] = board[index2], board[index1]
    return ''.join(board)


def get_children(board):
    index = board.index('.')
    size = int(len(board) ** .5)
    row, col = index_to_coords(index, size)
    children = [None, None, None, None]
    if row > 0: #If I can move up
        swap_index = coords_to_index(row - 1, col, size) #The string index of the character I need to swap with
        children[0] = swap(board, index, swap_index)
    if row < size - 1: #If I can move down
        swap_index = coords_to_index(row + 1, col, size)
        children[1] = swap(board, index, swap_index)
    if col > 0: #If I can move left
        swap_index = coords_to_index(row, col - 1, size)
        children[2] = swap(board, index, swap_index)
    if col < size - 1: #If I can move right
        swap_index = coords_to_index(row, col + 1, size)
        children[3] = swap(board, index, swap_index)
    return children


def coords_to_index(row, col, size):
    index = row * size + col
    return index


def index_to_coords(index, size):
    row = index // size
    col = index % size
    return row, col


def goal_test(state):
    return state == find_goal(state)


def bfs_shortest_path(board):
    fringe = deque()
    visited = set()
    dictionary = {board:None}  #State:Parent
    fringe.append(board)
    visited.add(board)
    while len(fringe) > 0:
        v = fringe.popleft()
        parent = v
        if goal_test(v):
            key = v
            path = []
            while key is not None:
                path.append(key)
                key = dictionary[key]
            return len(path) - 1
        children = get_children(v)
        for child in children:
            if child is not None and child not in visited:
                fringe.append(child)
                visited.add(child)
                dictionary[child] = parent #This is correct
    return None


def parity_check(board):
    temp = board[:board.index('.')] + board[board.index('.') + 1:]
    score = 0
    for elem1 in temp:
        for elem2 in temp[temp.index(elem1) + 1:]: #So as to avoid duplicate worl
            if elem2 < elem1:
                score = score + 1
    return score


def solvable(board):
    size = int(len(board) ** .5)
    score = parity_check(board)
    if size % 2 != 0:
        return (score % 2 == 0)
    else:
        row, col = index_to_coords(board.index('.'), size)
        if row % 2 == 0:
            return (score % 2 != 0)
        else:
            return (score % 2 == 0)

def check_solvability(filename):
    with open(filename) as f:
        for line in f:
            print(str(solvable(line[2:].strip())))


#check_solvability('slide_puzzle_tests.txt')

def kDFS(board, k):
    fringe = []
    fringe.append((board, 0, {board}))
    while len(fringe) > 0:
        state, depth, ancestors = fringe.pop()
        if goal_test(state):
            return depth
        if depth < k:
            children = get_children(state)
            for child in children:
                if child is not None and child not in ancestors:
                    new_depth = depth + 1
                    new_ancestors = ancestors.union([child])
                    fringe.append((child, new_depth, new_ancestors))
    return None

def final_output(filename):
    with open(filename) as f:
        x = 0
        for line in f:
            line = line.strip()
            board = line[2:-2]
            search = line[-1]
            j = time.perf_counter()
            if not solvable(board):
                i = time.perf_counter()
                print('Line ' + str(x) + ': ' + board + ', ' + 'no solution determined in ' + str(i - j) + ' seconds')
            elif search == 'B':
                start = time.perf_counter()
                b = bfs_shortest_path(board)
                end = time.perf_counter()
                print('Line ' + str(x) + ': ' + board + ', ' + 'BFS - ' + str(b) + ' moves in ' + str(end - start) + ' seconds')
            elif search == 'I':
                start = time.perf_counter()
                b = id_dfs(board)
                end = time.perf_counter()
                print('Line ' + str(x) + ': ' + board + ', ' + 'ID-DFS - ' + str(b) + ' moves in ' + str(end - start) + ' seconds')
            elif search == 'A':
                start = time.perf_counter()
                b = A_star(board)
                end = time.perf_counter()
                print('Line ' + str(x) + ': ' + board + ', ' + 'A* - ' + str(b) + ' moves in ' + str(end - start) + ' seconds')
            elif search == '!':
                start = time.perf_counter()
                b = bfs_shortest_path(board)
                end = time.perf_counter()
                print('Line ' + str(x) + ': ' + board + ', ' + 'BFS - ' + str(b) + ' moves in ' + str(end - start) + ' seconds')
                start = time.perf_counter()
                b = id_dfs(board)
                end = time.perf_counter()
                print('Line ' + str(x) + ': ' + board + ', ' + 'ID-DFS - ' + str(b) + ' moves in ' + str(end - start) + ' seconds')
                start = time.perf_counter()
                b = A_star(board)
                end = time.perf_counter()
                print('Line ' + str(x) + ': ' + board + ', ' + 'A* - ' + str(b) + ' moves in ' + str(end - start) + ' seconds')
            print()
            x = x + 1


def id_dfs(board):
    k = 0
    while kDFS(board, k) is None:
        k = k + 1
    return k



def taxicab(board):
    total = 0
    size = int(len(board) ** .5)
    goal = find_goal(board)
    for char in board:
        if char != '.':
            row, col = index_to_coords(board.index(char), size)
            goalrow, goalcol = index_to_coords(goal.index(char), size)
            temp = abs(row - goalrow) + abs(col - goalcol)
            total += temp
    return total

# print(str(taxicab('GBCDEFAHIJKLMNO.')))
# print(str(taxicab('ABEDCFGHIJKLMNO.')))

def A_star(start):
    closed = set()
    fringe = [(taxicab(start), start, 0)]
    while len(fringe) > 0:
        heuristic, state, depth = heappop(fringe)
        if(goal_test(state)):
            return depth
        if state not in closed:
            closed.add(state)
            children = get_children(state)
            for child in children:
                if child is not None:
                    new_depth = depth + 1
                    new_f = new_depth + taxicab(child)
                    heappush(fringe, (new_f, child, new_depth))
    return None
#This is my work for extension A
def weighted_A_star(start, weight):
    closed = set()
    fringe = [(taxicab(start), start, 0)]
    while len(fringe) > 0:
        heuristic, state, depth = heappop(fringe)
        if(goal_test(state)):
            return depth
        if state not in closed:
            closed.add(state)
            children = get_children(state)
            for child in children:
                if child is not None:
                    new_depth = depth + 1
                    new_f = weight * new_depth + taxicab(child)
                    heappush(fringe, (new_f, child, new_depth))
    return None

def A_output(filename, weight):
    with open(filename) as f:
        x = 0
        for line in f:
            if 20 <= x <= 30:
                # start = time.perf_counter()
                # b = A_star(line.strip())
                # end = time.perf_counter()
                # # print("Line: " + str(x) + ",  A* - " + line.strip() + ', ' + str(b) + " moves found in " + str(end - start) + " seconds")
                # #print("Weight 1: " + str(b) + "   " + str(end - start))
                start = time.perf_counter()
                b = weighted_A_star(line.strip(), weight)
                end = time.perf_counter()
                # print("Line: " + str(x) + ",  Weighted A* (" + str(weight) + ") - " + line.strip() + ', ' + str(b) + " moves found in " + str(end - start) + " seconds")
                #print("Weight " + str(weight) + ': '  + str(b) + "   " + str(end - start))
                print(str(b) + "   " + str(end - start))
            x = x + 1

#A_output(sys.argv[1], .5)

#This is my code for part B
def weighted_random_tie_breaker_A_star(start, weight):
    closed = set()
    fringe = [(taxicab(start), random.random(), start, 0, "")]
    while len(fringe) > 0:
        heuristic, tie, state, depth, path = heappop(fringe)
        if(goal_test(state)):
            return depth, path
        if state not in closed:
            closed.add(state)
            children = get_children(state)
            x = 0
            for child in children:
                if child is not None:
                    tie = random.random()
                    new_depth = depth + 1
                    new_f = weight * new_depth + taxicab(child)
                    if x == 0:
                        new_path = path + 'U'
                    if x == 1:
                        new_path = path + 'D'
                    if x == 2:
                        new_path = path + 'L'
                    if x == 3:
                        new_path = path + 'R'
                    heappush(fringe, (new_f, tie, child, new_depth, new_path))
                    x = x + 1
    return None


def B_output(filename, weight):
    with open(filename) as f:
        x = 0
        for line in f:
            if x == 41:
                for x in range(0, 10):
                    start = time.perf_counter()
                    b, p = weighted_random_tie_breaker_A_star(line.strip(), weight)
                    end = time.perf_counter()
                    print(str(b) + "   " + str(end - start))
                    print(p)
            x = x + 1

#B_output(sys.argv[1], .7)

#This is my code for extension C - I apologize for all the 'D's in the names
def A_star_modded_heuristic(start):
    closed = set()
    fringe = [(D_heuristic(start), start, 0)]
    while len(fringe) > 0:
        heuristic, state, depth = heappop(fringe)
        if(goal_test(state)):
            return depth
        if state not in closed:
            closed.add(state)
            children = get_children(state)
            for child in children:
                if child is not None:
                    new_depth = depth + 1
                    new_f = new_depth + D_heuristic(child)
                    heappush(fringe, (new_f, child, new_depth))
    return None

def A_star_modded_2_heuristic(start):
    closed = set()
    fringe = [(D2_heuristic(start), start, 0)]
    while len(fringe) > 0:
        heuristic, state, depth = heappop(fringe)
        if(goal_test(state)):
            return depth
        if state not in closed:
            closed.add(state)
            children = get_children(state)
            for child in children:
                if child is not None:
                    new_depth = depth + 1
                    new_f = new_depth + D2_heuristic(child)
                    heappush(fringe, (new_f, child, new_depth))
    return None


def D_heuristic(board):
    size = int(len(board) ** .5)
    goal = "ABCDEFGHIJKLMNO."
    total = taxicab(board)
    if total < 2:
        if board[-1] != goal[len(board) - size] and board[-1] != goal[len(board) - 1]:
            total += 2
    return total


def D2_heuristic(board):
    total = 0
    problem_index = []
    size = int(len(board) ** .5)
    goal = find_goal(board)
    for char in board:
        if char != '.':
            row, col = index_to_coords(board.index(char), size)
            goalrow, goalcol = index_to_coords(goal.index(char), size)
            temp = abs(row - goalrow) + abs(col - goalcol)
            if temp > 1:
                problem_index.append(temp)
            total += temp
        if sum(problem_index) < 25: #25, 20, 30, 50, 60, 40
            total += 2
    return total

def D_output(filename):
    with open(filename) as f:
        x = 0
        for line in f:
            if x < 38:
                start1 = time.perf_counter()
                b1 = A_star(line.strip())
                end1 = time.perf_counter()
                #print("Regular h(x): " + str(b) + "   " + str(end - start))
                #start2 = time.perf_counter()
                #b2 = A_star_modded_heuristic(line.strip())
                #end2 = time.perf_counter()
                #print("Modded (last - checked) h(x): " + str(b) + "   " + str(end - start))
                start3 = time.perf_counter()
                b3 = A_star_modded_2_heuristic(line.strip())
                end3 = time.perf_counter()
                #print("Modded (weighted wrong moves) h(x): " + str(b) + "   " + str(end - start))
                difference = abs((end3 - start3) - (end1 - start1))
                if (end3 - start3) < (end1 - start1):
                    print(str(b3) + " Modded faster by: " + str(difference) + " seconds")
                else:
                    print(str(b3) + " Regular faster by: " + str(difference) + " seconds")
            x = x + 1
#D_output(sys.argv[1])

#This is my code for extension D
def c_bfs_shortest_path(board):
    nodes = 0
    fringe = deque()
    visited = set()
    dictionary = {board:None}  #State:Parent
    fringe.append(board)
    visited.add(board)
    while len(fringe) > 0:
        v = fringe.popleft()
        nodes = nodes + 1
        parent = v
        if goal_test(v):
            key = v
            path = []
            while key is not None:
                path.append(key)
                key = dictionary[key]
            return len(path) - 1, nodes
        children = get_children(v)
        for child in children:
            if child is not None and child not in visited:
                fringe.append(child)
                visited.add(child)
                dictionary[child] = parent #This is correct
    return None

def c_kDFS(board, k):
    nodes = 0
    fringe = []
    fringe.append((board, 0, {board}))
    while len(fringe) > 0:
        state, depth, ancestors = fringe.pop()
        nodes = nodes + 1
        if goal_test(state):
            return depth, nodes
        if depth < k:
            children = get_children(state)
            for child in children:
                if child is not None and child not in ancestors:
                    new_depth = depth + 1
                    new_ancestors = ancestors.union([child])
                    fringe.append((child, new_depth, new_ancestors))
    return None, nodes

def c_id_dfs(board):
    k = 0
    nodes = 0
    x, temp = c_kDFS(board, k)
    while x is None:
        nodes = nodes + temp
        k = k + 1
        x, temp = c_kDFS(board, k)
    return k, nodes

def c_A_star(start):
    nodes = 0
    closed = set()
    fringe = [(taxicab(start), start, 0)]
    while len(fringe) > 0:
        heuristic, state, depth = heappop(fringe)
        nodes = nodes + 1
        if(goal_test(state)):
            return depth, nodes
        if state not in closed:
            closed.add(state)
            children = get_children(state)
            for child in children:
                if child is not None:
                    new_depth = depth + 1
                    new_f = new_depth + taxicab(child)
                    heappush(fringe, (new_f, child, new_depth))
    return None

def C_output(filename):
    with open(filename) as f:
        x = 0
        for line in f:
            if x <= 17: # or == 20
                start = time.perf_counter()
                a, b = c_bfs_shortest_path(line.strip())
                end = time.perf_counter()
                print(str(a) + " moves in " + str(end - start) + " seconds. BFS processes " + str(b/(end - start)) + ' nodes per second')
                start = time.perf_counter()
                a, b = c_id_dfs(line.strip())
                end = time.perf_counter()
                print(str(a) + " moves in " + str(end - start) + " seconds. ID-DFS processes " + str(b/(end - start)) + ' nodes per second')
                start = time.perf_counter()
            if x == 40: #or == 40
                a, b = c_A_star(line.strip())
                end = time.perf_counter()
                print(str(a) + " moves in " + str(end - start) + " seconds. A* processes " + str(b/(end - start)) + ' nodes per second')
            x = x + 1

C_output(sys.argv[1])
#A_output(sys.argv[1], -9 * 10 ** 100)