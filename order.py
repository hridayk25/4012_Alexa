import nltk
from nltk.tokenize import MWETokenizer
import parse_dict
import string

class Order:
    def __init__(self):
        self.items = parse_dict.initialize_base_order_dict()

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

        foodTokenizer = self.instantiateTokenizer()
        tokenizedOrder = foodTokenizer.tokenize(self.stripAndStemText(text))

        finalOrder = []
        for t in tokenizedOrder:
            if t in unit_number:
                print t
                finalOrder.append(unit_number[t])
            elif t in synonyms:
                if(len(finalOrder)>0 and type(finalOrder[-1])!=int):
                    finalOrder.append(1)
                finalOrder.append(synonyms[t])
            elif t not in stopWords:
                finalOrder.append(1)
                finalOrder.append(t)
        finalOrder.reverse()
        print finalOrder
        i = 0  
        while i < len(finalOrder):
            try:
                self.items[finalOrder[i]] += finalOrder[i+1]
                i+=2
            except:
                i+=1
                pass

    def instantiateTokenizer(self):
        # foodTokenizer = MWETokenizer()
        # foodTokenizer.add_mwe(('origin','chicken', 'sandwich'))
        # foodTokenizer.add_mwe(('chicken', 'sandwich'))
        # foodTokenizer.add_mwe(('spici','chicken', 'sandwich'))
        # foodTokenizer.add_mwe(('chicken', 'biscuit'))
        # foodTokenizer.add_mwe(('chicken', 'nugget'))
        # foodTokenizer.add_mwe(('chicken', 'nugget'))
        # foodTokenizer.add_mwe(('hash', 'browns'))
        # foodTokenizer.add_mwe(('fruit', 'cup'))
        # return foodTokenizer
        return parse_dict.build_tokenizer()


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