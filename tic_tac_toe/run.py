import os
from time import sleep
from random import randint, choice
from operator import itemgetter
from termcolor import colored
from tabulate import tabulate

global board
global players; players = list()
global computer; computer = False
global level; level = 1
symbols = ('X', 'O')
combinations = ((0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6))

os.system('color')
_color = {'X': 'green', 'O': 'magenta'}
_colored = lambda n: colored(n, _color.get(n, 'white'), attrs=['bold'])
_print = lambda ttl: print(f"\n{ttl.center(50, '-')}\n")

def final_score():
    colums = ('name', 'symbol', 'won', 'draw')
    data = [[p[col] for col in colums] for p in players]
    print(tabulate(data, headers=colums, tablefmt='psql'))
    p1, p2 = players
    winner = p1['name'] if p1['won'] > p2['won'] else p2['name'] if p1['won'] < p2['won'] else None
    if winner:
        print(f"\nCongratulations {winner}!, You have won the Game.")
    else:
        print("\nHurrah! Its a Tie.")

def check_winning(win=False):
    for comb in combinations:
        comb_set = set(itemgetter(*comb)(board))
        if len(comb_set) == 1:
            win = True
    return win

def level_based_position(sym_p):
    available_nums = [n for n in board if isinstance(n, int)]
    if level == 1: # Easy
        return choice(available_nums) ## random.choice
    prefer_position = (5, 1, 3, 7, 9, 2, 4, 6, 8)
    if level == 3: # Hard
        if (board[0] == board[8] == sym_p) or (board[2] == board[6] == sym_p):
             prefer_position = (5, 2, 4, 6, 8, 1, 3, 7, 9)
    for pos in prefer_position:
        if pos in available_nums:
            return pos

def computer_input(p):
    print("\nComputer's turn..."); sleep(level)
    sym_c = p['symbol']
    sym_p = [sym for sym in symbols if sym != sym_c][-1]
    ## If Computer Can Win
    for comb_set in combinations:
        comb = itemgetter(*comb_set)(board)
        s = len(set(symbols).intersection(set(comb)))
        if s == 1 and comb.count(sym_c) == 2:
            return list(set(comb).difference(set(symbols)))[-1]
    ## If Player Can Win
    for comb_set in combinations:
        comb = itemgetter(*comb_set)(board)
        s = len(set(symbols).intersection(set(comb)))
        if s == 1 and comb.count(sym_p) == 2:
            return list(set(comb).difference(set(symbols)))[-1]
    return level_based_position(sym_p)

def user_input(p):
    available_nums = [n for n in board if isinstance(n, int)]
    try:
        n = int(input(f"\n{p['name']}, Enter a number on the board: "))
        if n > len(board) or n < 0 or n not in available_nums:
            print(f"\tInCorrect Input, Try again! Available places {available_nums}")
            user_input(p)
        else:
            board[n-1] = p['symbol']
    except:
        print(f"\tInCorrect Input, Try again! Available places {available_nums}")
        user_input(p)

def show_board():
    print()
    for i in range(3):
        a, b, c = board[i*3: (i+1)*3]
        print(f"\t {_colored(a)} | {_colored(b)} | {_colored(c)} ")
        if i < 2:
            print('\t---+---+---')

def play_game(p1, p2):
    player_turns = [p1 if i%2 == 0 else p2 for i in range(len(board))]
    for idx, p in enumerate(player_turns):
        if idx % 2 == 0:
            user_input(p)
        elif computer:
            n = computer_input(p)
            board[n-1] = p['symbol']
        else:
            user_input(p)
        show_board()
        win = check_winning()
        if win:
            _print(f" {p['name']} heve won the match ")
            for P in players:
                if P['name'] == p['name']:
                    P['won'] += 1
            break
    else:
        for player in players:
            player['draw'] += 1
        _print(' Match DRAW ')

def start_game(rpi=0): # rpi=0, Only player will start game
    global board
    board = list(range(1, 10))
    _players = players.copy()
    if not computer:
        rpi = randint(0, 1) # Random player will start game
    player1 = _players.pop(rpi)
    player2 = _players.pop()
    print(f"\n{player1['name']} will start the game!")
    show_board()
    play_game(player1, player2)

def initialize_computer_mode():
    global level
    print("\t1. Easy (Beginner)\n\t2. Medium (Normal)\n\t3. Hard (Impossible)\n")
    while True:
        try:
            level = int(input("Choose difficulty level: "))
            if level not in (1, 2, 3):
                print(colored("\tPlease enter either 1, 2 or 3,", 'red'), 'Try Again!')
                continue
            break
        except:
            print(colored("\tPlease enter either 1, 2 or 3,", 'red'), 'Try Again!')
    player = str(input("\nEnter Your Name: "))
    players.append({'name': player, 'won': 0, 'draw': 0})
    players.append({'name': 'Computer', 'won': 0, 'draw': 0})

def initialize_game(rpi=0): # rpi=0, Only player will select Symbol
    if computer:
        initialize_computer_mode()
    else:
        for i in range(2):
            player = str(input(f"Enter Player {i+1} Name: "))
            players.append({'name': player, 'won': 0, 'draw': 0})
        rpi = randint(0, 1) # Random player will select Symbol

    common = ([0, 1], list(symbols))
    while True:
        symbol = str(input(f"\t{players[rpi]['name']}: Select your symbol of choice (X / O): "))
        if symbol in symbols:
            players[common[0].pop(rpi)]['symbol'] = common[1].pop(symbols.index(symbol))
            players[common[0].pop()]['symbol'] = common[1].pop()
            break
        else:
            print("\t\tInCorrect Input, Try again!")

def choose_mode():
    global computer
    _print(" Welcome to Tic Tac Toe Game ")
    print("\t1. Play with computer\n\t2. Play with friend\n")
    while True:
        mode = input("Choose a Mode: ")
        try:
            if int(mode) not in (1, 2):
                print(colored("\tPlease enter either 1 or 2,", 'red'), 'Try Again!')
                continue
            if int(mode) == 1:
                computer = True
                _print(" You will be playing with Computer ")
            else:
                _print(" You will be playing with Friend ")
            break
        except:
            print(colored("\tPlease enter either 1 or 2,", 'red'), 'Try Again!')

def main():
    choose_mode()
    initialize_game()
    while True:
        start_game()
        while True:
            reset = str(input("Do you want to play again (Y / N): "))
            if reset not in ('Y', 'N'):
                print("\tInCorrect Input, Try again!")
            elif reset == 'Y':
                break
            else:
                _print(" FINAL SCORE ")
                final_score()
                return

if __name__ == '__main__':
    main()