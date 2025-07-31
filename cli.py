# This file contains the cli front for the Connect4 game
# I expect the gui to be built on top of this. So this is really
# the core of the program

import random
from copy import deepcopy
import json

#~~~ A note on the indexing for the connect4 grid.
# the cols are indexed from 0 to 6, left to right
# while the rows can be read from -1 to -6, down to up.
random.seed(0)

class Game:
    width = 7
    height = 6
    colours = "YR"
    def __init__(self, state=None, player=None, targets=None):
        if state is None:
            state = ["" for i in range(Game.width)]
        if player is None:
            player = random.randint(0, 1)
            targets = str(player) + str(1-player)
        self.state = state
        self.player = player
        self.targets = targets
        self.winner = None
    
    def getStateTuple(self):
        return tuple(self.state)
    
    def getStateList(self):
        return deepcopy(self.state)
    
    def show(self):
        s = self.getStateTuple()
        rows = f"Current State ({Game.colours[self.player]}'s turn):\n+" + "+".join(["---" for i in range(len(s))]) + "+\n" + ("\n|" + "+".join(["---" for i in range(len(s))]) + "|\n").join([
            "| " + " | ".join([
                Game.colours[int(self.targets[int(s[i][-(Game.height-h)])])] if len(s[i]) >= (Game.height-h) else " " for i in range(len(s))
                ]) + " |" for h in range(0, Game.height)
            ]) + "\n+" + "+".join(["---" for i in range(len(s))]) + "+"
        print(rows)
    
    def makeMove(self, action):
        """
        `action` is simply the int val for the col to add the number to
        assumes action is a legal move
        """
        # print("state before", self.state)
        # print("\t", self.targets[self.player])
        self.state[action] = self.targets[self.player] + self.state[action]
        if self.someoneWins(action, self.targets[self.player]):
            print("yes", self.player, "wins. winning move: action", action)
            self.winner = self.player
        elif self.full():
            # print("fullllllll", self.fu)
            self.winner = -1
        # print("state after", self.state)
        self.player = 1-self.player
        # Also, now, invert the bits
        self.invertBits()
        self.targets = self.targets[::-1]

    def invertBits(self):
        new_cols = []
        for i in self.state:
            if i == "":
                new_cols.append(i)
                continue
            new_col = str(int("1"*len(i)) - int(i))
            new_col = "0" * (len(i) - len(new_col)) + new_col
            new_cols.append(new_col)
        self.state = new_cols

    
    def full(self):
        return all([len(i) == 6 for i in self.getStateTuple()])
    
    def otherPlayer(self):
        """returns the index of the other player"""
        return 1-self.player
    
    def otherTarget(self, target):
        return 1-target
    
    @classmethod
    def actionsFromState(self, state):
        s = Game(state=list(state), player=self.player, targets=self.targets)
        return s.actions()

    def actions(self):
        """returns all the legal moves one can make"""

        # Out of the cells which actually have space for a move,
        emptyCols = [i for i in range(len(self.state)) if len(self.state[i]) <= 5]
        #print("these are the empty cols", emptyCols)

        # Sees if there's a winning move for current_player, if yes, returns it.
        for i in emptyCols:
            if self.someoneWins(i, self.player):
                return [i]

        # otherwise, finds if there are any winning moves for the opponent, blocks them
        legality_bound = [i for i in emptyCols if self.someoneWins(i, self.otherPlayer())]
        # print("legality bound", legality_bound)
        # if len(legality_bound) > 1:
            #print("Ha! You're under a trap! Need to perform all", legality_bound, "to win")
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

    
    def someoneWins(self, action, target: str):
        """
        this program doesn't have a standard victory check algo as that's quite expensive
        instead, it sees if the `action` leads to a victory.
        Thus, it assumes that the game hadn't been won before `action`
        IDEA:
        1) starts from `action` with the vectors for NE, E, SE, S, SW, W, NW and graphs consecutive vectors
        of the same colour. if any of them have a length greater than 4, return true right away
        2) having mapped everything, sees if the conjunction of the opposites leads to a sequence >= 4
        """
        target = str(target)
        # print("seeing if", target, "wins upon action", action)
        vectors = [(1, -1), (1, 0), (1, 1)]
        action_index = (action, -(len(self.state[action])+1))
        for vector in vectors:
            dirs = [(vector, action_index), (tuple([-1*i for i in vector]), action_index)]
            chain_len = 1
            #print(vector)
            while dirs and chain_len != 4:
                current_vector = dirs.pop()  # remember this is a tuple of the vector and the index
                #print("considering vector, intial", current_vector)
                new_index = self.applyVector(*current_vector) # get the new_index by adding the vector to the index
                if new_index is None:
                    continue
                #print("\tthis is the new index", new_index)
                if self.getVal(new_index) == target:
                    #print("\t  equals target", target)
                    dirs.append((current_vector[0], new_index))
                    chain_len += 1
                #print("chain length", chain_len)
            if chain_len >= 4:
                #print("\ttrue")
                return True
        # now take care of the vector pointing downwards
        try:
            other_index = list(reversed(self.state[action])).index(str(self.otherTarget(int(target))))
            #print("\t", other_index + 1 >= 4)
            return other_index + 1 >= 4
        except ValueError:
            #print("\t", len(self.state[action]) + 1 >= 4)
            return len(self.state[action]) + 1 >= 4
    

