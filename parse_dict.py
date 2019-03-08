import csv
from nltk.tokenize import MWETokenizer


def init_base_order_tokenizer():
    food_tokenizer = MWETokenizer()
    food_items = {}
    with open('sheet1.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            food_item = row['Menu Item'].replace(' ', '_').lower()
            food_items[food_item] = 0
            items = row['Menu Item'].split(' ')
            if len(items) > 1:
                item_words = tuple(row['Menu Item'].lower().split(' '))
                food_tokenizer.add_mwe(item_words)
    return food_tokenizer, food_items