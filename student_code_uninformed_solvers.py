
from solver import *
import queue



class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)
        self.movables = queue.Queue()

    def get_children(self):
        movables = self.gm.getMovables()
        #movables.reverse()

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


    def get_child(self):
        movables = self.gm.getMovables()

        parent = self.currentState
        depth = parent.depth
        idx = parent.nextChildToVisit


        # if movables==0 go to parent
        if not movables or idx == len(movables):
            self.gm.reverseMove(self.currentState.requiredMovable)
            self.currentState = self.currentState.parent
            self.get_child()
            return self.currentState

        m = movables[idx]

        self.gm.makeMove(m)
        s = self.gm.getGameState()
        game_state = GameState(s, depth + 1, m)
        game_state.parent = parent
       
        if game_state not in self.visited:
            child = game_state
            self.visited[game_state] = True
            self.currentState.children.append(child)
        else:
            self.currentState.nextChildToVisit += 1
            self.gm.reverseMove(m)
            child = self.get_child()

        return child


    def solveOneStep2(self):
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

        if self.gm.getGameState() == self.victoryCondition:
            return True
            
        possibleMoves = self.gm.getMovables()

        if len(possibleMoves) == 0:
            self.currentState = self.currentState.parent
            self.solveOneStep()
        else:
            allMovesVisited = True
            for move in possibleMoves:
                self.gm.makeMove(move)

                currentGameState = GameState(self.gm.getGameState(), self.currentState.depth + 1, move)

                if not self.visited.get(currentGameState, False):
                    if not currentGameState in self.currentState.children:
                        self.currentState.children.append(currentGameState)
                        currentGameState.parent = self.currentState

                self.gm.reverseMove(move)

            for child in self.currentState.children:
                move = child.requiredMovable
                self.gm.makeMove(move)

                if self.visited.get(child, False):
                    self.gm.reverseMove(move)
                    continue

                self.visited[child] = True
                self.currentState = child
                allMovesVisited = False
                break

            if allMovesVisited:
                self.currentState = self.currentState.parent
                self.solveOneStep()
        
        if self.gm.getGameState() == self.victoryCondition:
            return True

        return False

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

        while idx == len(children):
            if self.currentState.depth == 0:
                idx = self.currentState.nextChildToVisit
                break
            ret_parent_mov = self.currentState.requiredMovable
            self.currentState = self.currentState.parent
            self.gm.reverseMove(ret_parent_mov)
            idx = self.currentState.nextChildToVisit
        
        
        child = self.currentState.children[idx]

        if self.visited[child] == False:
            self.gm.makeMove(child.requiredMovable)
            self.currentState = child
            return False
        
        if self.currentState.state == self.victoryCondition:
            return True

        # next child no children array
        #self.currentState = self.get_child()
    
        return False

    def solveOneStep1(self):
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

        # next child no children array
        self.currentState = self.get_child()
        
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

            # if s == self.victoryCondition:
            #    return True
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
            #elif self.visited[game_state] == False:
            #    children.append(game_state)
            #    self.nodes.put(game_state)
            #    self.list_moves_root_to_child[game_state] = []
            #    self.list_moves_root_to_child[game_state].extend(parent_list_moves)
            #    self.list_moves_root_to_child[game_state].append(game_state)

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

        GM = self.gm

        #print("current")
        #print(self.currentState.state)
        if self.currentState.state == self.victoryCondition:
            return True

        curr_Gamestate = self.currentState
        curr_state = curr_Gamestate.state
        self.visited[curr_Gamestate] = True
        idx = self.currentState.nextChildToVisit

        # for parent node
        if self.currentState.depth == 0:
            self.list_moves_root_to_child[self.currentState] = []

        children = self.get_children()
        self.currentState.children = children


        prev_list_moves = self.list_moves_root_to_child[self.currentState]
        prev_list_moves.reverse()

        self.currentState = self.nodes.get()
        curr_list_moves = self.list_moves_root_to_child[self.currentState]
        

        # get the gm to the current state
        for m in prev_list_moves:
            next_mov = m
            self.gm.reverseMove(next_mov.requiredMovable)
            #print("next move reverse")
            #print(self.gm.getGameState())

        for m in curr_list_moves:
            next_mov = m
            self.gm.makeMove(next_mov.requiredMovable)
            #print("next move down")
            #print(self.gm.getGameState())
            #check = self.gm.getGameState()

        if self.currentState.state == self.victoryCondition:
            return True
        

        return False
        
        

