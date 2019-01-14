import time
from random import randint


# returns the NxN board list
def createBoard(size):
    return [['_'] * size for row in range(size)]


# displays the board
def displayBoard(queenslist, size):
    board = createBoard(size)

    for i, j in queenslist:
        board[i][j] = 'Q'

    for row in board:
        for i in row:
            print str(i) + '  ',
        print "\n"


# initializes the board with with random queen assingments
def init(n):
    list = set()
    for i in range(n):
        position = randint(0, n - 1)
        list.add((i, position))
    return list


"""
Using the idea of equation of line: y = mx + b.
m is always 1. We just check if every queen's position
is on the main diagonal line, other diagonal line
and same column
"""


def getConflicts(x, y, queenslist):
    odiagonal = y + x
    mdiagonal = y - x
    conflict = 0
    for i, j in queenslist:
        if (i, j) != (x, y):
            if abs(i - x) == abs(j - y):
                conflict += 1
            elif j == y:
                conflict += 1

    return conflict


# returns random conflicted queen
def getQueen(conflictedQueens, n):
    index = randint(0, len(conflictedQueens) - 1)
    return conflictedQueens[index]


# returns the position (column) with the least conflicts.
# if multiple columns have same least conflict, returns a random column
def getMinConflicts(queen, queenslist):
    minconflict = 99999
    pos = (0, 0)
    list = []

    for col in range(n):
        if queen[1] != col:
            conflict = getConflicts(queen[0], col, queenslist)
            if conflict == minconflict:
                list.append((queen[0], col))
            elif conflict < minconflict:
                minconflict = conflict
                pos = (queen[0], col)
                del list[:]

    if len(list) != 0:
        index = randint(0, len(list) - 1)
        pos = list[index]

    return pos


# updates position of the queen
def changePosition(queen, position, queenslist):
    queenslist.remove(queen)
    queenslist.add(position)


# returns a list of conflicted queens
def getConflictedList(queenslist):
    list = []
    for i, j in queenslist:
        conflict = getConflicts(i, j, queenslist)
        if conflict != 0:
            list.append((i, j))

    return list


if __name__ == '__main__':
    iterations = 1

    while iterations == 1:
        try:
            n = input("Enter the number of queens: ")

            queenslist = init(n)
            conflictedQueens = getConflictedList(queenslist)

            while len(conflictedQueens) != 0:
                queen = getQueen(conflictedQueens, n)
                position = getMinConflicts(queen, queenslist)
                changePosition(queen, position, queenslist)
                conflictedQueens = getConflictedList(queenslist)

            print "Solution found!"

            display = input("Enter 1 to display solution or 0 to continue: ")
            if display:
                print ""
                displayBoard(queenslist, n)
                print ""

            iterations = input("Again? Press 1 to retry or 0 to exit: ")

        except (ValueError, NameError), e:
            print "Invalid input; Try again.\n"
