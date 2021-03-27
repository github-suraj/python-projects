import requests
from bs4 import BeautifulSoup

class WordSource:
    fruits = "https://www.halfyourplate.ca/fruits-and-veggies/fruits-a-z/"
    veggies = "https://www.halfyourplate.ca/fruits-and-veggies/veggies-a-z/"
    flowers1 = "https://www.flyingflowers.co.uk/page/flower_names_and_origins/"
    flowers2 = "https://7esl.com/flowers-vocabulary/"
    def __init__(self):
        self.data_dict = dict()
        self.data_dict['fruits'] = self.__get_data_list(self.fruits)
        self.data_dict['veggies'] = self.__get_data_list(self.veggies)
        self.data_dict['flowers'] = self.__get_flowers1_list(self.flowers1)
        self.data_dict['flowers'].extend(self.__get_flowers2_list(self.flowers2))

    def __get_flowers2_list(self, url):
        resp = requests.get(url)
        content = resp.content
        soup = BeautifulSoup(content, features="html.parser")
        d_all = soup.find("div", attrs={"class": "thecontent clearfix"})
        ul_all = d_all.findAll("ul", attrs={"class": ""})
        data_list = [d.text for d in ul_all[-2].findAll("li")]
        data_list.sort()
        return data_list

    def __get_flowers1_list(self, url):
        resp = requests.get(url)
        content = resp.content
        soup = BeautifulSoup(content, features="html.parser")
        d_all = soup.findAll("div", attrs={"class": "ipbBlogTempPagetextR"})
        data_list = [d.findAll("h3")[-1].text for d in d_all]
        data_list.sort()
        return data_list

    def __get_data_list(self, url):
        resp = requests.get(url)
        content = resp.content
        soup = BeautifulSoup(content, features="html.parser")
        d = soup.find("ul", attrs={"class": "fv-list"})
        data_list = [li.findAll("a")[-1].text for li in d.findAll("li")]
        data_list.sort()
        return data_list

"""
def main(minL=10, maxL=15):
    from random_word import RandomWords
    from PyDictionary import PyDictionary
    r = RandomWords()
    word_list = r.get_random_words(minLength=minL, maxLength=maxL)
    print(word_list)
    dictionary = PyDictionary()
    for word in word_list[:5]:
        print(dictionary.synonym(word.title()))
        print(dictionary.antonym(word.title()))
        print(dictionary.meaning(word.title()))
"""