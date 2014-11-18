'''
Created on Nov 11, 2014

@author: vaddera, campbeeg
'''

import time

def shape(A, B):
    return [a+b for a in A for b in B]

cols   = '123456789'
rows     = 'ABCDEFGHI'
squares  = shape(rows, cols)

lst = []

for c in cols:
    lst.append(shape(rows, c))
for r in rows:
    lst.append(shape(r, cols))
for r1 in ('ABC', 'DEF', 'GHI'):
    for c1 in ('123', '456', '789'):
        lst.append(shape(r1, c1))

unitList = lst

units = dict((s, [u for u in unitList if s in u])
             for s in squares)
peers = dict((s, set(sum(units[s],[]))-set([s]))
             for s in squares)

def parseGrid(grid):
    values = dict((s, cols) for s in squares)
    for s,d in gridValues(grid).items():
        if d in cols and not assign(values, s, d):
            return False
    return values

def gridValues(grid):
    chars = [c for c in grid if c in cols or c in '0.']
    
    if len(chars) == 81:
        print 'Sudoku string length pass.'
    else:
        print 'Error: Sudoku string length failure.'
    return dict(zip(squares, chars))

def assign(values, s, d):
    other_values = values[s].replace(d, '')
    if all(eliminate(values, s, d2) for d2 in other_values):
        return values
    else:
        return False

def eliminate(values, s, d):
    if d not in values[s]:
        return values
    values[s] = values[s].replace(d,'')
    
    if len(values[s]) == 0:
        return False
    elif len(values[s]) == 1:
        d2 = values[s]
        if not all(eliminate(values, s2, d2) for s2 in peers[s]):
            return False
    
    for u in units[s]:
        dplaces = [s for s in u if d in values[s]]
        if len(dplaces) == 0:
            return False 
        elif len(dplaces) == 1:
            
            if not assign(values, dplaces[0], d):
                return False
    return values


def display(values):
    width = 1+max(len(values[s]) for s in squares)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print ''.join(values[r+c].center(width)+('|' if c in '36' else '')
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
    
    return some(dfs(assign(values.copy(), square, d)) for d in values[square])
    

def some(seq):
    for e in seq:
        if e: return e
    return False

'''Ethan, please take a look on the function below. I would like to remove the time calculation.'''

def solution(grids, name='', showif=0.0):
    """Attempt to solve a sequence of grids. Report results.
    When showif is a number of seconds, display puzzles that take longer.
    When showif is None, don't display any puzzles."""
    def timeSolve(grid):
        start = time.clock()
        values = solve(grid)
        t = time.clock()-start
        ## Display puzzles that take long enough
        #if showif is not None and t > showif:
        if 1==1:
            display(gridValues(grid))
            if values: display(values)
            print '(%.2f seconds)\n' % t
        return (t, solved(values))
    times, results = zip(*[timeSolve(grid) for grid in grids])
    N = len(grids)
    if N > 1:
        print "Solved %d of %d %s puzzles (avg %.2f secs (%d Hz), max %.2f secs)." % (
            sum(results), N, name, sum(times)/N, N/sum(times), max(times))

def solved(values):
    def unitsolved(unit): return set(values[s] for s in unit) == set(cols)
    return values is not False and all(unitsolved(unit) for unit in unitList)

''' Main Code: '''

# Puzzles
grid1  = '003020600900305001001806400008102900700000008006708200002609500800203009005010300'
grid2  = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
hard1  = '.....6....59.....82....8....45........3........6..3.54...325..6..................'
hardest = '85...24..72......9..4.........1.7..23.5...9...4...........8..7..17..........36.4.'

# Solving Puzzles
solution(grid1.split(), "grid1", None)
solution(grid2.split(), "grid2", None)
solution(hard1.split(), "hard1", None)
solution(hardest.split(), "hardest", None)
print 'Terminated.'
