from collections import deque
import time
import sys

def print_puzzle(size, board):
    x = 0
    for i in range(0, len(board), size):
        print(board[i: i + size])


def find_goal(board):
    board = board.replace('.', '')
    temp = sorted(board)
    str1 = ''.join(sorted(temp))
    return str1.strip() + '.'


def print_boards_and_goals():
    with open("slide_puzzle_tests.txt") as f:
        for line in f:
            print("This is the unsorted version: ")
            print_puzzle(int(line[0]), line[2:].strip())
            print("This is the sorted version: ")
            print_puzzle(int(line[0]), find_goal(line[2:]))


def print_boards_goals_children():
    x = 0
    with open("slide_puzzle_tests.txt") as f:
        for line in f:
            line = line.strip()
            print("Line " + str(x) + " start state: ")
            print_puzzle(int(line[0]), line[2:].strip())
            print("Line " + str(x) + " goal state: ")
            print_puzzle(int(line[0]), find_goal(line[2:]))
            print("Line " + str(x) + " children: ")
            children = get_children(line[2:])
            for child in children:
                if child is not None:
                  print("Child #" + str(children.index(child)) + ":")
                  print_puzzle(int(line[0]), child)

            print('')
            x = x + 1


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


def bfs_number_of_goal_states(board):
    start = find_goal(board)
    fringe = deque()
    visited = set()
    fringe.append(start)
    visited.add(start)
    while len(fringe) > 0:
        v = fringe.pop()
        children = get_children(v)
        for child in children:
            if child is not None and child not in visited:
                fringe.append(child)
                visited.add(child)
    return len(visited)


def bfs_shortest_path(board):
    fringe = deque()
    visited = set()
    parent = None
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


def bfs_shortest_path_steps(board):
    fringe = deque()
    visited = set()
    parent = None
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
            return path
        children = get_children(v)
        for child in children:
            if child is not None and child not in visited:
                fringe.append(child)
                visited.add(child)
                dictionary[child] = parent #This is correct
    return None


def bfs_shortest_path_moves(board):
    fringe = deque()
    visited = set()
    dictionary = {board: None}  #State:Parent
    moves = {}
    fringe.append(board)
    visited.add(board)
    while len(fringe) > 0:
        v = fringe.popleft()
        parent = v
        if goal_test(v):
            key = v
            path = []
            while key is not None:
                if key != board:
                    path.append(moves[key])
                key = dictionary[key]
            return path
        children = get_children(v)
        for child in children:
            if child is not None and child not in visited:
                fringe.append(child)
                visited.add(child)
                dictionary[child] = parent #This is correct
                if children[0] == child:
                    moves[child] = 'Up'
                if children[1] == child:
                    moves[child] = 'Down'
                if children[2] == child:
                    moves[child] = 'Left'
                if children[3] == child:
                    moves[child] = 'Right'
    return None


def print_shortest_path_steps(board):
    size = int(len(board) ** .5)
    shortest_path = bfs_shortest_path_steps(board)
    for i in range(len(shortest_path) - 1, -1, -1):
        print_puzzle(size, shortest_path[i])
        print('')


def print_moves(board):
    moves = bfs_shortest_path_moves(board)
    for i in range(len(moves) - 1, -1, -1):
        print(moves[i])
    print('')


def hardest_eight_puzzle():
    start = '12345678.'
    fringe = deque()
    visited = set()
    dictionary = {start: None}  # State:Parent
    fringe.append(start)
    visited.add(start)
    while len(fringe) > 0:
        v = fringe.popleft()
        parent = v
        children = get_children(v)
        for child in children:
            if child is not None and child not in visited:
                fringe.append(child)
                visited.add(child)
                dictionary[child] = parent
    parents = set(dictionary.values())
    hardest_puzzles = []
    for x in dictionary:
        if x not in parents:
            hardest_puzzles.append(x)
    #for y in hardest_puzzles:
    #   print(str(bfs_shortest_path(y)))
    p = bfs_shortest_path(hardest_puzzles[-1])
    really_hardest_puzzles = []
    for i in range(len(hardest_puzzles) - 1, -1, -1):
        if bfs_shortest_path(hardest_puzzles[i]) == p:
            really_hardest_puzzles.append(hardest_puzzles[i])
        else:
            return really_hardest_puzzles
    return len(hardest_puzzles)


