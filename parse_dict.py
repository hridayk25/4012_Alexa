import csv
import nltk
from nltk.tokenize import MWETokenizer


def init_base_order_tokenizer():
    p = nltk.PorterStemmer()
    food_tokenizer = MWETokenizer()
    food_items = {}
    with open('sheet1.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            food_item = row['Menu Item'].replace(' ', '_').lower()
            food_items[food_item] = 0

            items_stem = [p.stem(i) for i in row['Menu Item'].lower().split(' ')]
            if len(items_stem) > 1:
                food_tokenizer.add_mwe(tuple(items_stem))
    
    return food_tokenizer, food_items