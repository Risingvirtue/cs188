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

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
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

    def evaluationFunction(self, currentGameState, action):
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
        from util import *
        currPosition = currentGameState.getPacmanPosition()
        oldFood = currentGameState.getFood()
        foodList = oldFood.asList()
        score = 0
        pelletPQ = PriorityQueue()
        order = []
        counter = 0
        for food in foodList:
            if food == newPos:
                score += 25
            else:
                manDist = manhattanDistance(newPos, food)
                pelletPQ.push(food, manDist)
        while not pelletPQ.isEmpty() and counter != 2:
            counter += 1
            score += 10 / manhattanDistance(newPos, pelletPQ.pop())
        ghostPos = successorGameState.getGhostPositions()
        scareTime = 999
        for time in newScaredTimes:
            if scareTime > time:
                scareTime = time
        multiplier = -1
        if scareTime > 10:
            multiplier = scareTime / 10
        for ghost in ghostPos:
            ghostDist = manhattanDistance(newPos, ghost)
            if ghostDist == 0:
                score += 500 * multiplier
            else:
                score += (50/ghostDist) * multiplier

        return score

def scoreEvaluationFunction(currentGameState):
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

    def getAction(self, gameState):
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
        numGhost = [gameState.getNumAgents() - 1]
        currAction = ['test']
        def maxValue(state, deep):
            currValue = -9999
            prevValue = currValue
            pacmanActions = state.getLegalActions(0)
            for action in pacmanActions:
                successor = state.generateSuccessor(0,action)
                currValue = max(currValue, value(successor, deep , 1))
                if prevValue != currValue and state == gameState:
                    currAction[0] = action
                    prevValue = currValue
            return currValue
        def minValue(state, deep, ghostNum):
            currValue = 9999
            ghostAction = state.getLegalActions(ghostNum)
            if ghostNum == numGhost[0]:
                deep -= 1
            for action in ghostAction:
                successor = state.generateSuccessor(ghostNum , action)
                newGhostNum = (ghostNum + 1) % (numGhost[0] + 1)
                currValue = min(currValue, value(successor, deep, newGhostNum))
            return currValue
        def value(state, deep, ghostNum):
            if state.isWin() or state.isLose() or deep == 0:
                return self.evaluationFunction(state)
            elif ghostNum == 0:
                return maxValue(state, deep)
            else:
                return minValue(state, deep, ghostNum)
        value(gameState, self.depth, 0)
        return currAction[0]
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        numGhost = [gameState.getNumAgents() - 1]
        currAction = ['test']
        def maxValue(state, a, b, deep):
            currValue = -9999
            prevValue = currValue
            pacmanActions = state.getLegalActions(0)
            for action in pacmanActions:
                successor = state.generateSuccessor(0 , action)
                currValue = max(currValue, value(successor, a, b, deep, 1))
                if currValue > b:
                    return currValue
                if prevValue != currValue and state == gameState:
                    currAction[0] = action
                    prevValue = currValue
                a = max(a, currValue)
            return currValue
        def minValue(state, a, b, deep, ghostNum):
            currValue = 9999
            ghostAction = state.getLegalActions(ghostNum)
            if ghostNum == numGhost[0]:
                deep -= 1
            for action in ghostAction:
                successor = state.generateSuccessor(ghostNum, action)
                newGhostNum = (ghostNum + 1) % (numGhost[0] + 1)
                currValue = min(currValue, value(successor, a, b, deep, newGhostNum))
                if currValue < a:
                    return currValue
                b = min(b, currValue)
            return currValue
        def value(state, a, b, deep, ghostNum):
            if state.isWin() or state.isLose() or deep == 0:
                return self.evaluationFunction(state)
            elif ghostNum == 0:
                return maxValue(state, a, b, deep)
            else:
                return minValue(state, a, b, deep, ghostNum)
        value(gameState, -999, 999, self.depth, 0)
        return currAction[0]
        util.raiseNotDefined()
class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        numGhost = [gameState.getNumAgents() - 1]
        currAction = ['test']
        def maxValue(state, deep):
            currValue = -9999
            prevValue = currValue
            pacmanActions = state.getLegalActions(0)
            for action in pacmanActions:
                successor = state.generateSuccessor(0,action)
                currValue = max(currValue, value(successor, deep , 1))
                if prevValue != currValue and state == gameState:
                    currAction[0] = action
                    prevValue = currValue
            return currValue
        def chance(state, deep, ghostNum):
            sumValue = 0.0
            ghostActions = state.getLegalActions(ghostNum)
            numNodes = 0.0 + len(ghostActions)
            p = 1.0 / numNodes
            if ghostNum == numGhost[0]:
                deep -= 1
            for action in ghostActions:
                successor = state.generateSuccessor(ghostNum, action)
                newGhostNum = (ghostNum + 1) % (numGhost[0] + 1)
                sumValue += p * value(successor, deep, newGhostNum)
            return sumValue
        def value(state, deep, ghostNum):
            if state.isWin() or state.isLose() or deep == 0:
                return self.evaluationFunction(state)
            elif ghostNum == 0:
                return maxValue(state, deep)
            else:
                return chance(state, deep, ghostNum)
        value(gameState, self.depth, 0)
        return currAction[0]
        util.raiseNotDefined()
def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    from util import *
    foodList = currentGameState.getFood().asList()
    currPos = currentGameState.getPacmanPosition()
    currGhostStates = currentGameState.getGhostStates()
    ghosts = currentGameState.getGhostPositions()
    scaredTimes = [ghostState.scaredTimer for ghostState in currGhostStates]
    score = 0
    pelletPQ = PriorityQueue()
    order = []
    counter = 0
    distGhost = 0
    closeFood = 0
    whiteGhost = 0
    currScore = scoreEvaluationFunction(currentGameState)
    if currentGameState.isLose():
        return -9999
    if currentGameState.isWin():
        return 9999
    numFood = len(foodList)
    numCapsules = len(currentGameState.getCapsules())
    for food in foodList:
        manDist = manhattanDistance(currPos, food)
        pelletPQ.push(food, manDist)
    if numFood != 0:
        closeFood = manhattanDistance(currPos, pelletPQ.pop())
    ghostNum = 0
    for ghost in ghosts:
        manDist = manhattanDistance(currPos, ghost)
        if manDist != 0 and scaredTimes[ghostNum] == 0:
            distGhost += 1 / manDist
        elif manDist != 0 and scaredTimes[ghostNum] > 0:
            whiteGhost += manDist
        else:
            distGhost = 1
        ghostNum += 1
    score = currScore - 2 * distGhost - 2 * closeFood - 5 * numFood - 1 * whiteGhost - numCapsules * 18
    return score
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
