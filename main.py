import numpy as np
import random
import time
import math

goal = [[1,2,3],
        [4,5,6],
        [7,8,0]]
# start = np.arange(9)


class Puzzle8Board:

    def __init__(self):
        """initialise root instance"""
        # heuristic value
        self.hval = 0
        # current search depth
        self.depth = 0
        # parent node
        self.parent = None
        # puzzle current


        self.mat8 = [[1, 2, 3],
                     [4, 5, 6], 
                     [7, 8, 0]]
        # np.random.shuffle(start)
        # for i in range(3):
        #     for j in range(3):
        #         self.mat8[i][j] = start[i*3+j]
        # print self.mat8
        # print goal


    def __eq__(self, other):
        """ checks equality of the two puzzles (for goal check)"""
        if self.__class__ != other.__class__:
            return False
        else:
            return (self.mat8 == other.mat8)

    def __str__(self):
        """ string representation of the 8 puzzle object for print statement """
        strpuzz = ''
        for row in range(3):
            strpuzz += ' '.join(map(str, self.mat8[row])) + '\r\n'
        return strpuzz

    def newCopy(self):
        p = Puzzle8Board()
        for i in range(3):
            p.mat8[i] = self.mat8[i][:]
        return p
    
    def findval(self, puzzlemat, value):
        """returns row, col of the key in the graph"""
        if value < 0 or value > 8:
            raise Exception("value out of range")

        for row in range(3):
            for col in range(3):
                if puzzlemat[row][col] == value:
                    return row, col

    def getval(self, row, col):
        """returns the value at the specified row and column"""
        return self.mat8[row][col]

    def putval(self, row, col, value):
        """sets the value at the specified row and column"""
        self.mat8[row][col] = value

    def swap(self, pos_a, pos_b):
        """swaps values at the specified coordinates"""
        temp = self.getval(*pos_a)
        self.putval(pos_a[0], pos_a[1], self.getval(*pos_b))
        self.putval(pos_b[0], pos_b[1], temp)
    
    def nextMoves(self):
        """Returns a list of pieces which may move into free space"""
        
        movable = []
        # get row and column of the empty piece
        r, c = self.findval(self.mat8,0)
        
        # find which pieces can move there
        if c > 0:
            movable.append((r, c - 1))
        if r > 0:
            movable.append((r - 1, c))
        if c < 2:
            movable.append((r, c + 1))
        if r < 2:
            movable.append((r + 1, c))

        return movable

    def movePiece(self):
        """returns new board states after playing valid moves"""
        zero = self.findval(self.mat8,0)
        moveset = self.nextMoves()

        def swap_clone(a, b):     #required by lambda below
            p = self.newCopy()
            p.parent = self     ################
            p.depth = self.depth + 1
            p.swap(a,b)     #new copied puzzle with the move played.
            return p

        # return list of possible new states after moving.
        # map takes a lambda function which swaps the zero position with
        # the adjacent positions which are supplied as the iterable
        return map(lambda pair: swap_clone(zero, pair), moveset)     ################

    def finalPath(self, path):
        """recurse from goal state to original using parent"""
        if self.parent == None:
            return path
        else:
            path.append(self)
            return self.parent.finalPath(path)

    def aStar(self, h):
        """Performs A* search for goal state.
        h(puzzle) - heuristic function, returns an integer
        """
        def is_solved(puzzle):
            return puzzle.mat8 == goal

        def isalreadyvisited(item, list1):
            """Returns -1 for non-found index value of the list"""
            if item in list1:
                return list1.index(item)
            else:
                return -1


        openl = [self]
        closedl = []
        moves = 0

        while len(openl) > 0:
            
            x = openl.pop(0)
            moves += 1  #popping means exploring 1 state = 1 move
            
            if (is_solved(x)):  #GOAL CHECK
                if len(closedl) > 0:
                    return x.finalPath([]), moves
                else:
                    return [x], moves

            succ = x.movePiece()
            idx_open = idx_closed = -1

            for move in succ:
                # Check if node already visited
                idx_open = isalreadyvisited(move, openl)
                idx_closed = isalreadyvisited(move, closedl)

                hval = h(move)  #heuristic value for the move
                fval = hval + move.depth    #path cost

                if idx_closed == -1 and idx_open == -1:
                    move.hval = hval
                    openl.append(move)

                elif idx_open > -1:
                    copy = openl[idx_open]
                    if fval < copy.hval + copy.depth:
                        # copy move's values over existing
                        copy.hval = hval
                        copy.parent = move.parent
                        copy.depth = move.depth

                elif idx_closed > -1:
                    copy = closedl[idx_closed]
                    if fval < copy.hval + copy.depth:
                        move.hval = hval
                        closedl.remove(copy)
                        openl.append(move)

            #append best move to the path list
            closedl.append(x)   
            #sort the queue
            openl = sorted(openl, key=lambda p: p.hval + p.depth)

        # if finished state not found, return failure
        return [],0

    def shuffle(self, steps):
        for i in range(steps):
            r, c = self.findval(self.mat8,0)
            movable = self.nextMoves()
            target = random.choice(movable)
            self.swap((r, c), target)            



def heur(puzzle, item_total_calc, total_calc):
    """
    Heuristic template 
    Takes as input the current Puzzle8Board object and 2 functions defined by the specific heuristic:
    1) item_total_calc - takes 4 parameters: current row, current col, target row, target col. 
    2) total_calc - takes 1 parameter, the sum of item_total_calc over all entries. 
    This is the value of the heuristic function
    """
    t = 0
    for row in range(3):
        for col in range(3):
            val = puzzle.getval(row,col)
            trow,tcol = puzzle.findval(goal,val)
            t += item_total_calc(row, col, trow, tcol)

    return total_calc(t)

#some heuristic functions, the best being the standard manhattan distance in this case, as it comes
#closest to maximizing the estimated distance while still being admissible.


def h_approx(puzzle):
    return 0

def h_manhattan(puzzle):
    return heur(puzzle,
                lambda r, c, tr, tc: abs(tr - r) + abs(tc - c),
                lambda t : t)

def h_euclidean(puzzle):
    return heur(puzzle,
                lambda r, c, tr, tc: (tr - r)**2 + (tc - c)**2,
                lambda t: math.sqrt(t))

def h_chebyshev(puzzle):
    return heur(puzzle,
            lambda r, c, tr, tc: max(abs(tr - r) ,abs(tc - c)),
            lambda t: t)


   
def main():
    puzzle8 = Puzzle8Board()
    n = 15
    print "for",n,"shuffles:"
    puzzle8.shuffle(n)
    print puzzle8
    # fo.write(puzzle8.__str__())

    start = time.clock()
    path, n_states = puzzle8.aStar(h_approx)
    # path.reverse()
    # for i in path: 
    #     print i   
    print "Approximation h=0, Djikstra heuristic, explored", n_states, "states and took t =", (time.clock() - start), "s"
    # st = str(("Approximation h=0, Djikstra heuristic, explored", n_states, "states and took t =", (time.clock() - start), "s"))
    # fo.write(st)
    # fo.write(("\n"))


    start = time.clock()
    path, n_states = puzzle8.aStar(h_euclidean)
    # path.reverse()
    # for i in path: 
    #     print i
    print "Euclidean distance heuristic explored", n_states, "states and took t =", (time.clock() - start), "s"
    # st = str(("Euclidean distance heuristic explored", n_states, "states and took t =", (time.clock() - start), "s"))
    # fo.write(st)
    # fo.write(("\n"))

    start = time.clock()
    path, n_states = puzzle8.aStar(h_chebyshev)
    # path.reverse()
    # for i in path: 
    #     print i
    print "Chebyshev distance heuristic explored", n_states, "states and took t =", (time.clock() - start), "s"
    # st = str(("Chebyshev distance heuristic explored", n_states, "states and took t =", (time.clock() - start), "s"))
    # fo.write(st)
    # fo.write(("\n"))

    start = time.clock()
    path, n_states = puzzle8.aStar(h_manhattan)
    # path.reverse()
    # for i in path: 
    #     print i
    print "Manhattan distance heuristic explored", n_states, "states and took t =", (time.clock() - start), "s"
    # st = str(("Manhattan distance heuristic explored", n_states, "states and took t =", (time.clock() - start), "s"))
    # fo.write(st)
    # fo.write(("\n\n"))

   

if __name__ == "__main__":
    # fo = open("exampleresult.txt","w") 
    # for i in range(50):
    main()
    # fo.close()
