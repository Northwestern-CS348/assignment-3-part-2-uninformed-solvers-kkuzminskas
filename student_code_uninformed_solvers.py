
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

    def get_child(self):
        movables = self.gm.getMovables()

        parent = self.currentState
        depth = parent.depth
        idx = parent.nextChildToVisit


        # if movables==0 go to parent
        if not movables:
            self.gm.reverseMove(self.currentState.requiredMovable)
            self.currentState = self.currentState.parent
            return self.currentState

        m = movables[idx]

        self.gm.makeMove(m)
        s = self.gm.getGameState()
        game_state = GameState(s, depth + 1, m)
        game_state.parent = parent
       
        if game_state not in self.visited:
            child = game_state
            self.visited[game_state] = False
            #self.currentState.children.append(child)
        #elif not self.visited[game_state]:
        #    child = game_state
            #self.currentState.children.append(child)
        else:
            self.currentState.nextChildToVisit += 1
            self.gm.reverseMove(m)
            child = self.get_child()
           

        self.currentState = child

    
        return child



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


        # times out
        #self.currentState.children = self.get_children()
        #child = self.currentState.children[idx]
        #self.currentState.nextChildToVisit += 1

        #req_mov = child.requiredMovable
        #self.gm.makeMove(req_mov)
        #self.currentState = child


        # next child no children array
        self.get_child()
    
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

        next_child = 0


        for i in range(0, len(curr_layers)):
            ind = 0
            c = curr_layers[i]

            print("curr layers")
            print(c.state)

            # get back to c
            if self.gm.getGameState() != c.state:
                #print("current state")
                #print(self.currentState.state)
                # return to parent state:
                ret_parent_mov = self.currentState.requiredMovable
                self.gm.reverseMove(ret_parent_mov)

                req_mov = c.requiredMovable
                self.gm.makeMove(req_mov)
                self.currentState = c
                #ind = 1
                #print("made move")
            print("checking game state")
            print(self.gm.getGameState())

            movables = self.gm.getMovables()

            #movables.reverse()

            parent = c
            depth = parent.depth
            c.nextChildToVisit = next_child
            

            #print("should be at c game state")
            #print(self.gm.getGameState())

            for m in movables:
                print("looking at movables")
                print(m)
                self.gm.makeMove(m)
                s = self.gm.getGameState()
                print(s)
                game_state = GameState(s, depth + 1, m)
                game_state.parent = parent
                if game_state not in self.visited:
                    children.append(game_state)
                    self.visited[game_state] = False
                elif self.visited[game_state] == False:
                    children.append(game_state)
                else:
                    print("not added")

                self.gm.reverseMove(m)
                #print("movable state")
                #print(self.gm.getGameState())
                next_child += 1

            #if ind == 1:
            #    self.gm.reverseMove(req_mov)


        if not children:
            return False

        print("all children")
        for c in children:
            print(c.state)

        return children


    def get_child(self):
        pass


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
        curr_state = curr_Gamestate.state
        self.visited[curr_Gamestate] = True
        idx = self.currentState.nextChildToVisit
        

