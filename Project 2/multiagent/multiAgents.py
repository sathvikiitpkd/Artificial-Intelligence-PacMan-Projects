# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        # store the coordinates of the food
        foodCoordinates=newFood.asList() 
        minimDist=-1 # minimDist represents the minimum of the distances from the pacman to each food
        nearGhosts=0 # number of ghosts nearby pacman (when the scaredtimer of the corresponding ghost is 0) which are at distance less than or equal to 1
        i=0
        for x in foodCoordinates:
            if(minimDist==-1 or minimDist > util.manhattanDistance(newPos, x)):
                minimDist=util.manhattanDistance(newPos, x)
        for y in newGhostStates:
            if(util.manhattanDistance(newPos, y.getPosition())<=1):
                if(newScaredTimes[i]==0):
                    nearGhosts+=1
            i+=1
        
        return successorGameState.getScore()+(1/float(minimDist))-nearGhosts

def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        #Pacman is max player and all ghosts are min player
        numberOfGhosts = gameState.getNumAgents() - 1
        #Function for max player move
        def maxi(gameState,depth):
            #Terminal Test
            if gameState.isWin() or gameState.isLose() or self.depth==depth + 1:   
                return self.evaluationFunction(gameState)
            # set maxvalue to negative infinity
            maxvalue = -9999999
            #Get all the legal actions in the game state
            actions = gameState.getLegalActions(0)
            #for every legal action find the successors of the gamestate and call for minplayer moves and update the maxvalue
            for action in actions:
                successor= gameState.generateSuccessor(0,action)
                if maxvalue <= mini(successor,depth + 1,1) :
                   maxvalue = mini(successor,depth + 1,1)
            return maxvalue
        #Function for min player move  
        def mini(gameState,depth, agentIndex):
        # set minvalue to infinity
            minvalue = 9999999
            #Terminal Test
            if gameState.isWin() or gameState.isLose():   
                return self.evaluationFunction(gameState)
            #Get all the legal actions in the game state
            actions = gameState.getLegalActions(agentIndex)
            #for every legal action find the successors of the gamestate and call for maxplayer moves and update the minvalue if and only if agent index is No of ghosts else call for minplayer and update the minvalue 
            for action in actions:
                successor= gameState.generateSuccessor(agentIndex,action)
                if agentIndex is numberOfGhosts:
                    if minvalue >=maxi(successor,depth) :
                       minvalue = maxi(successor,depth)
                else :
                    if minvalue >=mini(successor,depth,agentIndex+1) :
                       minvalue = mini(successor,depth,agentIndex+1)
            return minvalue
        #Initiate root level of action
        actions = gameState.getLegalActions(0)
        currentScore = -9999999
        returnAction = None
        for action in actions:
            nextState = gameState.generateSuccessor(0,action)
            score = mini(nextState,0,1)
            if score > currentScore:
                returnAction = action
                currentScore = score
        return returnAction
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        #Pacman is max player and all ghosts are min player
        numberOfGhosts = gameState.getNumAgents() - 1
        #Function for max player move
        def maxi(gameState,depth,a,b):
            #initialise alpha to a
            alpha = a
            #Terminal test
            if gameState.isWin() or gameState.isLose() or self.depth==depth + 1:   
                return self.evaluationFunction(gameState)
            # set maxvalue to negative infinity
            maxvalue = -9999999
            #Get all the legal actions in the game state
            actions = gameState.getLegalActions(0)
            #for every legal action find the successors of the gamestate and call for minplayer moves and update the maxvalue
            for action in actions:
                successor= gameState.generateSuccessor(0,action)
                if maxvalue <= mini(successor,depth + 1,1,alpha,b) :
                   maxvalue = mini(successor,depth + 1,1,alpha,b)
                #update alpha value with maximum of maxvalue and alpha
                alpha = max(alpha,maxvalue)
                #Main Condition: If alpha > b then we need to prune the sub-tree
                if alpha > b :
                   return alpha
            return maxvalue
            
        def mini(gameState,depth,agentIndex,a,b):
            #initialise beta to b and minvalue to infinity
            minvalue = 9999999
            beta = b
            #Terminal Test
            if gameState.isWin() or gameState.isLose():   
                return self.evaluationFunction(gameState)
            #Get all the legal actions in the game state 
            actions = gameState.getLegalActions(agentIndex)
            #for every legal action find the successors of the gamestate and call for maxplayer moves and update the minvalue if and only if agent index is No of ghosts else call for minplayer and update the minvalue
            for action in actions:
                successor= gameState.generateSuccessor(agentIndex,action)
                if agentIndex is numberOfGhosts:
                    if minvalue >=maxi(successor,depth,a,beta) :
                       minvalue = maxi(successor,depth,a,beta) 
                else :
                    if minvalue >=mini(successor,depth,agentIndex+1,a,beta) :
                       minvalue = mini(successor,depth,agentIndex+1,a,beta)
                #update beta value with minimum of minvalue and beta
                beta = min(beta,minvalue) 
                #Main Condition: If a > beta then we need to prune the sub-tree
                if a > beta :
                       return beta 
            return minvalue
        
        #Initiate root level of action
        actions = gameState.getLegalActions(0)
        alpha = -999999
        beta = 999999
        currentScore = -9999999
        returnAction = None
        for action in actions:
            nextState = gameState.generateSuccessor(0,action)
            score = mini(nextState,0,1,alpha,beta)
            if score > currentScore:
                returnAction = action
                currentScore = score
            if score > beta:
                return returnAction
            alpha= max(alpha,score)
        return returnAction
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        #Function for max player move
        def maxi(gameState,depth):
            #Terminal Test
            if gameState.isWin() or gameState.isLose() or self.depth == depth + 1:   
                return self.evaluationFunction(gameState)
            #Initialise maxvalue to negative infinity
            maxvalue = -999999
            #Get all the legal actions in the game state 
            actions = gameState.getLegalActions(0)
            #for every legal action find the successors of the gamestate and call for chance player moves and update the maxvalue
            for action in actions:
                successor= gameState.generateSuccessor(0,action)
                if maxvalue <= expecti(successor,depth + 1,1) :
                   maxvalue = expecti(successor,depth + 1,1)
            return maxvalue
        #Function for min player move(implicitly set for chance player's moves)
        def expecti(gameState,depth, agentIndex):
            if gameState.isWin() or gameState.isLose():    
                return self.evaluationFunction(gameState)
            #Get all the legal actions in the game state 
            actions = gameState.getLegalActions(agentIndex)
            #initialise totalvalue to zero
            totalvalue = 0
            #for every legal action find the successors of the gamestate and call for maxplayer moves and update the expectedvalue if and only if agent index is No of ghosts else call for maxplayer and update the expected value
            for action in actions:
                successor= gameState.generateSuccessor(agentIndex,action)
                if agentIndex == (gameState.getNumAgents() - 1):
                    expectedvalue = maxi(successor,depth)
                else:
                    expectedvalue = expecti(successor,depth,agentIndex+1)
                # Add the expectedvalue to totalvalue for every legal action
                totalvalue += expectedvalue
            #if there are no legal actions then return zero
            if len(actions) == 0:
                return  0
            #We know Totalvalue indicates summation of expected value from every legal action,is divided by total no of legal actions
            else :
                 return float(totalvalue)/float(len(actions))
        #Initialise Root level of action
        currentScore = -999999
        returnAction = None
        actions = gameState.getLegalActions(0)
        for action in actions:
            nextState = gameState.generateSuccessor(0,action)
            score = expecti(nextState,0,1)
            if score > currentScore:
                currentScore = score
                returnAction = action
        return returnAction
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: The features added for the evaluation here are the following:
    1. The minimum of the distances from the pacman to the food and power pellets. (minimDist)
    2. The number of ghosts which are at a distance less than or equal to 1 when the scaredTimer is zero for the corresponding ghost. (nearGhosts)
    3. The sum of all the distances from the Pacman to the ghosts. (ghostDist)
    4. The number of ghosts which are at a distance less than or equal to 1 when the scaredTimer is not equal to zero. (scaredGhost)
    5. Checking whether the minimDist is greater than or equal to the ghostDist(this might be a chance to collect the food where the ghosts are not present). (choice)
    """
    "*** YOUR CODE HERE ***"
    Pos = currentGameState.getPacmanPosition()
    Food = currentGameState.getFood()
    GhostStates = currentGameState.getGhostStates()
    ScaredTimes = [ghostState.scaredTimer for ghostState in GhostStates]
    Capsules= currentGameState.getCapsules()

    foodCoordinates=Food.asList()
    ghostDist=0
    scaredGhost=0
    nearGhosts=0
    minimDist=-1
    choice=1
    i=0
    for foodPos in foodCoordinates:
        if(minimDist==-1 or minimDist>util.manhattanDistance(Pos,foodPos)):
            minimDist=util.manhattanDistance(Pos,foodPos)
    for capsulePos in Capsules:
        if(minimDist>util.manhattanDistance(Pos,capsulePos)):
            minimDist=util.manhattanDistance(Pos,capsulePos)
    for y in GhostStates:
        ghostDist+=util.manhattanDistance(Pos,y.getPosition())
        if(ghostDist==0):
            ghostDist+=10000
        if(util.manhattanDistance(Pos, y.getPosition())<=1):
            if(ScaredTimes[i]==0):
                nearGhosts+=1
            else:
                scaredGhost+=1
        i+=1
    if(minimDist>=ghostDist):
        choice+=1000000
    return currentGameState.getScore()+(10*(1/float(minimDist)))-((nearGhosts+ghostDist-(scaredGhost*100))*10)-(1/float(choice))
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
