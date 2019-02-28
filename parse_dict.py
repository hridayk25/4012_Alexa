import csv
from nltk.tokenize import MWETokenizer


def build_tokenizer():
	food_tokenizer = MWETokenizer()
	with open('ChickfilAmenuitems - Sheet1.csv') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			items = row['Menu Item'].split(' ')
			if len(items) > 1:
				item_words = tuple(row['Menu Item'].lower().split(' '))
				food_tokenizer.add_mwe(item_words)
	return food_tokenizer


def initialize_base_order_dict():
	items = {}
	with open('ChickfilAmenuitems - Sheet1.csv') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			food_item = row['Menu Item'].replace(' ', '_').lower()
			items[food_item] = 0
	return items

initialize_base_order_dict()