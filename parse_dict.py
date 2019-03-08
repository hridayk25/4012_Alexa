import csv
from nltk.tokenize import MWETokenizer


def init_base_order_tokenizer():
    food_tokenizer = MWETokenizer()
    items = {}
    with open('ChickfilAmenuitems - Sheet1.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            food_item = row['Menu Item'].replace(' ', '_').lower()
            items[food_item] = 0
            items = row['Menu Item'].split(' ')
            if len(items) > 1:
                item_words = tuple(row['Menu Item'].lower().split(' '))
                food_tokenizer.add_mwe(item_words)
    return food_tokenizer, items