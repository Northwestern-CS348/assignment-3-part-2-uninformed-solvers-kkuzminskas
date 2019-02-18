
from solver import *



class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

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
        GM = self.gm

        if self.currentState.state == self.victoryCondition:
            return True


        curr_Gamestate = self.currentState
        self.visited[curr_Gamestate] = True
        children = self.get_children()
        self.currentState.children = children
        idx = self.currentState.nextChildToVisit
        
        # final unexplored state
        if idx == len(self.currentState.children):
            curr = self.currentState.parent
            while curr != None:
                idx = curr.nextChildToVisit
                mov = curr.requiredMovable

                # should be in the parent game state
                self.gm.reverseMove(mov) 

                while idx != len(curr.children):
                    curr_child = curr.children[idx]
                    if not self.visited[curr_child]:
                        new_mov = curr_child.requiredMovable
                        self.gm.makeMove(new_mov)
                        self.currentState = curr_child
                        self.currentState.parent.nextChildToVisit = idx + 1
                        return False
                    elif self.visited[curr_child] == False:
                        new_mov = curr_child.requiredMovable
                        self.gm.makeMove(new_mov)
                        self.currentState = curr_child
                        self.currentState.parent.nextChildToVisit = idx + 1
                        return False
                    idx += 1
                
                curr = self.currentState.parent
            return False
        
        

        self.currentState = self.currentState.children[idx]
        self.gm.makeMove(self.currentState.requiredMovable)
        self.currentState.parent.nextChildToVisit += 1


        return False


class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def get_children(self):
        children = []
        curr_layers = []
        if self.currentState.parent:
            curr_layers = self.currentState.parent.children
            
        else:
            curr_layers.append(self.currentState)

        for i in range(0, len(curr_layers)):
            ind = 0
            c = curr_layers[i]
            print("c")
            print(c.state)

            # get back to c
            if self.currentState != c:
                #print("current state")
                #print(self.currentState.state)
                # return to parent state:
                ret_parent_mov = self.currentState.requiredMovable
                self.gm.reverseMove(ret_parent_mov)

                req_mov = c.requiredMovable
                self.gm.makeMove(req_mov)
                #ind = 1
                #print("made move")

            movables = self.gm.getMovables()
            #movables.reverse()

            parent = c
            depth = parent.depth

            #print("should be at c game state")
            #print(self.gm.getGameState())

            for m in movables:
                self.gm.makeMove(m)
                s = self.gm.getGameState()
                game_state = GameState(s, depth + 1, m)
                game_state.parent = parent
                if game_state not in self.visited:
                    children.append(game_state)
                    self.visited[game_state] = False

                self.gm.reverseMove(m)
                #print("movable state")
                #print(self.gm.getGameState())

            #if ind == 1:
            #    self.gm.reverseMove(req_mov)


        if not children:
            return False

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

        if self.currentState.state == self.victoryCondition:
            return True


        curr_Gamestate = self.currentState
        self.visited[curr_Gamestate] = True

        for m in self.visited:
            if self.visited[m] == False:
                print(m.depth)


        if self.currentState.parent:
            idx = self.currentState.parent.nextChildToVisit
            
            # final unexplored state
            if idx == len(self.currentState.parent.children):
                children = self.get_children()
                self.currentState.children = children
                for c in self.currentState.parent.children:
                    c.children = children
                self.currentState.nextChildToVisit = 0
                idx = 0
            
            if self.currentState.children == False:
                return False       

            # return to the parent state
            ret_parent_mov = self.currentState.requiredMovable
            self.gm.reverseMove(ret_parent_mov)
            self.currentState = self.currentState.parent.children[idx]
            self.gm.makeMove(self.currentState.requiredMovable)
            self.currentState.parent.nextChildToVisit += 1

        else:
            children = self.get_children()
            self.currentState.children = children
            self.currentState.nextChildToVisit = 0
            self.currentState = self.currentState.children[0]
            self.gm.makeMove(self.currentState.requiredMovable)
            self.currentState.parent.nextChildToVisit += 1
            return False

        return False

