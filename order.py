import nltk
from nltk.tokenize import MWETokenizer
import parse_dict
import string

class Order:
    def __init__(self):
        self.foodTokenizer, self.items = parse_dict.init_base_order_tokenizer()

    def addFromText(self,text):
        stopWords = nltk.corpus.stopwords.words()
        unit_number = {'0':0, '1':1, '2':2,'to':2, '3':3, '4':4, 
                   '5':5 , '6':6, '7':7, '8':8, '9':9,
                   '10':10, '11':11, '12':12, '13':13,
                   '14':14, '15':15, '16':16, '17':17,
                   '18':18, '19':19, '20':20}
        synonyms = {'lemonad':'lemonade', 'milkshak':'milkshake','fri':'fries',
                    'spici':'spicy', 'spici_chicken_sandwich': 'spicy_chicken_sandwich',
                    'origin_chicken_sandwich': 'chicken_sandwich'}

        foodTokenizer = self.foodTokenizer
        tokenizedOrder = foodTokenizer.tokenize(self.stripAndStemText(text))
        tokenizedOrder.reverse()
        i = 0
        for t in tokenizedOrder:
            if t in self.items:
                try:
                    self.items[t] += int(tokenizedOrder[i+1])
                except:
                    self.items[t] += 1
            elif t in synonyms:
                try:
                    self.items[synonyms[t]] += int(tokenizedOrder[i+1])
                except:
                    self.items[synonyms[t]] += 1
            i+=1


    def stripAndStemText(self,text):
        p = nltk.PorterStemmer()
#         res = text.translate(None, string.punctuation)
        res = text
        res = [p.stem(i) for i in res.split()]
        return res

    def printOrder(self):
        res = ""

        for item in self.items:
            if self.items[item] != 0:
                res = res + " " + str(self.items[item]) + " " + item.replace("_"," ") + " and"
        return res[:-3]