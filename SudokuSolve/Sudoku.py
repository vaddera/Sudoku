def sameRow(i,j): 
    return (i/9 == j/9)

def sameColumn(i,j): 
    return (i-j) % 9 == 0

def sameBlock(i,j): 
    return (i/27 == j/27 and i%9/3 == j%9/3)

def solve(a):
    i = a.find('.')
    if i == -1:
        printGrid(a)
        return

    excludedNumbers = set()
    for j in range(81):
        if sameRow(i,j) or sameColumn(i,j) or sameBlock(i,j):
            excludedNumbers.add(a[j])

    for m in '123456789':
        if m not in excludedNumbers:
            solve(a[:i]+m+a[i+1:])

def printGrid(a):
    k = 0
    for i in range(1, 12):
        for j in range(1, 12):
            if i % 4 == 0:
                print '-',
            else:
                if j % 4 == 0:
                    print '|',
                else:
                    print a[k],
                    k = k + 1
        print

if __name__ == '__main__':
    filename = file('hardest.txt').read().strip().split('\n')

    for fil in filename:
        printGrid(fil)
        print
        solve(fil)
        print