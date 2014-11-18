'''
Created on Nov 11, 2014

@author: vaddera, campbeeg
'''

def shape(A, B):
    lst = []
    for a in A:
        for b in B:
            lst.append(a + b)
    return lst

cols = '123456789'
rows = 'ABCDEFGHI'
squares = shape(rows, cols)

lst = []

for c in cols:
    lst.append(shape(rows, c))
for r in rows:
    lst.append(shape(r, cols))
for r1 in ('ABC', 'DEF', 'GHI'):
    for c1 in ('123', '456', '789'):
        lst.append(shape(r1, c1))

unitList = lst

units = dict()
peers = dict()
for s in squares:
    temp = []
    for u in unitList:
        if s in u:
            temp.append(u)
    units[s] = temp
    peers[s] = set(sum(units[s], [])) - set([s])

def parseGrid(grid):
    values = dict()
    for s in squares:
        values[s] = cols
    for s, d in gridValues(grid).items():
        if d in cols and not assign(values, s, d):
            return False
    return values

def gridValues(grid):
    chars = []
    for c in grid:
        if c in cols or c in '0.':
            chars.append(c)
    
    if len(chars) == 81:
        print 'Sudoku string length pass.'
    else:
        print 'Error: Sudoku string length failure.'
    return dict(zip(squares, chars))

def assign(values, s, d):
    other_values = values[s].replace(d, '')
    
    for d2 in other_values:
        if not eliminate(values, s, d2):
            return False
    return values
    
def eliminate(values, s, d):
    if d not in values[s]:
        return values
    values[s] = values[s].replace(d, '')
    
    if len(values[s]) == 0:
        return False
    elif len(values[s]) == 1:
        d2 = values[s]
        for s2 in peers[s]:
            if not eliminate(values, s2, d2):
                return False  
    
    for u in units[s]:
        dplaces = []
        for s in u:
            if d in values[s]:
                dplaces.append(s)
                
        if len(dplaces) == 0:
            return False 
        elif len(dplaces) == 1:
            
            if not assign(values, dplaces[0], d):
                return False
    return values


def display(values):
    w = []
    for s in squares:
        w.append(len(values[s]))
    width = 1 + max(w)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print ''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in cols)
        if r in 'CF': print line
    print

def solve(grid):
    return dfs(parseGrid(grid))
    
def dfs(values):
    
    if values is False:
        return False
    
    temp = []
    for square in squares:
        temp.append(len(values[square]) == 1)
    if all(temp):
        return values
    
    lst = []
    for square in squares:
        if len(values[square]) > 1:
            lst.append((len(values[square]), square))
    n, square = min(lst)
    
    tmp = []
    for d in values[square]:
        tmp.append(dfs(assign(values.copy(), square, d)))
    
    return some(tmp)
    

def some(seq):
    for e in seq:
        if e: return e
    return False

''' Main Code: '''

# Puzzles
grid1 = '003020600900305001001806400008102900700000008006708200002609500800203009005010300'
grid2 = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
hardest = '85...24..72......9..4.........1.7..23.5...9...4...........8..7..17..........36.4.'

# Solving Puzzles
display(gridValues(grid1))
display(solve(grid1))
display(gridValues(grid2))
display(solve(grid2))
display(gridValues(hardest))
display(solve(hardest))

print 'Terminated.'