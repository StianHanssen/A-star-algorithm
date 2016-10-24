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
from heapq import heappush, heappop

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
        return successorGameState.getScore()

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
        """
        "*** YOUR CODE HERE ***"
        rel_depth = self.depth * gameState.getNumAgents()  # Relative depth to all the agents
        return self.miniMax(gameState, rel_depth, 0)[1]

    def miniMax(self, game_state, depth, agent_index):
        if game_state.isWin() or game_state.isLose() or depth == 0:  # If terminal node
            return self.evaluationFunction(game_state), None
        next_agent = (agent_index + 1) % game_state.getNumAgents()
        sign = -1 if agent_index == 0 else 1  # If pacman: Small initial value, else: Big initial value
        value, best_action = sign * float('inf'), None  # Sign affects whether we have a very big number (minimize) or small number (maximize)
        for action in game_state.getLegalActions(agent_index):
            next_state = game_state.generateSuccessor(agent_index, action)
            next_value = self.miniMax(next_state, depth - 1, next_agent)[0]
            if (agent_index == 0 and value < next_value) or (agent_index > 0 and value > next_value):  # Maximizing for pacman and minimizing for ghost
                value = next_value
                best_action = action
        return value, best_action

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        rel_depth = self.depth * gameState.getNumAgents()  # Relative depth to all the agents
        inf = float('inf')
        return self.alphaBeta(gameState, rel_depth, 0, -inf, inf)[1]

    def alphaBeta(self, game_state, depth, agent_index, a, b):
        if game_state.isWin() or game_state.isLose() or depth == 0:  # If terminal node
            return self.evaluationFunction(game_state), None
        next_agent = (agent_index + 1) % game_state.getNumAgents()
        pacman, sign, comp = (True, -1, max) if agent_index == 0 else (False, 1, min)  # If pacman: Small value and maximize, else: Big value and minimize
        value, best_action = sign * float('inf'), None  # Sign affects whether we have a very big (minimizing) or very small number (maximize)
        for action in game_state.getLegalActions(agent_index):
            next_state = game_state.generateSuccessor(agent_index, action)
            next_value = self.alphaBeta(next_state, depth - 1, next_agent, a, b)[0]
            value = comp(value, next_value)  # If pacman: comp() == max(), else: comp() == min()
            if (pacman and b < value) or (not pacman and value < a):  # If any condition implying we don't need further iteration
                break
            if pacman and value > a:  # If a better alpha value found (maximize)
                a = value
                best_action = action
            elif not pacman and b > value:  # If a better beta value found (minimize)
                b = value
                best_action = action
        return value, best_action

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
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
