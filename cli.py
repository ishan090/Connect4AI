# This file contains the cli front for the Connect4 game
# I expect the gui to be built on top of this. So this is really
# the core of the program

import random


class Game:
    width = 7
    height = 6
    def __init__(self, state=None):
        if state is None:
            state = [[] for i in range(Game.width)]
        self.state = state
    
    def getStateTuple(self):
        return tuple([tuple(i) for i in self.state])
    
    def show(self):
        s = self.getStateTuple()
        rows = "Current State:\n+" + "+".join(["---" for i in range(len(s))]) + "+\n" + ("\n|" + "+".join(["---" for i in range(len(s))]) + "|\n").join([
            "| " + " | ".join([
                s[i][-(Game.height-h)] if len(s[i]) >= (Game.height-h) else " " for i in range(len(s))
                ]) + " |" for h in range(0, Game.height)
            ]) + "\n+" + "+".join(["---" for i in range(len(s))]) + "+"
        print(rows)


x = Game(state=[["R" for i in range(random.randint(0, 4))] for j in range(7)])
x.show()
