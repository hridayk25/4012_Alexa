import nltk
from nltk.tokenize import MWETokenizer
import parse_dict
import re
import string
import sys
## cannot handle waffle fries
class Order:
    def __init__(self):
        self.foodTokenizer, self.items = parse_dict.init_base_order_tokenizer()
        self.unit_number = {'to': 2, 'too': 2, 'for': 4, 'all': sys.maxint}
        self.synonyms = {'lemonad': 'lemonade', 'milkshak': 'vanilla_milkshake', 'fri': 'waffle_potato_fries',
                    'spici_chicken_sandwich': 'spicy_chicken_sandwich',
                    'grill_cool_wrap': 'grilled_cool_wrap',
                    'origin_chicken_sandwich': 'chicken_sandwich',
                    'spici_southwest_salad': 'spicy_southwest_salad',
                    'waffl_potato_fri': 'waffle_potato_fries',
                    'waffl_fri': 'waffle_potato_fries',
                    'waffl_potato_chip': 'waffle_potato_chips',
                    'chocol_milkshak': 'chocolate_milkshake',
                    'cooki_and_cream_milkshak': 'cookies_and_cream_milkshake',
                    'grill_chicken_club': 'grilled_chicken_club',
                    'chicken_strip': 'chicken_strips',
                    'chicken_mini': 'chicken_minis',
                    'bacon_egg_and_chees_biscuit': 'bacon_egg_and_cheese_biscuit',
                    'sausag_egg_and_chees_biscuit': 'sausage_egg_and_cheese_biscuit',
                    'bacon_egg_and_chees_muffin': 'bacon_egg_and_cheese_muffin',
                    'sausag_egg_and_chees_muffin': 'sausage_egg_and_cheese_muffin',
                    'butter_biscuit': 'buttered_biscuit',
                    'hash_brown': 'hash_browns',
                    'chicken_egg_and_chees_bagel': 'chicken_egg_and_cheese_bagel',
                    'sunflow_multigrain_bagel': 'sunflower_multigrain_bagel',
                    'hash_brown_scrambl_burrito': 'hash_brown_scramble_burrito',
                    'hash_brown_scrambl_bowl': 'hash_brown_scramble_bowl',
                    'delux_sandwich': 'deluxe_sandiwch',
                    'nugget': 'nuggets',
                    'chicken_noodl_soup': 'chicken_noodle_soup',
                    'nugget_km': 'nuggets_km',
                    'chicken_strip_km': 'chicken_strips_km',
                    'grill_nugget_km': 'grilled_nuggets_km',
                    'vanilla_milkshak': 'vanilla_milkshake',
                    'strawberri_milkshak': 'strawberry_milkshake',
                    'frost_coffe': 'frosted_coffee',
                    'frost_lemonad': 'frosted_lemonade',
                    'chocol_chunk_cooki': 'chocolate_chunk_cookie',
                    'dasani_bottl_water': 'dasani_bottled_water',
                    'honest_kid_appl_juic': 'honest_kid_apple_juice',
                    'simpli_orang': 'simply_orange',
                    'coffe': 'coffee',
                    'ice_coffe': 'iced_coffee',
                    'gallon_beverag': 'gallon_beverages',
                    'diet_lemonad': 'diet_lemonade',
                    'chick_fil_a_sauc': 'chick_fil_a_sauce',
                    'polynesian_sauc': 'polynesian_sauce',
                    'garden_herb_ranch_sauc': 'garden_herb_ranch_sauce',
                    'honey_mustard_sauc': 'honey_mustard_sauce',
                    'zesti_buffalo_sauc': 'zesty_buffalo_sauce',
                    'barbequ_sauc': 'barbeque_sauce',
                    'sriracha_sauc': 'sriracha_sauce',
                    'creami_salsa': 'creamy_salsa',
                    'fat_free_honey_mustard_dress': 'fat_free_honey_mustard_dressing',
                    'garden_herb_ranch_dress': 'garden_herb_ranch_dressing',
                    'light_italian_dress': 'light_italian_dressing',
                    'avacado_lime_dress': 'avacado_lime_dressing',
                    'chili_lime_vinaigrett': 'chili_lime_vinaigrette',
                    'light_balsam_vinaigrett': 'light_balsamic_vinaigrette',
                    'zesti_appl_cider_vinaigrett': 'zesty_apple_cider_vinaigrette',
                    'freshli_brew_ice_tea_sweeten': 'freshly_brewed_iced_tea_sweetened',
                    'freshli_brew_ice_tea_unsweeten': 'freshly_brewed_iced_tea_unsweetened'
                    }

    def modify(self, text):
        foodTokenizer = self.foodTokenizer
        text = re.sub('[^\w\s]', '', text)
        tokenizedOrder = foodTokenizer.tokenize(self.stripAndStemText(text))
        tokenizedOrder.reverse()
        print tokenizedOrder
        return tokenizedOrder

    def add_items(self, text):
        tokenizedOrder = self.modify(text)
        i = 0
        for t in tokenizedOrder:
            
            if t in self.items:
                possibleNumber = tokenizedOrder[i+1]
                if possibleNumber in self.unit_number:
                    self.items[t] += self.unit_number[possibleNumber]
                else:
                    try:
                        self.items[t] += int(tokenizedOrder[i+1])
                    except:
                        self.items[t] += 1
            elif t in self.synonyms:
                possibleNumber = tokenizedOrder[i+1]
                if possibleNumber in self.unit_number:
                    self.items[self.synonyms[t]] += self.unit_number[possibleNumber]
                else:
                    try:
                        self.items[self.synonyms[t]] += int(tokenizedOrder[i+1])
                    except:
                        self.items[self.synonyms[t]] += 1
            i+=1


    def remove_items(self, text):
        tokenizedOrder = self.modify(text)
        i = 0
        for t in tokenizedOrder:
            if t in self.items:
                possibleNumber = tokenizedOrder[i+1]
                if possibleNumber in self.unit_number:
                    self.items[t] -= self.unit_number[possibleNumber]
                else:
                    try:
                        self.items[t] -= int(tokenizedOrder[i+1])
                    except:
                        self.items[t] -= 1
                self.items[t] = max(self.items[t],0)
            elif t in self.synonyms:
                possibleNumber = tokenizedOrder[i+1]
                if possibleNumber in self.unit_number:
                    self.items[self.synonyms[t]] -= self.unit_number[possibleNumber]
                else:
                    try:
                        self.items[self.synonyms[t]] -= int(tokenizedOrder[i+1])
                    except:
                        self.items[self.synonyms[t]] -= 1
                self.items[self.synonyms[t]] = max(self.items[self.synonyms[t]],0)
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
                res = res + " " + str(self.items[item]) + " " + item.replace("_"," ") + ", "
        return res[:-2]

    def resetDict(self):
        for item in self.items:
            self.items[item] = 0