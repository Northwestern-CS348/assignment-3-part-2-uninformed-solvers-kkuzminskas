
from solver import *




class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        successors = []
        GM = self.gm


        curr_Gamestate = self.currentState
        curr_state = curr_Gamestate.state
        movables = GM.getMovables()
        children = []
        depth = curr_Gamestate.depth 
        unexplored = []

        curr_Gamestate.children = movables

        successors.append(curr_Gamestate)
        
        while len(successors) != 0:
            curr_Gamestate = successors.pop()
            curr_state = curr_Gamestate.state

            print(curr_state)

            if str(curr_Gamestate) == str(self.victoryCondition):
                return True
            
            print("current state")
            print(curr_state)

            # loop through the children
            for m in movables:
                GM.makeMove(m)
                s = GM.getGameState()
                c = GameState(s, depth + 1, m)
                c.parent = curr_state
                self.solveOneStep()
                GM.reverseMove(m)
                successors.append(c)



        return True


class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here

       

        return True
