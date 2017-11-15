import itertools, pickle as cPickle,bisect
from operator import itemgetter
import time,math
start_time = time.time()
class Node:
    def __init__(self, region,count,fruit):
        self.region = region
        self.count = count
        self.fruit = fruit
    def __lt__(self, other):
        return self.count > other.count

def get_move(board,n,p,remaining_time):
    v, action= max_value(board, float("-inf"),float("inf"),n,p,min_score,max_score,0)
    return action,result(board,action),v


def max_value(state, alpha, beta,n,p,min_score, max_score,depth):
    if cutoff(state,depth):
        return util(state,min_score,max_score)
    v = float("-inf")
    max_move = None
    hash_key = hash(str(state))
    try:
        actions = actions_map[hash_key]
    except:
        actions = getActions(state,n,p)
        actions_map[hash_key] = actions
    for action in actions:
        temp_move = None
        val, move = min_value(result(state,action),alpha,beta,n,p,min_score,max_score+pow(action.count,2),depth+1)
        if val > v:
            v = val
            temp_move = action
        if v>= beta:
            return v,action
        if v > alpha:
            alpha = v
            max_move = temp_move
    return v, max_move

def min_value(state, alpha, beta,n,p,min_score,max_score,depth):
    if cutoff(state,depth):
        return util(state,min_score,max_score)
    v = float("inf")
    min_move = None
    hash_key = hash(str(state))
    try:
        actions = actions_map[hash_key]
    except:
        actions = getActions(state,n,p)
        actions_map[hash_key] = actions
    for action in actions:
        temp_move = None
        val, move = max_value(result(state,action),alpha,beta,n,p,min_score+pow(action.count,2),max_score,depth+1)
        if val < v:
            v = val
            temp_move = action
        if v <= alpha:
            return v, action
        if v < beta:
            beta = v
            min_move = temp_move
    return v, min_move

def util(state,min_score,max_score):
    return max_score - min_score,state

def getActions(state,n,p):
    actions = []
    for i in fruits.keys():
        actions = getPossibleRegions(state,i,n,actions)
    return actions

def getPossibleRegions(state,fruit,n,actions):
    l= []
    visited = [[False for j in range(n)]for i in range(n)]
    for i in range(n):
        for j in range(n):
            if state[i][j] == fruit and not visited[i][j]:
                l = [(i,j)]
                getRegion(state, i, j, visited ,fruit,l)
                node = Node(l,len(l),fruit)
                bisect.insort_left(actions, node)
    return actions

def getRegion(state, i, j, visited ,fruit,l):
    visited[i][j] = True
    for k in range(4):
        if hasSameFruit(state, i + rows[k], j + cols[k],visited,fruit):
            l.append((i + rows[k], j + cols[k]))
            getRegion(state, i + rows[k], j + cols[k],visited,fruit,l)


def hasSameFruit(state, row, col,visited,fruit):
    return (row >= 0) and (row < n) and (col >= 0) and (col < n) and (state[row][col] == fruit and not visited[row][col])


def cutoff(state,depth):
    if remaining_time <= time.time()-start_time+0.5:
        return True
    if depth == DEPTH:
        return True
    if all(x == '*' for x in itertools.chain(*state)):
        return True
    return False

def result(state,action):
    new_state = cPickle.loads(cPickle.dumps(state, -1))
    action.region.sort(key=itemgetter(0, 1))
    for coord in action.region:
        x = coord[0]
        y = coord[1]
        while x > 0:
            new_state[x][y], new_state[x-1][y] = new_state[x-1][y], new_state[x][y]
            x -= 1
        new_state[x][y] = '*'
    return new_state



rows = [-1, 0, 0, 1]
cols = [ 0, -1, 1, 0]
max_score = 0
fruits = {}
actions_map = {}
min_score = 0
with open('input.txt') as input_file:
    n = int(input_file.readline().rstrip('\n'))
    p = int(input_file.readline().rstrip('\n'))
    remaining_time = float(input_file.readline().rstrip('\n'))
    board = []
    total_fruits = 0
    for line in input_file:
        line = line.rstrip('\n')
        row = []
        for x in list(line):
            if x !='*':
                total_fruits +=1
                x = int(x)
                if x in fruits:
                    fruits[x] = fruits[x]+1
                else:
                    fruits[x] = 1
            row.append(x)
        board.append(row)
    actions_map[hash(str(board))] = getActions(board,n,p)
    num_of_regions = len(actions_map[hash(str(board))])
    DEPTH = min(5,math.ceil(((remaining_time*total_fruits*2)/(num_of_regions*n*n*len(fruits)))))
    if DEPTH == 1 or DEPTH == 2:
        DEPTH = DEPTH+1

with open('output.txt', 'w') as output_file:
    move, board,v = get_move(board,n,p,remaining_time)
    move.region.sort(key=itemgetter(0, 1))
    output_file.write(chr(move.region[0][1]+65)+str(move.region[0][0]+1)+'\r\n')
    for line in board:
        output_file.write(''.join(map(str,line))+'\r\n')