class AI:
    def __init__(self, alpha=0.9, epsilon=0):
        self.q = {}
        self.alpha = alpha
        self.epsilon = epsilon
    
    def update_q_val(self, state: Game, action, reward, best_future, old_val):
        """Q(s, a) = Q(s, a) + alpha * [r + max(Q(s', a')) - Q(s, a)]
        -> Q(key) = Q(key) + alpha * [reward + best_future - Q(key)]
        make sure key is a tuple (immutable) as dict keys need to be immutable"""
        if best_future == 0 and reward == 0:
            return
        key = (state.getStateTuple(), action)
        self.q[key] = old_val + self.alpha * (reward + best_future - old_val)
    
    def get_q_val(self, state: Game, action, key=None):
        if key is None:
            key = (state.getStateTuple(), action)
        return self.q.get(key, 0)
    
    def update(self, state: Game, action, reward):
        """both state and action are tuples"""
        best_future = self.getBestFuture(state, action)
        old_val = self.get_q_val(state, action)
        if best_future != 0 or reward != 0:
            self.update_q_val(state, action, reward, best_future, old_val)
    
    def getBestFuture(self, state: Game, action, depth=4):
        """again, state and action are tuples"""
        if depth <= 0:
            return self.get_q_val(state, action)
        
        best = 0
        for act in state.actions():
            new_state = Game(state.getStateList(), state.player, state.targets)
            new_state.makeMove(action)
            val = self.get_q_val(new_state, act)
            if val == 0:
                val = self.getBestFuture(new_state, act, depth=depth-1)
                if val != 0:
                    self.update_q_val(new_state, act, 0, -val, 0)
            if val > best:
                best = val
        return -best
    
    def choose_action(self, state: Game, train=True):
        if not train:  # when we're playing for real:
            best = None
            best_action = None
            for action in state.actions():
                val = self.get_q_val(state, action)
                if val == 0:
                    val = self.getBestFuture(state, action)
                if best is None or val > best:
                    best = val
                    best_action = action
            return best_action
        # otherwise, explore.
        actions = [i for i in state.actions() if self.get_q_val(state, i) == 0]
        return random.choice(actions)
        

                
 

def train(n, js_out="map.json"):

    model = AI()
    
    for i in range(n):
        print("Playing Game", i)

        game = Game()

        last_moves = {
            0: {"state": None, "action": None},
            1: {"state": None, "action": None}
        }

        while True:
            print("state is:", game.getStateTuple())
            game.show()

            # choose the best move
            action = model.choose_action(game)
            print("\tchose action", action)

            # update the last move by the player
            last_moves[game.player]["state"] = deepcopy(game)
            last_moves[game.player]["action"] = action

            # and move onto the new state
            game.makeMove(action)
            # print("game after move:", game.getStateTuple())
            # print("full?", game.full(), "winner?", game.winner)
            if game.winner is not None:
                print("winner's been found:", game.player)
                # then give the last move a positive reward
                # print("these are the params:", last_moves[game.otherPlayer()]["state"],
                    # last_moves[game.otherPlayer()]["action"],
                    # 1)
                model.update(
                    last_moves[game.otherPlayer()]["state"],
                    last_moves[game.otherPlayer()]["action"],
                    1)
                # and the move before that a negative value; be careful in case the move doesn't exist
                try:
                    model.update(
                        last_moves[game.player]["state"],
                        last_moves[game.player]["action"],
                        -1
                    )
                except:
                    pass
                break
            else:   # no reward, just update (in case bestFuture exists)
                # print("general update~")
                model.update(
                    last_moves[game.otherPlayer()]["state"],
                    last_moves[game.otherPlayer()]["action"],
                    1)
    
    with open(js_out, "w") as f:
        json.dump({str(i):str(model.q[i]) for i in sorted(model.q)}, f, indent=2)
    
    return model


def play(model: AI):
    """
    Takes the model and plays the game
    """
    human = random.randint(0, 1)
    who = {human: "Human", 1-human: "AI"}
    game = Game()

    while game.winner is None:
        print("Current player:", who[game.player])
        game.show()
        if game.player == human:
            valid_moves = game.actions()
            while True:
                try:
                    x = int(input("Enter your move as an integer between 0-6 (inclusive):\n--> "))
                    if x not in valid_moves:
                        print("Invalid Move.. try again. Valid moves:", valid_moves)
                    else:
                        break
                except ValueError:
                    print("val must be an int")
            game.makeMove(x)
        else:
            move = model.choose_action(game, train=False)
            game.makeMove(move)
        
    print("Game over. game.winner", game.winner)
    if game.winner == -1:
        print("No more moves left. Good game!")
    else:
        print(who[game.winner], "Won!")







sample1 = ["00", "100", "010", "", "", "11", "001"]
x = Game(state=sample1, player=1, targets="10")
x.show()
trained = train(1)
play(trained)
# #print(x.currentTarget())
# #print(x.otherPlayer(x.currentTarget()))
# x.makeMove(3)
# #print(x.actions())
# x.invertBits()
# x.show()
