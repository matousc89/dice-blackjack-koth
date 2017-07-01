from __future__ import print_function
import os
import random

#a = os.popen('java bot2 1 2').read()

class Player():

    def __init__(self, source):
        """
        This class represents player.
        
        Args:
            * source : should be command that calls the bot in console
        """
        self.TARGET = 21
        self.SOURCE = source
        self.role = False
        self.value = 0
        self.bettor_value = 0
        self.wins = 0
        self.penalty = 0

    def testing_bot(self):
        """
        This function represent simple testing strategy.
        It does the same thing (no matter if the role is dealer or bettor).
        """
        if self.value > 18:
            return 0
        elif self.value > 15:
            return random.getrandbits(1)
        else:
            return 1
        
    def testing_bot2(self):
        """
        This function represent simple testing strategy.
        It does the same thing (no matter if the role is dealer or bettor).
        """
        if self.value > 19:
            return 0
        elif self.value > 15:
            return random.getrandbits(1)
        else:
            return 1
        
    def make_decision(self):
        """
        This function obtain decision from AI script or testing function.
        """
        if self.SOURCE == "TEST1":
            return self.testing_bot()
        elif self.SOURCE == "TEST2":
            return self.testing_bot2()
        else:
            # get response from AI
            query = "{} {} {}".format(self.SOURCE,
                self.bettor_value, self.value) 
            output = os.popen(query).read()
            # handle response
            if not output:
                # if empty answer
                raise Exception("Empty bot output.")     
            answer = int(output.split("\n")[0])
            if answer in [0, 1]:
                # pass the answer further
                return(int(answer))
            else:
                # if answer is not correct
                raise Exception("Bot output {} is not 0 or 1.".format(answer))
            
    def roll_dice(self):
        """
        This function simulate a roll of fair six-sided dice.
        Integer 1-6 is returned.
        """
        return random.randint(1,6)
 
    def estimate_penalty(self):
        """ 
        This function measures penalty.
        """
        if self.value > self.TARGET:
            return 100
        else:
            return self.TARGET - self.value 
        
    def play_round(self):
        """
        This function simulates one round of the player.
        It rolls till AI script call stop.
        """
        self.done = False
        self.value = 0
        # bettor game
        if self.role == "B":
            # first roll
            if not self.value:
                self.value += self.roll_dice()
            # other rolls
            while self.value < self.TARGET and not self.done:
                decision = self.make_decision()
                if decision == 0:
                    self.done = True
                else:
                    self.value += self.roll_dice()
        # dealer game
        else:
            # first roll
            if not self.value:
                self.value += self.roll_dice()
            # other rolls
            while self.value < 17 and not self.done:
                decision = self.make_decision()
                if decision == 0:
                    self.done = True
                else:
                    self.value += self.roll_dice()
        # estimate penalty
        self.penalty = self.estimate_penalty()      
 

N = 10000    
#PLAYER1 = 'python3 bots/bot1.py'
#PLAYER2 = 'python3 bots/bot1.py'
PLAYER1 = 'TEST1'
PLAYER2 = 'TEST2'


p1 = Player(PLAYER1)
p2 = Player(PLAYER2)

## player1 is bettor
p1.role = "B"
p2.role = "D"
for rnd in range(N):
    p1.play_round()
    p2.bettor_value = p1.value
    p2.play_round()
    # decide winner
    if p1.penalty < p2.penalty:
        p1.wins += 1
        winner = "P1"
    else:
        p2.wins += 1
        winner = "P2"
    
## player1 is bettor
p1.role = "D"
p2.role = "B"
for rnd in range(N):
    p2.play_round()
    p1.bettor_value = p2.value
    p1.play_round()
    # decide winner
    if p2.penalty < p1.penalty:
        p2.wins += 1
        winner = "P2"
    else:
        p1.wins += 1
        winner = "P1"
   
# output results  
print(p1.wins, p2.wins)









