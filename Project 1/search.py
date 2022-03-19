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
    frontier = util.Stack()   
    element = problem.getStartState()
    expanded_states = []
    explored_path = []
    if problem.isGoalState(element):
    	return explored_path
    else :
    	frontier.push((element,explored_path))
    i=0
    while i<1 :
    	if frontier.isEmpty() :
    		return []
    	else:
    		(node,explored_path) = frontier.pop()
	    	expanded_states.append(node);
	    	if problem.isGoalState(node):
	    		return explored_path	
	    	else:
			for j in problem.getSuccessors(node):
		    		if j[0] not in expanded_states:
				    		newpath = explored_path+[j[1]]
				    		frontier.push((j[0],newpath))
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    frontier = util.Queue()   
    element = problem.getStartState()
    expanded_states = []
    explored_path = []
    if problem.isGoalState(element):
    	return explored_path
    else :
    	frontier.push((element,explored_path))
    i=0
    while i<1 :
    	if frontier.isEmpty() :
    		return []
    	else:
    		(node,explored_path) = frontier.pop()
	    	expanded_states.append(node)
	    	if problem.isGoalState(node):
	    		return explored_path
	    	else:	
			for j in problem.getSuccessors(node):
		    		if j[0] not in expanded_states :
		    			if j[0] not in (state[0] for state in frontier.list):
				    		newpath = explored_path + [j[1]]
				    		frontier.push((j[0],newpath))
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    Frontier = util.PriorityQueue()
    path = [] 
    visited = [] 
    if problem.isGoalState(problem.getStartState()):
        return []
    Frontier.push((problem.getStartState(),[]),0)
    i=0
    while(i<1):
        if Frontier.isEmpty():
            return []
        node,path = Frontier.pop()
        visited.append(node)
        if problem.isGoalState(node):
            return path
        succ = problem.getSuccessors(node)
        if succ:
            for item in succ:
                if item[0] not in visited and (item[0] not in (state[2][0] for state in Frontier.heap)):
                    newPath = path + [item[1]]
                    value = problem.getCostOfActions(newPath)
                    Frontier.push((item[0],newPath),value)
                elif item[0] not in visited and (item[0] in (state[2][0] for state in Frontier.heap)):
                    for state in Frontier.heap:
                        if state[2][0] == item[0]:
                            oldvalue = problem.getCostOfActions(state[2][1])
                    newvalue = problem.getCostOfActions(path + [item[1]])
                    if oldvalue > newvalue:
                        newPath = path + [item[1]]
                        Frontier.update((item[0],newPath),newvalue)	
    util.raiseNotDefined()


from util import PriorityQueue
class MyPriorityQueueWithFunction(PriorityQueue):
    """
    Implements a priority queue with the same push/pop signature of the
    Queue and the Stack classes. This is designed for drop-in replacement for
    those two classes. The caller has to provide a priority function, which
    extracts each item's priority.
    """
    def  __init__(self, problem, priorityFunction):
        "priorityFunction (item) -> priority"
        self.priorityFunction = priorityFunction      # store the priority function
        PriorityQueue.__init__(self)        # super-class initializer
        self.problem = problem
    def push(self, item, heuristic):
        "Adds an item to the queue with priority from the priority function"
        PriorityQueue.push(self, item, self.priorityFunction(self.problem,item,heuristic))


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


# Calculate f(n) = g(n) + h(n) #
def f(problem,state,heuristic):
    return problem.getCostOfActions(state[1]) + heuristic(state[0],problem)
    
def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***" 
    frontier = MyPriorityQueueWithFunction(problem,f)
    element = (problem.getStartState(),[])
    expanded_states = []
    explored_path = []
    if problem.isGoalState(element):
    	return explored_path
    else :
    	frontier.push(element,heuristic)
    i=0
    while i<1 :
    	if frontier.isEmpty() :
    		return []
    	else:
    		(node,explored_path) = frontier.pop()
    		if node in expanded_states:
            		continue
	    	expanded_states.append(node)
	    	if problem.isGoalState(node):
	    		return explored_path	
	    	else:
			for j in problem.getSuccessors(node):
		    		if j[0] not in expanded_states:
				    		newpath = explored_path+[j[1]]
				    		frontier.push((j[0],newpath),heuristic)
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
