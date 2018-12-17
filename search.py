# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """    
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    found = False
    graph = Graph()
    graph.CreateGraph((100,100))
    stack = util.Stack()
    crossroads = util.Stack()
    path = util.Stack()
    head = (problem.getStartState(), 'Start', 1)
    graph.FillPlace(head[0], head[0])
    start = head[0]

    while not found:
        #get all children of the last added node of the stack that are located on a tile which hasn't been previously visited
        #GetChildren also updates the graph and stack, which keep track of all visited spots and all expended nodes respectively
        children = problem.getSuccessors(head[0])
        nondouble = []
        for c in children:            
            if not graph.CheckPlace(c[0]):                         
                nondouble.append(c)
                graph.FillPlace(c[0], head)                      
                stack.push(c)
        #if more than one child are created, remember the parent that created them so that path knows where to stop backing up
        #when it needs to find a new branch after a dead end
        i = 0
        while i < len(nondouble) - 1:
            crossroads.push(head)
            i += 1
        #if a node is a dead end, go to the last added child and expand again, i.o.w. perform dfs
        if not nondouble:                          
            head = stack.pop()            
            pathhead = path.pop()
            splitpoint = crossroads.pop()
            #back up until path reaches the last 'crossroad' it encountered, and then add it to path again (since you popped it to read its value)
            while not pathhead == splitpoint:
                pathhead = path.pop()
                if path.isEmpty() == True:
                    break
            if path.isEmpty() == False:           
                path.push(pathhead) 
        else:
            head = stack.pop()          
        path.push(head)
        if problem.isGoalState(head[0]):   
            found = True
    
    # graph has a grid which keeps track of which nodes were added by which nodes
    # using this grid, we can reverse engineer the path to the end if we know where the path starts and ends
    finalpath = graph.GetPath(head, start)
    return finalpath  

def breadthFirstSearch(problem):
    
    #create the necessary graph and queu and fill the start place
    found = False
    graph = Graph()
    graph.CreateGraph((100,100))
    queu = util.Queue()
    head = (problem.getStartState(), 'Start', 1)
    graph.FillPlace(head[0], head[0])
    start = head[0]

    #As long as the goal isn't found keep searching
    while not found:
        children = problem.getSuccessors(head[0])
        #If you haven't already been there add it into the queu
        for c in children:
            if not graph.CheckPlace(c[0]):                         
                graph.FillPlace(c[0], head)                      
                queu.push(c)
        head = queu.pop()
        if problem.isGoalState(head[0]):   
            found = True

    #Create the right path and return it
    finalpath = graph.GetPath(head, start)
    return finalpath
            
def uniformCostSearch(problem):
    found = False
    graph = Graph()
    graph.CreateGraph((100,100))
    pqueue = util.PriorityQueue()
    head = (problem.getStartState(), 'Start', 1)
    graph.FillPlace(head[0], head[0])
    start = head[0]
    
    while not found:
        children = problem.getSuccessors(head[0])
        for c in children:
            if not graph.CheckPlace(c[0]):
                graph.FillPlace(c[0], head)
                #put the child node in the priority queue with its priority value
                pqueue.push(c,c[2])
        #use the child node with the highest priority first
        head = pqueue.pop()
        #if the given child node is the goal then return      
        if problem.isGoalState(head[0]):   
            found = True

    finalpath = graph.GetPath(head, start)
    return finalpath

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    found = False
    graph = Graph()
    graph.CreateGraph((100,100))
    start = problem.getStartState()
    current = (start, 'Start', 0, 0)
    open = [current]
    closed = []
    graph.FillPlace(current[0], current)

    while len(open) > 0 and not found:        
        minimum = -1
        for x in open:
            #chose the node with the lowest f(n)
            if x[2] + x[3] < minimum or minimum < 0:
                current = x
                minimum = x[2] + x[3]
        open.remove(current)
        closed.append(current)
        children = problem.getSuccessors(current[0])
        nondouble = []
        for c in children:            
            if not graph.CheckPlace(c[0]):                         
                nondouble.append(c)
                graph.FillPlace(c[0], current)
                #put the child node in the list with its heuristic
                open.append(((c[0]), c[1], current[2] + 1, heuristic(c[0], problem)))
                if problem.isGoalState(c[0]):
                    current = c
                    found = True
                    break
    
    finalpath = graph.GetPath(current, start)
    return finalpath

def GetDirection(direction):
    from game import Directions
    if direction == 'North':
        return Directions.NORTH
    if direction == 'East':
        return Directions.EAST
    if direction == 'South':
        return Directions.SOUTH
    if direction == 'West':
        return Directions.WEST

class Graph:
    matrix = [[]]
    previous = [[]]

    #Creates a graph(two dimensional array) which holds true if you've been there already and a
    #two dimensional array which holds the position from which you came
    def CreateGraph(self, position):
        global matrix
        global previous
        matrix = [[False for x in range(position[0])] for y in range(position[1])]
        previous = [[((-1,-1),'Nothing') for x in range(position[0])] for y in range(position[1])]
        return matrix
    
    #Stores if that you have been in that place and from where you came
    def FillPlace(self, position, origin):
        global matrix
        global previous

        matrix [(position[0])][(position[1])] = True
        previous [(position[0])][(position[1])] = (origin[0], origin[1])        

    #Checks if you've already been there
    def CheckPlace(self, position):
        return matrix [(position[0])][(position[1])]

    #Gets the path from the end that you have found to the start and returns them in a list
    def GetPath(self, endnode, start):
        global previous
        path = []
        i = (endnode[0], endnode[1])
        while not i[1] == 'Start':
            path.append(GetDirection(i[1]))
            a = (i[0])[0]
            b = (i[0])[1]
            i = previous[a][b]
        path.reverse()
        return path

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch