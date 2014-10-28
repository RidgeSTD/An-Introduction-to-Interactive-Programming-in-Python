# Rock-paper-scissors-lizard-Spock template


# The key idea of this program is to equate the strings
# "rock", "paper", "scissors", "lizard", "Spock" to numbers
# as follows:
#
# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors

# helper functions

import random

def name_to_number(name):
    if name=='rock':
        return 0
    elif name=='Spock':
        return 1
    elif name=='paper':
        return 2
    elif name=='lizard':
        return 3
    else:
        return 4
        


def number_to_name(number):
    if number==0:
        return 'rock'
    elif number==1:
        return 'Spock'
    elif number==2:
        return 'paper'
    elif number==3:
        return 'lizard'
    else:
        return 'scissors'
    

def rpsls(player_choice):
    judge_arr=[0,-1,-1,1,1],[1,0,-1,-1,1],[1,1,0,-1,-1],[-1,1,1,0,-1],[-1,-1,1,1,0]
    print('\n')
    # print out the message for the player's choice
    print('Player chooses '+player_choice+'\n')
    # convert the player's choice to player_number using the function name_to_number()
    p_num = name_to_number(player_choice)
    # compute random guess for comp_number using random.randrange()
    c_num = int(random.randrange(0,5))
    # convert comp_number to comp_choice using the function number_to_name()
    comp_choice = number_to_name(c_num)
    # print out the message for computer's choice
    print('Computer chooses '+comp_choice+'\n')
    # use if/elif/else to determine winner, print winner message
    if judge_arr[p_num][c_num]>0:
        print('Player wins!\n')
    elif judge_arr[p_num][c_num]==0:
        print('Player and computer tie!\n')
    else:
        print('Computer wins!\n')

    
# test your code - THESE CALLS MUST BE PRESENT IN YOUR SUBMITTED CODE
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")

# always remember to check your completed program against the grading rubric


