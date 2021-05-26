from hashlib import new
from questions import QUESTIONS
import random


def isAnswerCorrect(question, answer): # Returns if the guessed answer by the user is correct or not

    '''
    :param question: question (Type JSON)
    :param answer:   user's choice for the answer (Type INT)
    :return:
        True if the answer is correct
        False if the answer is incorrect
    '''

    return answer == question['answer']    


def lifeLine(ques): # Removes two incorrect options and returns the question

    '''
    :param ques: The question for which the lifeline is asked for. (Type JSON)
    :return: delete the key for two incorrect options and return the new ques value. (Type JSON)
    '''
    incorrect_options = [int(x) for x in range(1, 5) if x != ques['answer']]
    choice = random.choice(incorrect_options)
    del ques['option' + str(choice)]
    del incorrect_options[incorrect_options.index(choice)]
    choice = random.choice(incorrect_options)
    del ques['option' + str(choice)]
    del incorrect_options[incorrect_options.index(choice)]
    #print(incorrect_options)
    ques['options'] = sorted([ques['answer'], incorrect_options.pop()])
    return ques
    
def isValidInput(inp): # checks for input validity
    '''
    :param inp: The input given by the user
    :return: return input validity (boolean value)
    '''
    return 1 <= inp <=4


def getMinReward(level): # returns min reward according to the level
    '''
    :param level: The level of the game
    :return: returns the amount according to the level(type int)
    '''
    if level < 6:
        return 0
    if 6 <= level < 11:
        return 10000
    return 320000

def kbc(): # main function

    print('''
        Rules to play KBC:
        * You will have 15 rounds
        * In each round, user will get a question
        * For each question, there are 4 choices out of which ONLY one is correct.
        * You will get money accoring to each round won.
        * If you are:
            1. below questions number 5, then the minimum amount rewarded is Rs. 0 (zero)
            2. As you correctly answer question number 5, the minimum reward becomes Rs. 10,000 (First level)
            3. As you correctly answer question number 11, the minimum reward becomes Rs. 3,20,000 (Second Level)
        * If the answer is wrong, then you will return with the minimum reward.
        * Type "lifeline" (case insensitive) as input, to get 50-50 lifeline.
        
        * NOTE:
            50-50 lifeline can be used ONLY ONCE.
            There is no option of lifeline for the last question( ques no. 15 ), even if you have not used it before.
        * If the user inputs "quit" (case insensitive) as input, then you will return with the amount you have won until now,
            instead of the minimum amount.
    ''')
    
    inp = ""
    while inp.lower() != "start":
        inp = input("Please type 'start' to start the game: ")
    
    print("\n\nWelcome to Kon Banega Crorepati!!!!", end="\n\n")
    total_amount = 0
    min_reward = 0
    isLifelineUsed, isGameComplete = False, False
    ques_no = 0
    lifeLineRound = -1

    while ques_no < 15:
        if 6 <= ques_no < 11:
            print("\n\n\tAap pohoch gaye hai pehle padav par!!!")
        elif ques_no >= 11:
            print("\n\n\tAap pohoch gaye hai dusre padav par!!!")
        print(f'\tQuestion {str(ques_no + 1)}: {QUESTIONS[ques_no]["name"]}' )
        print(f'\t\tOptions:')
        if ques_no == lifeLineRound:
            for opt in QUESTIONS[ques_no]['options']:
                print(f'\t\t\tOption {str(opt)}: {QUESTIONS[ques_no]["option"+str(opt)]}')
        else:
            for opt in range(1, 5):
                print(f'\t\t\tOption {str(opt)}: {QUESTIONS[ques_no]["option"+str(opt)]}')
        if not isLifelineUsed and ques_no + 1 != 15:
            print("\n\t\tLifeline Available :)",end="\n\n")
        ans = input('Your choice ( 1-4 ) :')

        if ans.lower() == 'quit':
            break
        
        if ans.lower() == 'lifeline':
            if not isLifelineUsed and ques_no + 1 != 15:
                QUESTIONS[ques_no] = lifeLine(QUESTIONS[ques_no])
                isLifelineUsed = True
                lifeLineRound = ques_no
                continue
            else:
                if isLifelineUsed:
                    print("\n\t\tLifeLine already used", end="\n\n")
                elif ques_no + 1 == 15:
                    print("\n\t\tCannot use Lifeline on Question no. 15")
                continue

        if not isValidInput(int(ans)):
            print("Please give valid input. Valid input can be Options (1-4), 'lifeline' or 'quit'\n\n")
            continue

        if isAnswerCorrect(QUESTIONS[ques_no], int(ans)):
            print('\nCorrect!')
            total_amount = QUESTIONS[ques_no]["money"]

        else:
            print('\nIncorrect !')
            total_amount = getMinReward(ques_no+1)
            break
        print("\n Current Reward : {}".format(total_amount), end="\n\n")
        ques_no += 1
    
    if ques_no == 15:
        print("\t\tCongrats, You have completed the Game :) \n")
    else:
        print("\n\nCongrats, for reaching till question {}. Better Luck Next Time!!!".format(ques_no+1),end="\n\n")
    print("\n\t\tYou won Rs. {}".format(total_amount))


#driver code

kbc()