from __future__ import print_function
import os
import random

#a = os.popen('java bot2 1 2').read()

class Player():

    def __init__(self, source, n):
        """
        This class represents player.
        
        Args:
            * source : should be command that calls the bot in console
        """
        self.TARGET = 21
        self.SOURCE = source
        self.value = 0
        self.wins = 0
        self.penalty = 0
        self.money = n * 5
        self.bet = 0

    def testing_bot1(self):
        """
        This function represent simple testing strategy.
        It does the same thing (no matter if the role is dealer or bettor).
        """
        if self.value >= 18:
            return max(1, 5 - self.penalty)
        else:
            return 0
        
    def testing_bot2(self):
        """
        This function represent simple testing strategy.
        It does the same thing (no matter if the role is dealer or bettor).
        """
        if self.value >= 19:
            return 5
        else:
            return 0
        
    def make_decision(self, role):
        """
        This function obtain decision from AI script or testing function.
        """
        if self.SOURCE == "TEST1":
            return self.testing_bot1()
        elif self.SOURCE == "TEST2":
            return self.testing_bot2()
#        else:
#            # get response from AI
#            query = "{} {} {}".format(self.SOURCE,
#                self.bettor_value, self.value) 
#            output = os.popen(query).read()
#            # handle response
#            if not output:
#                # if empty answer
#                raise Exception("Empty bot output.")     
#            answer = int(output.split("\n")[0])
#            if answer in [0, 1]:
#                # pass the answer further
#                return(int(answer))
#            else:
#                # if answer is not correct
#                raise Exception("Bot output {} is not 0 or 1.".format(answer))
            
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
        
    def play_round(self, role):
        """
        This function simulates one round of the player.
        It rolls till AI script call stop.
        """
        done = False
        # first roll
        self.value = self.roll_dice()
        # other rolls
        while not done:
            self.penalty = self.estimate_penalty() 
            decision = self.make_decision(role)
            if decision:
                # choose bet
                done = True
                self.bet = decision
            else:
                # roll dice
                self.value += self.roll_dice()
           
 
def game_round(dealer, bettor):
    # play
    dealer.play_round("D")
    bettor.play_round("B")
    # decide
    if dealer.bet < bettor.bet:
        # dealer pass
        dealer.money -= 1
        bettor.money += 1
        return "pass"
    else:
        # game on
        if bettor.penalty < dealer.penalty:
            # bettor win
            bettor.money += bettor.bet
            dealer.money -= bettor.bet
            return "B win"
        else:
            # dealer win
            bettor.money -= bettor.bet
            dealer.money += bettor.bet
            return "D win"

N = 1000  
#PLAYER1 = 'python3 bots/bot1.py'
#PLAYER2 = 'python3 bots/bot1.py'
PLAYER1 = 'TEST1'
PLAYER2 = 'TEST2'


p1 = Player(PLAYER1, N)
p2 = Player(PLAYER2, N)



for rnd in range(N):
    if rnd % 2:
        result = game_round(dealer=p1, bettor=p2)
    else:    
        result = game_round(dealer=p2, bettor=p1)
    
    print(rnd % 2, "\t", result, "\t", p1.value, p2.value, "\t", p1.bet, p2.bet, "\t", p1.money, p2.money)

            














