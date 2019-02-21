
from solver import *
import queue



class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)
        self.movables = queue.Queue()

    def get_children(self):
        movables = self.gm.getMovables()

        parent = self.currentState
        depth = parent.depth

        children = []


        for m in movables:
            self.gm.makeMove(m)
            s = self.gm.getGameState()


            game_state = GameState(s, depth + 1, m)
            game_state.parent = parent
            if game_state not in self.visited:
                children.append(game_state)
                self.visited[game_state] = False
            elif self.visited[game_state] == False:
                children.append(game_state)

            self.gm.reverseMove(m)


    
        return children


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

        if self.currentState.state == self.victoryCondition:
            return True

        curr_Gamestate = self.currentState
        self.visited[curr_Gamestate] = True

        idx = self.currentState.nextChildToVisit

        children = self.get_children()
        self.currentState.children = children

        while idx == len(self.currentState.children):
            if self.currentState.depth == 0:
                idx = self.currentState.nextChildToVisit
                break
            ret_parent_mov = self.currentState.requiredMovable
            self.currentState = self.currentState.parent
            self.gm.reverseMove(ret_parent_mov)
            idx = self.currentState.nextChildToVisit
        
        
        child = self.currentState.children[idx]

        if self.visited[child] == False:
            self.currentState.nextChildToVisit += 1
            self.gm.makeMove(child.requiredMovable)
            self.currentState = child
            return False
        
        if self.currentState.state == self.victoryCondition:
            return True

        return False

   

class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)
        self.nodes = queue.Queue()
        self.list_moves_root_to_child = dict()

    def get_children(self):
        movables = self.gm.getMovables()

        parent = self.currentState
        depth = parent.depth

        children = []

        for m in movables:
            self.gm.makeMove(m)
            s = self.gm.getGameState()

            parent_list_moves = []
            parent_list_moves = self.list_moves_root_to_child[parent].copy()

            game_state = GameState(s, depth + 1, m)
            game_state.parent = parent

            if game_state not in self.visited:
                children.append(game_state)
                self.visited[game_state] = False
                self.nodes.put(game_state)
                self.list_moves_root_to_child[game_state] = []
                self.list_moves_root_to_child[game_state].extend(parent_list_moves)
                self.list_moves_root_to_child[game_state].append(game_state)

            self.gm.reverseMove(m)

        return children

    

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

        if self.currentState.state == self.victoryCondition:
            return True

        curr_Gamestate = self.currentState
        self.visited[curr_Gamestate] = True

        # for parent node
        if self.currentState.depth == 0:
            self.list_moves_root_to_child[self.currentState] = []


        # get the children of the current node
        children = self.get_children()
        self.currentState.children = children

        # get the list of moves for the current state to get to the root
        prev_list_moves = self.list_moves_root_to_child[self.currentState]
        prev_list_moves.reverse()

        # get the list of moves for the new current state to get from the root to the state
        self.currentState = self.nodes.get()
        curr_list_moves = self.list_moves_root_to_child[self.currentState]
        

        # get the gm to the root
        for m in prev_list_moves:
            next_mov = m
            self.gm.reverseMove(next_mov.requiredMovable)

        # get the gm to the current state
        for m in curr_list_moves:
            next_mov = m
            self.gm.makeMove(next_mov.requiredMovable)

        if self.currentState.state == self.victoryCondition:
            return True
        

        return False
        
        

