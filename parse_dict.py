import csv
import nltk
from nltk.tokenize import MWETokenizer


def init_base_order_tokenizer():
    p = nltk.PorterStemmer()
    food_tokenizer = MWETokenizer()
    food_items = {}
    prices_items = {}
    image_items = {}
    cal_items = {}
    with open('sheet1.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            food_item = row['Menu Item'].replace(' ', '_').lower()
            price = float(row['Price'])
            image = row['Image']
	    cal = float(row['Calories'])
            image_items[food_item] = image 
            food_items[food_item] = 0
            prices_items[food_item] = price
	    cal_items[food_item] = cal

            items_stem = [p.stem(i) for i in row['Menu Item'].lower().split(' ')]
            if len(items_stem) > 1:
                food_tokenizer.add_mwe(tuple(items_stem))
    
    return food_tokenizer, food_items, prices_items, cal_items, image_items

