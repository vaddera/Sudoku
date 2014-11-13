'''
Created on Nov 11, 2014

@author: vaddera, campbeeg
'''
# Defining Global Variables:
rows = 'ABCDEFGHI'
columns = '123456789'

# Shaping function:
def shape(A,B):
    return [a+b for a in A for b in B]

# Shaping Process:
squares = shape(rows, columns)
unitList = ([shape(rows, col) for col in columns] +
            [shape(row, columns) for row in rows] +
            [shape(row1, cols) for row1 in ('ABC', 'DEF', 'GHI') for cols in ('123', '456', '789')])

units = dict((square, [unit for unit in unitList if square in unit]) for square in squares)
peers = dict((square, set(sum(units[square],[])) - set([square])) for square in squares)

# Parsing a grid:
def parseGrid(grid):
    values = dict((square, columns) for square in squares)
    for square, d in gridValues(grid).items():
        if d in columns and not assign(values, square, d):
            return False #Fails if it can't assign d to a square
        return values
    
def gridValues(grid):
    chars = [col for col in grid if col in columns or col in '0.']
    assert len(chars) == 81
    return dict(zip(squares, chars))

# Constraint propagation:
def assign(values, square, d):
    otherValues = values[square].replace(d, '')
    if all(eliminate(values, square, d2) for d2 in otherValues):
        return values
    else:
        return False
    
def eliminate(values, square, d):
    
    if d not in values[square]:
        return values
    
    values[square] = values[square].replace(d, '')
    
    if len(values[square]) == 0:
        return False
    
    elif len(values[square]) == 1:
        d2 = values[square]
        
        if not all(eliminate(values, sqr, d2) for sqr in peers[square]):
            return False
        
    for i in units[square]:
        placed = [square for square in i if d in values[square]]
        
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
    
    if all(len(values[square]) == 1 for square in squares):
        return values
    
    n, square = min((len(values[square]), square) for square in squares if len(values[square]) > 1)
    return some(dfs(assign(values.copy(), square, d)) for d in values[square])

def some(seq):
    for i in seq:
        if i:
            return i
    return False
    
''' Main code: '''
grid1 = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
hardest = '85...24..72......9..4.........1.7..23.5...9...4...........8..7..17..........36.4.'
print '\n----------------- Solving random sequence --------------------\n'
display(gridValues(grid1))
display(solve(grid1))
print '----------------- Solving hardest sequence --------------------\n'
display(gridValues(hardest))
display(solve(hardest))