def dfs_shortest_path(board):
    fringe = deque()
    visited = set()
    parent = None
    dictionary = {board:None}  #State:Parent
    fringe.append(board)
    visited.add(board)
    while len(fringe) > 0:
        v = fringe.pop()
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

def hardest_eight_puzzle_analysis():
    size = 3
    hardest_puzzles = hardest_eight_puzzle()
    for i in hardest_puzzles:
        print_puzzle(3, i)
        print('')
        print('The solution length is: ' + str(bfs_shortest_path(i)))
        print('The solution boards are: ')
        print_shortest_path_steps(i)


def dfs_bfs_comparison(board):
    start = time.perf_counter()
    x = dfs_shortest_path(board)
    end = time.perf_counter()
    print("The shortest DFS path is: " + str(x) + ' moves, and takes ' + str(end - start) + ' seconds')
    start = time.perf_counter()
    x = bfs_shortest_path(board)
    end = time.perf_counter()
    print("The shortest BFS path is: " + str(x) + ' moves, and takes ' + str(end - start) + ' seconds')


def final_output(filename):
    x = 0
    with open(filename) as f:
        for line in f:
            start = time.perf_counter()
            b = bfs_shortest_path(line[2:].strip())
            end = time.perf_counter()
            elapsed = end - start
            print('Line '+ str(x) + ': ' + line[2:].strip() + ', ' + str(b) + ' moves found in ' + str(elapsed) + ' seconds')
            x = x + 1


def bibfs_is_the_devil(board):
    goal = find_goal(board)
    source_fringe = deque()
    goal_fringe = deque()
    left_visited = set()
    right_visited = set()
    source_fringe.append((board, 0))
    goal_fringe.append((goal, 0))
    left_visited.add(board) #Make two visited sets
    right_visited.add(goal)
    left_depth, right_depth = 0, 0
    right_dictionary = {goal:0}
    left_dictionary = {board:0}

    while source_fringe and goal_fringe: #Left or right depth can be up to 1 OFF! Figure out a better way of handling the two depths!
        if source_fringe:
            v, left_depth = source_fringe.popleft()
            if goal_test(v) or v in right_visited:
                return left_dictionary[v] + right_dictionary[v]
            children = get_children(v)
            for child in children:
                if child is not None and child not in left_visited:
                    source_fringe.append((child, left_depth + 1))
                    left_visited.add(child)
                    left_dictionary[child] = left_depth + 1
        if goal_fringe:
            v, right_depth = goal_fringe.popleft()
            if v == board or v in left_visited:
                return left_dictionary[v] + right_dictionary[v]
            children = get_children(v)
            for child in children:
                if child is not None and child not in right_visited:
                    goal_fringe.append((child, right_depth + 1))
                    right_visited.add(child)
                    right_dictionary[child] = right_depth + 1
    return None


def bibfs_bfs_comparison(filename):
    x = 0
    with open(filename) as f:
        for line in f:
            start = time.perf_counter()
            b = bfs_shortest_path(line[2:].strip())
            end = time.perf_counter()
            elapsed = end - start
            print('BFS: Line '+ str(x) + ': ' + line[2:].strip() + ', ' + str(b) + ' moves found in ' + str(elapsed) + ' seconds')
            s = time.perf_counter()
            b = bibfs_is_the_devil(line[2:].strip())
            e = time.perf_counter()
            elapsed = e - s
            print('BIBFS: Line ' + str(x) + ': ' + line[2:].strip() + ', ' + str(b) + ' moves found in ' + str(elapsed) + ' seconds')
            x = x + 1
# print_boards_and_goals() #Purely for testing
#print_boards_goals_children() #This is for my first signature

#print("The number of 2x2 solvable puzzles is: " + str(bfs_number_of_goal_states('ABC.'))) #These are for my second signature
#print("The number of 3x3 solvable puzzles is: " + str(bfs_number_of_goal_states('12345678.'))) #Second signature


# print(str("The shortest path length of the board is: " + str(bfs_shortest_path('.82314657')))) #These are for my third signature
# print("The correct sequence of moves is: ")
# print_moves('.82314657')
# print("The sequence of goal states is: ")
# print_shortest_path_steps('.82314657')

#hardest_eight_puzzle_analysis() #This is for my fourth signature

#dfs_bfs_comparison('.82314657') #This is for my last signature

#print(str(bfs_shortest_path('FABCE.HIDJKGMNOPLRSTUQVWX')))

#final_output(sys.argv[1])
bibfs_bfs_comparison(sys.argv[1])