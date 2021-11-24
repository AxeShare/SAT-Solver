import pycosat
import sys, getopt 
import time

def main(argv): 
    argument = '' 
    try:
        opts, args = getopt.getopt(argv,"emhvb",["easy","medium","hard","evil","blank","help"])
    except getopt.GetoptError:
        sys.exit(2)
    
    for opt, arg in opts: 
        if opt in ("--help"):
            help()
        elif opt in ("-e", "--easy"): 
            solve_problem(easy) 
        elif opt in ("-m", "--medium"): 
            solve_problem(medium) 
        elif opt in ("-h", "--hard"):
            solve_problem(hard) 
        elif opt in ("-v", "--evil"):
            solve_problem(evil) 
        elif opt in ("-b", "--blank"):
            solve_problem(blank) 
        else:
            help()
            sys.exit()
            

def solve_problem(problemset):
    print('Problem:') 
    pprint(problemset)  
    solve(problemset) 
    print('Answer:')
    pprint(problemset)  
    
def v(i, j, d): 
    return 81 * (i - 1) + 9 * (j - 1) + d

#Reduces Sudoku problem to a SAT clauses 
def sudoku_clauses(): 
    res = []
    # for all cells, ensure that the each cell:
    for i in range(1, 10):
        for j in range(1, 10):
            # denotes (at least) one of the 9 digits (1 clause)
            res.append([v(i, j, d) for d in range(1, 10)])
            # does not denote two different digits at once (36 clauses)
            for d in range(1, 10):
                for dp in range(d + 1, 10):
                    res.append([-v(i, j, d), -v(i, j, dp)])

    def valid(cells): 
        for i, xi in enumerate(cells):
            for j, xj in enumerate(cells):
                if i < j:
                    for d in range(1, 10):
                        res.append([-v(xi[0], xi[1], d), -v(xj[0], xj[1], d)])

    # ensure rows and columns have distinct values
    for i in range(1, 10):
        valid([(i, j) for j in range(1, 10)])
        valid([(j, i) for j in range(1, 10)])
        
    # ensure 3x3 sub-grids "regions" have distinct values
    for i in 1, 4, 7:
        for j in 1, 4 ,7:
            valid([(i + k % 3, j + k // 3) for k in range(9)])
      
    assert len(res) == 81 * (1 + 36) + 27 * 324
    return res

def solve(grid):
    #solve a Sudoku problem
    clauses = sudoku_clauses()
    for i in range(1, 10):
        for j in range(1, 10):
            d = grid[i - 1][j - 1]
            # For each digit already known, a clause (with one literal). 
            if d:
                clauses.append([v(i, j, d)])
    
    # Print number SAT clause  
    numclause = len(clauses)
    print ("CNF " + str(numclause) +"(number of clauses)")
    # print(clauses)
    # solve the SAT problem
    start = time.time()
    sol = set(pycosat.solve(clauses))
    end = time.time()
    print("Time: "+str(end - start))
    
    def read_cell(i, j):
        # return the digit of cell i, j according to the solution
        for d in range(1, 10):
            if v(i, j, d) in sol:
                return d

    for i in range(1, 10):
        for j in range(1, 10):
            grid[i - 1][j - 1] = read_cell(i, j)


if __name__ == '__main__':
    from pprint import pprint

    easy = [[0, 0, 0, 1, 0, 9, 4, 2, 7],
            [1, 0, 9, 8, 0, 0, 0, 0, 6],
            [0, 0, 7, 0, 5, 0, 1, 0, 8],
            [0, 5, 6, 0, 0, 0, 0, 8, 2],
            [0, 0, 0, 0, 2, 0, 0, 0, 0],
            [9, 4, 0, 0, 0, 0, 6, 1, 0],
            [7, 0, 4, 0, 6, 0, 9, 0, 0],
            [6, 0, 0, 0, 0, 8, 2, 0, 5],
            [2, 9, 5, 3, 0, 1, 0, 0, 0]]
        
    medium = [[5, 8, 0, 0, 0, 1, 0, 0, 0],
            [0, 3, 0, 0, 6, 0, 0, 7, 0],
            [9, 0, 0, 3, 2, 0, 1, 0, 6],
            [0, 0, 0, 0, 0, 0, 0, 5, 0],
            [3, 0, 9, 0, 0, 0, 2, 0, 1],
            [0, 5, 0, 0, 0, 0, 0, 0, 0],
            [6, 0, 2, 0, 5, 7, 0, 0, 8],
            [0, 4, 0, 0, 8, 0, 0, 1, 0],
            [0, 0, 0, 1, 0, 0, 0, 6, 5]]

    evil = [[0, 2, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 6, 0, 0, 0, 0, 3],
            [0, 7, 4, 0, 8, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 3, 0, 0, 2],
            [0, 8, 0, 0, 4, 0, 0, 1, 0],
            [6, 0, 0, 5, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 7, 8, 0],
            [5, 0, 0, 0, 0, 9, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 4, 0]]

    hard = [[0, 2, 0, 0, 0, 0, 0, 3, 0],
            [0, 0, 0, 6, 0, 1, 0, 0, 0],
            [0, 6, 8, 2, 0, 0, 0, 0, 5],
            [0, 0, 9, 0, 0, 8, 3, 0, 0],
            [0, 4, 6, 0, 0, 0, 7, 5, 0],
            [0, 0, 1, 3, 0, 0, 4, 0, 0],
            [9, 0, 0, 0, 0, 7, 5, 1, 0],
            [0, 0, 0, 1, 0, 4, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 9, 0]]
    
    blank = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]]
    
    if(len(sys.argv[1:]) == 0):
        print('Argument error, check --help')
    else:
        main(sys.argv[1:])