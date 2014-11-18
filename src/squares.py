'''
Created on Nov 11, 2014

@author: vaddera, campbeeg
'''
import time

# Defining Global Variables:
rows = 'ABCDEFGHI'
columns = '123456789'

# Shaping function:
def shape(A,B):
    lst = []
    for a in A:
        for b in B:
            lst.append(a + b)
    return lst

# Shaping Process:
squares = shape(rows, columns)
lst = []

for col in columns:
    lst.append(shape(rows, col))
for row in rows:
    lst.append(shape(row, columns))
for row1 in ('ABC', 'DEF', 'GHI'):
    for cols in ('123', '456', '789'):
        lst.append(shape(row1, cols))

unitList = lst

units = dict((square, [unit for unit in unitList if square in unit]) for square in squares)
peers = dict((square, set(sum(units[square],[])) - set([square])) for square in squares)

# Parsing a grid:
def parseGrid(grid):
    lst = []
    for square in squares:
        lst.append((square, columns))
    values = dict(lst)
    for square, d in gridValues(grid).items():
        if d in columns and not assign(values, square, d):
            return False #Fails if it can't assign d to a square
        return values
    
def gridValues(grid):
    chars = []
    for col in grid:
        if col in columns or col in '0.':
            chars.append(col)
    assert len(chars) == 81
    return dict(zip(squares, chars))

# Constraint propagation:
def assign(values, square, d):
    otherValues = values[square].replace(d, '')
    
    for d2 in otherValues:
        if not eliminate(values, square, d2):
            return False
    return values
    
def eliminate(values, square, d):
    
    if d not in values[square]:
        return values
    
    values[square] = values[square].replace(d, '')
    
    if len(values[square]) == 0:
        return False
    
    elif len(values[square]) == 1:
        d2 = values[square]
        for sqr in peers[square]:
            if not eliminate(values, sqr, d2):
                return False
        
    for i in units[square]:
        placed = []
        
        for square in i:
            if d in values[square]:
                placed.append(square)
        
        if len(placed) == 0:
            return False
        elif len(placed) == 1:
            if not assign(values, placed[0], d):
                return False
        
    return values

# Displays grids:
def display(values):
    width = 1 + max(len(values[square]) for square in squares)
    line = '+'.join(['-' * (width * 3)] * 3)
    
    for row in rows:
        print ''.join(values[row + col].center(width) + ('|' if col in '36' else '') for col in columns)
        if row in 'CF':
            print line
    print
    
# Depth First Search sequence:
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
    for i in seq:
        if i:
            return i
    return False
    

def solved(values):
    "A puzzle is solved if each unit is a permutation of the digits 1 to 9."
    def unitsolved(unit): return set(values[s] for s in unit) == set(columns)
    return values is not False and all(unitsolved(unit) for unit in unitList)
    
def solve_all(grids, name='', showif=0.0):
    """Attempt to solve a sequence of grids. Report results.
    When showif is a number of seconds, display puzzles that take longer.
    When showif is None, don't display any puzzles."""
    def time_solve(grid):
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
    times, results = zip(*[time_solve(grid) for grid in grids])
    N = len(grids)
    if N > 1:
        print "Solved %d of %d %s puzzles (avg %.2f secs (%d Hz), max %.2f secs)." % (
            sum(results), N, name, sum(times)/N, N/sum(times), max(times))
    
''' Main code: '''
if __name__ == '__main__':

    grid1 = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
    hardest = '85...24..72......9..4.........1.7..23.5...9...4...........8..7..17..........36.4.'

    solve_all(grid1.split(), "grid1", None)
    solve_all(hardest.split(), "hardest", None)


'''
print '\n----------------- Solving random sequence --------------------\n'
display(gridValues(grid1))
display(solve(grid1))
print '----------------- Solving hardest sequence --------------------\n'
display(gridValues(hardest))
display(solve(hardest))
'''