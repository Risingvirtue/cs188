# valueIterationAgents.py
# -----------------------
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


# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent
import collections

from util import *
class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()
    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        states = self.mdp.getStates()
        self.valueActions = {}
        for state in states:
            actions = self.mdp.getPossibleActions(state)
            self.valueActions[state] = [0 for action in actions]
            if self.mdp.isTerminal(state):
                self.valueActions[state] = [0]
        counter = 0
        while counter != self.iterations:
            counter += 1
            nextValues = {}
            for state in states:
                if self.mdp.isTerminal(state):
                    continue
                if state not in nextValues:
                    nextValues[state] = []
                actions = self.mdp.getPossibleActions(state)
                direction = 0
                for action in actions:
                    SAPairs = self.mdp.getTransitionStatesAndProbs(state, action)
                    sumState = 0
                    for pair in SAPairs:
                        reward = self.mdp.getReward(state, action, pair[0])
                        sumState += pair[1] * (reward + self.discount * max(self.valueActions[pair[0]]))
                    nextValues[state] += [sumState]
            for update in nextValues:
                self.valueActions[update] = nextValues[update]
        #reward = self.mdp.getReward(state, action, nextState)
        for valueAction in self.valueActions:
            self.values[valueAction] = max(self.valueActions[valueAction])
        return self.values
    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        SAPairs = self.mdp.getTransitionStatesAndProbs(state, action)
        sumQ = 0
        for pair in SAPairs:
            reward = self.mdp.getReward(state, action, pair[0])
            sumQ += pair[1] * (reward + self.discount * self.values[pair[0]])
        return sumQ

        util.raiseNotDefined()

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        actions = self.mdp.getPossibleActions(state)
        maxAction = 'test'
        bestActionTotal = float('-inf')
        for action in actions:
            currTotal = 0
            stateProbs = self.mdp.getTransitionStatesAndProbs(state, action)
            for pair in stateProbs:
                currTotal += pair[1] * (self.mdp.getReward(state, action, pair[0]) \
                                        + self.discount * self.values[pair[0]])
            if currTotal > bestActionTotal:
                maxAction = action
                bestActionTotal = currTotal

        return maxAction
        util.raiseNotDefined()

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        states = self.mdp.getStates()
        numStates = len(states)
        counter = 0
        while counter != self.iterations:
            currState = states[counter % numStates]
            counter += 1
            if self.mdp.isTerminal(currState):
                continue
            actions = self.mdp.getPossibleActions(currState)
            bestAction, bestValue = 'test' , -999
            for action in actions:
                SAPairs = self.mdp.getTransitionStatesAndProbs(currState, action)
                sumQ = 0
                for pair in SAPairs:
                    reward = self.mdp.getReward(currState, action, pair[0])
                    sumQ += pair[1] * (reward + self.discount * self.values[pair[0]])
                if sumQ > bestValue:
                    bestValue = sumQ
                    bestAction = action
            self.values[currState] = bestValue
        return self.values

class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"

        def predecessors():
            statePredecessors = {}
            states = self.mdp.getStates()
            for state in states:
                actions = self.mdp.getPossibleActions(state)
                for action in actions:
                    SAPairs = self.mdp.getTransitionStatesAndProbs(state, action)
                    for pair in SAPairs:
                        if pair[1] != 0:
                            if pair[0] not in statePredecessors:
                                statePredecessors[pair[0]] = []
                            if state not in statePredecessors[pair[0]]:
                                statePredecessors[pair[0]] += [state]
            return statePredecessors
        def updateState(state):
            actions = self.mdp.getPossibleActions(state)
            bestAction, bestValue = 'test' , -999
            for action in actions:
                SAPairs = self.mdp.getTransitionStatesAndProbs(state, action)
                sumQ = 0
                for pair in SAPairs:
                    reward = self.mdp.getReward(state, action, pair[0])
                    sumQ += pair[1] * (reward + self.discount * self.values[pair[0]])
                if sumQ > bestValue:
                    bestValue = sumQ
                    bestAction = action
            self.values[state] = bestValue
            return
        def maxQ(state):
            actions = self.mdp.getPossibleActions(state)
            maxQ = -999
            for action in actions:
                qValue = self.computeQValueFromValues(state, action)
                maxQ = max(maxQ, qValue)
            return maxQ
        statePredecessors = predecessors()
        states = self.mdp.getStates()
        update = PriorityQueue()
        for state in states:
            if self.mdp.isTerminal(state):
                continue
            maxQValue = maxQ(state)
            diff = abs(self.values[state] - maxQValue)
            update.push(state, -diff)

        for it in range(self.iterations):
            if update.isEmpty():
                break
            state = update.pop()
            updateState(state)
            for p in statePredecessors[state]:
                maxQValue = maxQ(p)
                diff = abs(self.values[p] - maxQValue)
                if diff > self.theta:
                    update.update(p, -diff)

        return self.values
