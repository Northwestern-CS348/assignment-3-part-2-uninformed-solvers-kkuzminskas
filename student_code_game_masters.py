from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        KB = self.kb

        
        # find all disks on pegs 1-3
        pegs = ["peg1", "peg2", "peg3"]

        # final game state tuple list
        game_state = []

        for peg in pegs:
            disks = KB.kb_ask(parse_input("fact: (on ?disk " + peg + ")"))

            peg_tuple = []

            if disks:
                for d in disks:
                    str_disk = str(d.bindings[0].constant)
                    order_binding = self.kb.kb_ask(parse_input("fact: (size_order " + str_disk + " ?order"))
                    disk_size_order = int(str(order_binding[0].bindings[0].constant))
                    peg_tuple.append(disk_size_order)
                peg_tuple.sort()

            game_state.append(tuple(peg_tuple))

        return tuple(game_state)
            


        



    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        KB = self.kb

        predicate = movable_statement.predicate
        
        # check to make sure it is a movable statement
        if predicate != "movable":
            print("Error: Given statement is not a movable statement")
            return


        terms = movable_statement.terms
        disk = terms[0]
        curr_peg = terms[1]
        target_peg = terms[2]

        # retract all facts from the KB that are involved with the disk being on that peg
        related_predicates = ["on", "top"]

        for pred in related_predicates:
            # remove facts from the KB related with that
            fact_remove = parse_input("fact: (" + str(pred) + " " + str(disk) + " " + str(curr_peg) + ")")
            KB.kb_retract(fact_remove)
            

        # change the new top of the current peg
        disk_base_under_move = KB.kb_ask(parse_input("fact: (ontop " + str(disk) + " ?d)"))
        str_new_top = str(disk_base_under_move[0].bindings[0].constant)
        
        fact_add = parse_input("fact: (top " + str_new_top + " " + str(curr_peg) + ")")
        KB.kb_assert(fact_add)

        # remove the ontop of fact
        fact_remove = parse_input("fact: (ontop " + str(disk) + " " + str_new_top + ")")
        KB.kb_retract(fact_remove)

    
        ## add new facts to the KB that are involved with the disk being on the target peg
        # add that the disk is on the target peg
        fact_add = parse_input("fact: (on "  + str(disk) + " " + str(target_peg) + ")")
        KB.kb_assert(fact_add)

        # find the current top of the target peg
        fact_ask = parse_input("fact: (top ?d " + str(target_peg) + ")")
        target_top = KB.kb_ask(fact_ask)
        str_top = str(target_top[0].bindings[0].constant)
        
        # remove the current top of the target peg
        KB.kb_retract(parse_input("fact: (top " + str_top + " " + str(target_peg) + ")"))

        
        # make the disk ontop of the previous top
        fact_add = parse_input("fact: (ontop " + str(disk) + " " + str_top + ")")
        KB.kb_assert(fact_add)

        # make the new top of the target
        KB.kb_assert(parse_input("fact: (top " + str(disk) + " " + str(target_peg) + ")"))

        disks = KB.kb_ask(parse_input("fact: (on ?disk " + str(target_peg) + ")"))
        return
        




    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### Student code goes here
        pass

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        pass

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
