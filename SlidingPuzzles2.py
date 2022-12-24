from collections import deque
import time
import sys
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

final_output(sys.argv[1])
