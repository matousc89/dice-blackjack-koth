from __future__ import print_function
import os
import random

#a = os.popen('java bot2 1 2').read()

class Player():

    def __init__(self, source, name, n):
        """
        This class represents player.
        
        Args:
            * source : should be command that calls the bot in console
        """
        self.NAME = name
        self.TARGET = 21
        self.MAX_BET = 5
        self.SOURCE = source
        self.value = 0
        self.wins = 0
        self.penalty = 0
        self.money = n * self.MAX_BET
        self.rolls_count = 1
        
    def place_bet(self, role, oponent_count):
        """
        This function contact the bettor to get the demanded bet.
        Bet must be an integer in allowed range.
        """
        args = [
                "PLACE", self.value, self.rolls_count, oponent_count
                ]
        # testing bot 1
        if self.SOURCE == "TEST1":
            bet = self.testing_bot1(args)
        # testing bot 2
        elif self.SOURCE == "TEST2":
            bet = self.testing_bot2(args)
        # check if the bet is valid
        bet = int(bet)
        if 0 <= bet <= self.MAX_BET:
            return bet
        else:
            raise Exception("The place bet get invalid answer.")

    def answer_bet(self, role, oponent_count, oponent_bet):
        args = [
                "ANSWER", self.value, self.rolls_count, oponent_count,
                oponent_bet
                ]
        # testing bot 1
        if self.SOURCE == "TEST1":
            answer = self.testing_bot1(args)
        # testing bot 2
        if self.SOURCE == "TEST2":
            answer = self.testing_bot2(args)
        # check if the answer is valid
        answer = int(answer)
        if answer in [0, 1]:
            return answer
        else:
            raise Exception("The answer for bet must be integer 0 or 1.")


    def make_decision(self, role):
        """
        This function obtain decision from AI script or testing function.
        """
        args = [
            "ROLL", self.value, role
            ]
        # testing bot 1
        if self.SOURCE == "TEST1":
            return int(self.testing_bot1(args))
        # testing bot 2
        if self.SOURCE == "TEST2":
            return int(self.testing_bot2(args))
            
            
#        elif self.SOURCE == "TEST2":
#            return self.testing_bot2()
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
        self.rolls_count = 1
        # first roll
        self.value = self.roll_dice()
        # other rolls
        while not done:
            self.penalty = self.estimate_penalty() 
            decision = self.make_decision(role)
            if not decision:
                done = True
            else:
                # roll dice
                self.rolls_count += 1
                self.value += self.roll_dice()
           
    def testing_bot1(self, argv):
        """
        This function represent simple testing strategy.
        """
        TASK = argv[0]
        VALUE = int(argv[1])
        if TASK == "PLACE":   
            MY_COUNT = int(argv[2])
            OP_COUNT = int(argv[3])
            # decide how much bet as bettor  
            return max(1, 21-VALUE)            
        if TASK == "ANSWER":
            MY_COUNT = int(argv[2])
            OP_COUNT = int(argv[3])
            OP_BET = int(argv[4])
            # decide whether to accept the bet or not
            acceptable = max(1, 21-VALUE) 
            return 1 if acceptable >= OP_BET else 0 
        elif TASK == "ROLL":
            ROLE = argv[1]   
            # decide whether to roll or not     
            if VALUE >= 18:
                return 0
            else:
                return 1
        
    def testing_bot2(self, argv):
        """
        This function represent simple testing strategy.
        """
        TASK = argv[0]
        VALUE = int(argv[1])
        if TASK == "PLACE":   
            MY_COUNT = int(argv[2])
            OP_COUNT = int(argv[3])
            # decide how much bet as bettor  
            return max(1, 21-VALUE)            
        if TASK == "ANSWER":
            MY_COUNT = int(argv[2])
            OP_COUNT = int(argv[3])
            OP_BET = int(argv[4])
            # decide whether to accept the bet or not
            acceptable = max(1, 21-VALUE) 
            return 1 if acceptable >= OP_BET else 0 
        elif TASK == "ROLL":
            ROLE = argv[1]   
            # decide whether to roll or not     
            if VALUE >= 18:
                return 0
            else:
                return 1

 
def game_round(dealer, bettor):
    # play
    dealer.play_round("D")
    bettor.play_round("B")
    # make bet
    bet = bettor.place_bet("B", dealer.rolls_count)
    answer = dealer.answer_bet("D", bettor.rolls_count, bet)
    # decide winner
    if answer:
        if bettor.penalty < dealer.penalty:
            # bettor win
            bettor.money += bet
            dealer.money -= bet
            return "B win"
        else:
            # dealer win
            bettor.money -= bet
            dealer.money += bet
            return "D win"
    else:
        dealer.money -= 1
        bettor.money += 1
        return "pass"
        


N = 1000
#PLAYER1 = 'python3 bots/bot1.py'
#PLAYER2 = 'python3 bots/bot1.py'
PLAYER1 = 'TEST1'
PLAYER2 = 'TEST2'


p1 = Player(PLAYER1, "P1", N)
p2 = Player(PLAYER2, "P2", N)



for rnd in range(N):
    if rnd % 2:
        result = game_round(dealer=p2, bettor=p1)
    else:    
        result = game_round(dealer=p1, bettor=p2)
    
    print("P"+str(rnd % 2 + 1), "\t", result, "\t", p1.value, p2.value, "\t", "\t", p1.money, p2.money)

            














