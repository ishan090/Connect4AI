# This file contains the cli front for the Connect4 game
# I expect the gui to be built on top of this. So this is really
# the core of the program

import random

#~~~ A note on the indexing for the connect4 grid.
# the cols are indexed from 0 to 6, left to right
# while the rows can be read from -1 to -6, down to up.


class Game:
    width = 7
    height = 6
    colours = "RY"
    def __init__(self, state=None, player=None):
        if state is None:
            state = [[] for i in range(Game.width)]
        if player is None:
            player = 0
        self.state = state
        self.player = player
        self.winner = None
    
    def getStateTuple(self):
        return tuple([tuple(i) for i in self.state])
    
    def show(self):
        s = self.getStateTuple()
        rows = f"Current State ({Game.colours[self.player]}'s turn):\n+" + "+".join(["---" for i in range(len(s))]) + "+\n" + ("\n|" + "+".join(["---" for i in range(len(s))]) + "|\n").join([
            "| " + " | ".join([
                s[i][-(Game.height-h)] if len(s[i]) >= (Game.height-h) else " " for i in range(len(s))
                ]) + " |" for h in range(0, Game.height)
            ]) + "\n+" + "+".join(["---" for i in range(len(s))]) + "+"
        print(rows)
    
    def makeMove(self, action):
        """
        `action` is simply the int val for the col to add the number to
        assumes action is a legal move
        """
        self.state[action] = [Game.colours[self.player]] + self.state[action]
    
    def otherPlayer(self, target):
        """given the target for one of the players, returns the other target"""
        assert target in Game.colours, f"target {target} invalid"
        return Game.colours[1-Game.colours.index(target)]
    
    def currentTarget(self):
        return Game.colours[self.player]

    def actions(self):
        """returns all the legal moves one can make"""
        # Sees if there's a winning move, if yes, returns it.
        

        emptyCols = [i for i in range(len(self.state)) if len(self.state[i]) <= 5]
        print("these are the empty cols", emptyCols)

        for i in emptyCols:
            if self.someoneWins(i, self.currentTarget()):
                return [i]

        legality_bound = [i for i in emptyCols if self.someoneWins(i, self.otherPlayer(self.currentTarget()))]
        print("legality bound", legality_bound)
        if len(legality_bound) > 1:
            print("Ha! You're under a trap! Need to perform all", legality_bound, "to win")
        if len(legality_bound):
            return legality_bound
        else:
            # No legality bound moves
            return emptyCols


    def getVal(self, index):
        """given an index, gets the val associated with it or None.
        expects index[1] to be a negative value ranging from -1 to -6"""
        s = self.getStateTuple()
        try:
            return s[index[0]][index[1]] if len(s[index[0]]) >= -index[1] else None
        except IndexError:
            return None
    
    def applyVector(self, vector, state):
        """applies `vector` on `state` and returns the new state as a tuple"""
        new_index = tuple([sum(i) for i in zip(vector, state)])
        if new_index[0] < 0 or new_index[0] > 6 or new_index[1] > -1 or new_index[1] < -6:
            return None
        return new_index

    
    def someoneWins(self, action, target):
        """
        this program doesn't have a standard victory check algo as that's quite expensive
        instead, it sees if the `action` leads to a victory.
        Thus, it assumes that the game hadn't been won before `action`
        IDEA:
        1) starts from `action` with the vectors for NE, E, SE, S, SW, W, NW and graphs consecutive vectors
        of the same colour. if any of them have a length greater than 4, return true right away
        2) having mapped everything, sees if the conjunction of the opposites leads to a sequence >= 4
        """
        print("seeing if", target, "wins upon action", action)
        vectors = [(1, -1), (1, 0), (1, 1)]
        action_index = (action, -(len(self.state[action])+1))
        for vector in vectors:
            dirs = [(vector, action_index), (tuple([-1*i for i in vector]), action_index)]
            chain_len = 1
            print(vector)
            while dirs and chain_len != 4:
                current_vector = dirs.pop()  # remember this is a tuple of the vector and the index
                print("considering vector, intial", current_vector)
                new_index = self.applyVector(*current_vector) # get the new_index by adding the vector to the index
                if new_index is None:
                    continue
                print("\tthis is the new index", new_index)
                if self.getVal(new_index) == target:
                    print("\t  equals target", target)
                    dirs.append((current_vector[0], new_index))
                    chain_len += 1
                print("chain length", chain_len)
            if chain_len >= 4:
                print("\ttrue")
                return True
        # now take care of the vector pointing downwards
        try:
            other_index = list(reversed(self.state[action])).index(Game.colours[1-Game.colours.index(target)])
            print("\t", other_index + 1 >= 4)
            return other_index + 1 >= 4
        except ValueError:
            print("\t", len(self.state[action]) + 1 >= 4)
            return len(self.state[action]) + 1 >= 4


sample1 = [['Y', 'Y'], ['R', 'Y', 'Y'], ['Y', 'R', 'Y'], [], [], ['R', 'R'], ['Y', 'Y', 'R']]
x = Game(state=sample1, player=1)
x.show()
# print(x.currentTarget())
# print(x.otherPlayer(x.currentTarget()))
# x.makeMove(3)
print(x.actions())
