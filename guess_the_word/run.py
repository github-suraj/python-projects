import sys
import urllib.request

try:
    urllib.request.urlopen('http://google.com')
except:
    print('No Internet Connection...')
    sys.exit(1)

import random
from word_source import WordSource
obj = WordSource()
raw_data = obj.data_dict

def guess_the_words(max_attempt, char_list_hided, cat, word, first=True):
    print(f"\nComplete the {cat[:-1]} Name : {''.join(char_list_hided)}")
    while max_attempt:
        if first:
            in_word = input("\t\t\t\tEnter your answer: ")
        else:
            in_word = input(f"Wrong Answer! {max_attempt} Attempt(s) Left, Enter your answer: ")
        if word.lower() == in_word.lower():
            print("\nCongratulations..! Your answer is correct"); break
        max_attempt -= 1
        first = False
    else:
        print(f"\nYou have lost all attemptes..! [Correct Answer is : {word}]")

def get_word_list_attempt(word):
    char_list = list(word)
    char_hide = len(char_list)//2
    max_attempt = char_hide
    char_list_hided = char_list.copy()
    for idx in range(char_hide):
        rnd_idx = random.randint(1, len(char_list))
        char_list_hided[rnd_idx-1] = '_'
    return max_attempt, char_list_hided

def select_category(raw_data_list):
    while True:
        cat = input(f"\n\t\tPlease select a Category [1 - {len(raw_data_list)+1}]: ")
        try:
            cat_idx = int(cat)
            if cat_idx == len(raw_data_list)+1:
                print('\n\tGame End! Hope you have enjoyed.'); sys.exit()
            if 1 <= cat_idx <= len(raw_data_list):
                print(f"\n\tSelected Category: {raw_data_list[cat_idx-1][0].upper()}"); break
            else:
                print(f"\tWARN : [{cat}] is not between [1 - {len(raw_data_list)+1}]")
        except ValueError:
            print(f"\tWARN : [{cat}] is not an Integer between [1 - {len(raw_data_list)+1}]")
    return raw_data_list[cat_idx-1]

def select_the_word():
    print()
    raw_data_list = [(cat, data) for cat, data in raw_data.items() if len(data) > 0]
    if len(raw_data_list) == 0:
         print('\n\tNo Words Left! Hope you have enjoyed.'); sys.exit()
    for idx, data in enumerate(raw_data_list, 1):
        print(f"\t{idx}. {data[0].upper()}", end="")
    print(f"\t{idx+1}. EXIT GAME", end="")
    cat, words = select_category(raw_data_list)
    word = words.pop(random.randint(1, len(words))-1)
    return cat, word

def main():
    while True:
        cat, word = select_the_word()
        max_attempt, char_list_hided = get_word_list_attempt(word)
        guess_the_words(max_attempt, char_list_hided, cat, word)

if __name__ == '__main__':
    main()