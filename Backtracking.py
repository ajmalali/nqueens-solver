import time
from random import randint


# returns the NxN board list
def createBoard(size):
    return [['_'] * size for row in range(size)]


# displays the board
def displayBoard(assignments, size):
    if not assignments:
        print "No solution found!"
        return

    board = createBoard(size)

    for i, j in assignments:
        board[i][j] = 'Q'

    for row in board:
        for i in row:
            print str(i) + '  ',
        print "\n"


"""
Using the idea of equation of line: y = mx + b.
m is always 1. We just check if every queen's position
is on the main diagonal line, other diagonal line
and same column
"""
def isSafe(x, y, assignments):
    for i, j in assignments:
        if (i, j) != (x, y):
            if (y + x == j + i) or (y - x == j - i):
                return False
            elif j == y:
                return False

    return True

# returns a list of domain values for a given row
def getDomain(assignments, row, domains):
    values = []
    for col in domains[row]:
        if isSafe(row, col, assignments):
            values.append(col)

    return values


# returns updated domains based on current assignments
# and a boolean for notifying empty domains. If any domain
# becomes empty, returns an empty list False.
# Also reutrns the row with minimum remaining domains (if specified). If multiple
# rows have minimum domains, returns first one.
def updateDomains(assignments, domains, unassigned, n, mrv=False):
    minsize = 9999
    newdomains = {}
    nextrow = len(assignments)
    list = []

    for i in unassigned:
        values = getDomain(assignments, i, domains)
        if len(values) == 0:
            return {}, True, nextrow
        newdomains[i] = values

        if mrv:
            size = len(values)
            if size == minsize:
                list.append(i)
            if size < minsize:
                nextrow = i
                minsize = size
                del list[:]

    if len(list) != 0:
        index = randint(0, len(list)-1)
        nextrow = list[index]

    return newdomains, False, nextrow


# backtracking algorithm without any filtering or ordering
def backtracking(assingments, row, n):
    # If all queens are placed, we are done
    if len(assignments) == n:
        return assignments

    # check every column for a given row
    for col in range(n):
        assingments.add((row, col))

        if isSafe(row, col, assingments) and backtracking(assingments, row+1, n) != None:
            return assignments

        assingments.remove((row, col))

    return None


# backtracking algorithm with forward checking
def backtrackingFC(assignments, domains, unassigned, row, n):
    # If all queens are placed, we are done
    if len(assignments) == n:
        return assignments

    # iterate over columns for a given row
    for col in domains[row]:
        assignments.add((row, col))
        unassigned.remove(row)

        newdomains, isempty, nextrow = updateDomains(assignments, domains, unassigned, n)

        if not isempty:
            if backtrackingFC(assignments, newdomains, unassigned, row + 1, n) != None:
                return assignments

        assignments.remove((row, col))
        unassigned.add(row)

    return None


# backtracking algorithm with forward checking and MRV
def backtrackingFCMRV(assignments, domains, unassigned, row, n):
    # If all queens are placed, we are done
    if len(assignments) == n:
        return assignments

    # iterate over columns for a given row
    for col in domains[row]:
        assignments.add((row, col))
        unassigned.remove(row)

        newdomains, isempty, nextrow = updateDomains(assignments, domains, unassigned, n, True)

        if not isempty:
            if backtrackingFCMRV(assignments, newdomains, unassigned, nextrow, n) != None:
                return assignments

        assignments.remove((row, col))
        unassigned.add(row)

    return None


# returns a dictionary of domains and
# a set of unassigned rows
def init(n):
    domains = {}
    unassigned = set()
    for i in range(n):
        unassigned.add(i)
        values = []
        for j in range(n):
            values.append(j)

        domains[i] = values

    return domains, unassigned



if __name__ == '__main__':
    iteration = 1

    while iteration == 1:
        try:
            n = input("Enter the Number of Queens: ")

            assignments = set()
            domains, unassigned = init(n)

            print("\n1. Backtracking Only")
            print("2. Backtracking with Forward Checking")
            print("3. Backtracking with MRV (Minimum Remaining Values)")
            menu = input("\nEnter 1, 2 or 3: ")

            if menu == 1:
                currentTime = time.time()
                assignments = backtracking(assignments, 0, n)
                timeElapsed = time.time() - currentTime
            elif menu == 2:
                currentTime = time.time()
                assignments = backtrackingFC(assignments, domains, unassigned, 0, n)
                timeElapsed = time.time() - currentTime
            elif menu == 3:
                currentTime = time.time()
                assignments = backtrackingFCMRV(assignments, domains, unassigned, 0, n)
                timeElapsed = time.time() - currentTime
            else:
                print("Restart. Enter 1, 2 or 3")

            print "Solution Found, Total Time Taken: " + str(timeElapsed)

            display = input("Enter 1 to display solution or 0 to continue: ")
            if display:
                print ""
                displayBoard(assignments, n)
                print ""

            iteration = input("Again? Press 1 to retry or 0 to exit: ")

        except (ValueError, NameError), e:
           print "Invalid input; Try again.\n"
