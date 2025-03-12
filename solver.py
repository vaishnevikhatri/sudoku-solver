"""
each puzzle is 9x9, all rows, columns, and 3x3 boxes must have unique numbers, no repeats. 

"""
import time
def isValid(grid): #look up what a set and or counter is or use dictionary
    #tracks numbers alr seen
    # for rows
    for i in range(len(grid)):
        numbersAlrSeen = []
        for j in range(len(grid[i])):
            currentNum = grid[i][j]
            if currentNum == 0:
                continue
            if currentNum in numbersAlrSeen: #is it equal to anything we've seen?
                return False
            numbersAlrSeen.append(currentNum)
          #row valid
    # for columns
    #f
    for j in range(len(grid)):
        numbersAlrSeen = []
        for i in range(len(grid)):
            currentNum = grid[i][j]
            if currentNum == 0:
                continue
            if currentNum in numbersAlrSeen: #is it equal to anything we've seen?
                return False
            numbersAlrSeen.append(currentNum)
    #subgrid checking code check (0,0; 0,1; 0,2; 1,0; 1,1; 1,2; 2,0; 2,1; 2,2)
    for startI in range(0,9,3):
        for startJ in range(0, 9, 3):
            numbersAlrSeen = []
            for di in range(3):
                for dj in range(3):
                    i = startI + di
                    j = startJ + dj
                    currentNum = grid[i][j]
                    if currentNum == 0:
                        continue
                    if currentNum in numbersAlrSeen:
                        return False
                    numbersAlrSeen.append(currentNum)
    return True
    
def isSolved(grid):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            currentNum = grid[i][j]
            if currentNum == 0:
                return False
    return isValid(grid)

def printGrid(grid):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            print(grid[i][j], end="")
        print()
#grid solver
numSolveGrids = 0
def solveGrid(grid):
    excecutionTime = 0
    startTime = time.time()
    global numSolveGrids
    numSolveGrids += 1
    # find the first empty slot
    emptySlot = 0
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            currentNum = grid[i][j]
            if currentNum == 0:
                emptySlot = (i,j)
                break
        if emptySlot != 0:
            break
    if emptySlot == 0:
        return isSolved(grid)
    if not isValid(grid):
        return False
    
    # determine valid candidates
    candidates = set()
    for x in range(1,10):
        candidates.add(x)
    rowEmptySlot = emptySlot[0]
    columnEmptySlot = emptySlot[1]
    for j in range(9):
        currentNum = grid[rowEmptySlot][j]
        candidates.discard(currentNum)
    for i in range(9):
        currentNum = grid[i][columnEmptySlot]
        candidates.discard(currentNum)
    #check subgrid and remove candidates
    startRow = (rowEmptySlot // 3) * 3
    startCol = (columnEmptySlot // 3) * 3
    for dR in range(3):
        for dC in range(3):
            row = startRow + dR
            col = startCol + dC
            candidates.discard(grid[row][col])
    # for candidate in candidates
    for candidate in candidates:
    # put candidate in slot
        grid[rowEmptySlot][columnEmptySlot] = candidate
    # recursivley call solveGrid (solved or unsolved)
        if solveGrid(grid):
    # if solved, return true
            return True
    # once out of loop, clear the most recently changed slot, return false after changing slot
        grid[rowEmptySlot][columnEmptySlot] = 0
        endTime = time.time()
        executionTime = endTime - startTime

def solveGridMRV(grid):
    global numSolveGrids
    numSolveGrids += 1
    # find the first empty slot
    minCandidateSlot = None
    minNumCandidates = None
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            currentNum = grid[i][j]
            if currentNum == 0:
                emptySlot = (i,j)
                candidateSet = findCandidates(grid, emptySlot)
                numCandidates = len(candidateSet)
                if minNumCandidates is None or numCandidates < minNumCandidates:
                    minNumCandidates = numCandidates
                    minCandidateSlot = emptySlot
    if minCandidateSlot is None:
        return isSolved(grid)
    if not isValid(grid):
        return False
    
    # determine valid candidates
    candidates = findCandidates(grid,minCandidateSlot)
    # for candidate in candidates
    rowEmptySlot = minCandidateSlot[0]
    columnEmptySlot = minCandidateSlot[1]
    for candidate in candidates:
        # put candidate in slot
        grid[rowEmptySlot][columnEmptySlot] = candidate
        # recursivley call solveGrid (solved or unsolved)
        if solveGridMRV(grid):
        # if solved, return true
            return True
        # once out of loop, clear the most recently changed slot, return false after changing slot
        grid[rowEmptySlot][columnEmptySlot] = 0
    return False
def findCandidates(grid, emptySlot):
    candidates = set()
    for x in range(1,10):
        candidates.add(x)
    rowEmptySlot = emptySlot[0]
    columnEmptySlot = emptySlot[1]
    for j in range(9):
        currentNum = grid[rowEmptySlot][j]
        candidates.discard(currentNum)
    for i in range(9):
        currentNum = grid[i][columnEmptySlot]
        candidates.discard(currentNum)
    #check subgrid and remove candidates
    startRow = (rowEmptySlot // 3) * 3
    startCol = (columnEmptySlot // 3) * 3
    for dR in range(3):
        for dC in range(3):
            row = startRow + dR
            col = startCol + dC
            candidates.discard(grid[row][col])
    return candidates
def solveAndReportData(grid, mrv = False):
    global numSolveGrids
    numSolveGrids = 0
    ableToSolve = False
    startTime = time.time()

    if mrv:
        ableToSolve = solveGridMRV(grid)
    else:
        ableToSolve = solveGrid(grid)
    numStates = numSolveGrids
    endTime = time.time()
    totalTime = endTime - startTime
    return {"time": totalTime, "states" : numStates, "ableToSolve": ableToSolve, "solvedPuzzle": grid}