"""
    A game state is represented by a tuple.  The leading elements of
    the tuple are the number of stones in each position, from position 0
    to the final position. The last element of the tuple is the current
    player, either 0 or 1.
    """

class MancalaGame:
    
    def __init__(self, size=6, count=4):
        self.size = size
        self.count = count
    
    def initial(self):
        """
            Return the initial game state.
            """
        return ((self.count,)*self.size + (0,))*2 + (0,)
    
    def player(self, state):
        """
            Return the current player in the given game state.
            """
        return state[-1]
    
    def actions(self, state):
        """
            Return a list of all actions available in the current game state.
            Each action is the position number of a non-empty small position
            on the current player's half of the board.
            """
        ## Finish me! ##
        actions = []
        if(state[-1] == 0):
            player_states = list(state[:self.size])
            for i,x in enumerate(player_states):
                if(x !=0):
                    actions.append(i)
        elif(state[-1] == 1):
            player_states = list(state[self.size+1:self.size*2+1])
            for i,x in enumerate(player_states):
                if(x !=0):
                    actions.append(i+(self.size +1))
        return actions
    
    
    def result(self, state, action):
        """
            Return the new game state that results from playing the given
            action in the given state.  Be sure to account for the special
            cases where a player's last stone lands in one of their own small
            positions, and when a player's last stone lands in their own mancala.
            """
       
        oldstate = list(state)
        # the number of iterations to add 1 stone to each mancala
        iter = list(range(oldstate[action]))
        for x in iter:
            # prevent player 0 adding to the player 1 mancala
            if((oldstate[-1] == 0) & (((action+x+1)% (self.size*2+2)) == ((self.size*2) + 1))):
                length = len(iter)
                iter2 = range(x+1,length+1)
                for v in iter2:
                    iter.append(v)
                x = length+1
            
            # prevent player 1 adding to player 0 mancala
            elif((oldstate[-1] == 1) & (((action+x+1)% (self.size*2+2)) == ((self.size + 1)))):
                length = len(iter)
                iter2 = range(x+1,length+1)
                for v in iter2:
                    iter.append(v)
                x = length+1
            
            # add 1 stone to the next
            else:
                oldstate[(action+x+1)% (self.size*2+2)] = oldstate[(action+x+1)% (self.size*2+2)] + 1
        # last iteration check whether the stone is in the players own mancala or opponent's
        if(x == max(iter)):
            # if the last action which is taken is in the player 0's own mancala
            if(oldstate[-1] == 0 & (((action + x + 1) % (self.size*2 + 2) ) in (range(self.size+1)))):
                # player 0 gets to play again so the state is same
                if(((action + x + 1) % (self.size*2 + 2 )) == self.size):
                    oldstate = oldstate
                # check if the state of player 0 has a 1 stone and if so takes the stones of the opposite player
                elif(((oldstate[(action+x+1)% (self.size*2+2)]) == 1)& (((action+x+1)% (self.size*2+2) != self.size)) & (((action + x + 1) % (self.size*2 + 2) ) not in (range(self.size+1,(self.size*2+2)))) ):
                    mylist = list(range(2,self.size*2+1,2))
                    mylist.reverse()
                    if( oldstate[mylist[(self.size - (action + 1))]+(self.size - (action + 1))] != 0):
                        oldstate[self.size] = oldstate[self.size] + (oldstate[(action+x+1)% (self.size*2+2)]) + oldstate[mylist[(self.size - (action + 1))]+(self.size - (action + 1))]
                        (oldstate[(action+x+1)% (self.size*2+2)]) = 0
                        oldstate[mylist[(self.size - (action + 1))]+(self.size - (action + 1))] = 0
                        oldstate[-1] = 1
                    else:
                        oldstate[-1] = 1
                # pass turn to player 1
                else:
                    oldstate[-1] = 1

            # if the last action which is taken is in the player 1's own mancala
            elif(oldstate[-1] == 1 & (((action + x + 1) % (self.size*2 + 2) ) in (range(self.size+1,(self.size*2+2))))):
                # player 1 gets to play again so the state is same
                if(((action + x + 1) % (self.size*2 + 2)) == (self.size * 2 + 1)):
                    oldstate = oldstate
                # check if the state of player 1 has a 1 stone and if so takes the stones of the opposite player
                elif(oldstate[(action+x+1)% (self.size*2+2)] == 1 & (((action + x + 1) % (self.size*2 + 2)) != (self.size * 2 + 1)) & (((action + x + 1) % (self.size*2 + 2) ) not in (range(self.size+1)))):
                    mylist = list(range(2,self.size*2+1,2))
                    if(oldstate[(self.size * 2) - (action+1)] != 0):
                        oldstate[self.size * 2 + 1] = oldstate[self.size*2 + 1] + oldstate[(action+x+1)% (self.size*2+2)] + oldstate[(self.size * 2) - (action+1)]
                        oldstate[(action+x+1)% (self.size*2+2)] = 0
                        oldstate[(self.size * 2) - (action+1)] = 0
                        oldstate[-1] = 0
                    else:
                        oldstate[-1] = 0
                #pass turn to player 0
                else:
                    oldstate[-1] = 0
            # if the last action taken lands in opponents mancala
            else:
                if(oldstate[-1] == 0):
                    oldstate[-1] = 1
                else:
                    oldstate[-1] = 0

            
        # change the number of stones left as the result of action as zero
        oldstate[action] = 0
        return tuple(oldstate)
    
    def is_over(self, state):
        """
            Return True if the game is over in the given state, False otherwise.
            The game is over if either player has no stones left in their small positions.
            """
       
        player_state1 = list(state[:self.size])
        player1 = all(v == 0 for v in player_state1)
        player_state2 = list(state[self.size+1:self.size*2+1])
        player2 = all(v == 0 for v in player_state2)
        return (player1 | player2)

    def score(self, state):
        """
            Return the score in the current state, from player 0's perspective.
            If the game is over and one player still has stones on their side,
            those stones are added to that player's score.
        """
           
        score1 = 0
        score2 = 0
        player_state1 = list(state[:self.size])
        player1 = all(v == 0 for v in player_state1)
        player_state2 = list(state[self.size+1:self.size*2+1])
        player2 = all(v == 0 for v in player_state2)
        game_over =  (player1 | player2)
        if(game_over):
            if(player1):
                score1 = state[self.size]
                for v in player_state2:
                    score2 += v
                score2 = score2 + state[self.size*2 + 1]
            elif(player2):
                score2 = state[self.size*2 + 1]
                for v in player_state1:
                    score1 += v
                score1 +=state[self.size]
        else:
            score1 = state[self.size]
            score2 = state[self.size*2 + 1]
            #add logic to check game over
        return (score1 - score2)

    def string(self, state):
        """
            Display current state as a game board.  The current player's mancala
            is marked with *.
            """
        z = self.size
        s = " ".join(["%2d"%m for m in state[-2:z:-1]] + [" *" if state[-1]==0 else "  "])
        s += "\n"
        s += " ".join(["  " if state[-1]==0 else " *"] + ["%2d"%m for m in state[:(z+1)]])
        return s

if __name__ == "__main__":
    
    """
        Scratch pad for informal tests
        """
    
    mg = MancalaGame(size=3, count=2)
    
    s = mg.initial()
    a = mg.actions(s)
    print(mg.string(s))
    print(s)
    print(a)
    print("Is over: %s"%mg.is_over(s))
    print("Utility = %d"%mg.score(s))
    print("")
    
    s = mg.result(s, 2)
    a = mg.actions(s)
    print(mg.string(s))
    print(s)
    print(a)
    print("Is over: %s"%mg.is_over(s))
    print("Utility = %d"%mg.score(s))
    print("")



