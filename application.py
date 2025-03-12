from flask import Flask
from flask import render_template
from flask import request

import solver

app = Flask(__name__)

# it should show a user input to put in the puzzle
# it should have a submit button
# submit button will send the user input to solver
# solver will solve the puzzle using MRV, regular
# solver will show the results for each one and the time taken/states explored

PRESET_PUZZLE_1 = """009420060
070905302
500003090
000801020
260000051
018200400
380004019
094030685
021008030"""
PRESET_PUZZLE_2 = """200000000
107400003
300200050
005020000
060100400
000007000
000003008
800600200
040800031"""
PRESET_PUZZLE_3 = """800000000
003600000
070090200
050007000
000045700
000100030
001000068
008500010
090000400"""

@app.route("/")
def index():
    return render_template("index.html", PRESET_PUZZLE_1=PRESET_PUZZLE_1, PRESET_PUZZLE_2=PRESET_PUZZLE_2, PRESET_PUZZLE_3=PRESET_PUZZLE_3)

def isValidPuzzle(puzzleString):
    puzzleString = puzzleString.strip().split()
    if len(puzzleString) != 9:
        return False
    for line in puzzleString:
        if len(line) != 9:
            return False

        for letter in line:
            if letter not in "0123456789":
                return False
    return True

# take a string and return a 2d array
def parsePuzzle(puzzleString):
    puzzleData = puzzleString.strip().split()
    outputPuzzle = [[0 for _ in range(9)] for _ in range(9)]
    for i in range(len(puzzleData)):
        for j in range(len(puzzleData[i])):
            outputPuzzle[i][j] = int(puzzleData[i][j])
    return outputPuzzle

# take a 2d array and return an html string
def renderPuzzle(rawPuzzle):
    outputString = ""
    for i in range(len(rawPuzzle)):
        if i > 0 and i % 3 == 0:
            outputString += "-" * 11
            outputString += "<br>"
        for j in range(len(rawPuzzle[i])):
            if j > 0 and j % 3 == 0:
                outputString += "|"
            outputString += str(rawPuzzle[i][j]) if (rawPuzzle[i][j] != 0) else "x"
        outputString += "<br>"
    return outputString

@app.route("/solve", methods=['GET', 'POST'])
def solve():
    if request.method == "POST":
        puzzleData = request.form["puzzle"]
        if not isValidPuzzle(puzzleData):
            return "not a valid puzzle"

        puzzleData = parsePuzzle(puzzleData)
        regularResults = solver.solveAndReportData(puzzleData, mrv=False)
        mrvResults = solver.solveAndReportData(puzzleData, mrv=True)

        """
        results: {
            "time": amount of time taken,
            "states": number of states explored,
            "ableToSolve": whether we were able to solve
            "solvedPuzzle": string containing solved puzzle, return original array if unsolved
        }
        """

        regularResults["solvedPuzzle"] = renderPuzzle(regularResults["solvedPuzzle"])
        mrvResults["solvedPuzzle"] = renderPuzzle(mrvResults["solvedPuzzle"])

        return render_template("results.html", regularResults=regularResults, mrvResults=mrvResults)

if __name__ == "__main__":
    app.run()
