# https://stackoverflow.com/questions/2835559/parsing-values-from-a-json-file
# https://techtutorialsx.com/2017/01/07/flask-parsing-json-data/
from flask import Flask, request
from flask_ask import Ask, statement, question, session
import json
from order import order
import re

app = Flask(__name__)
ask = Ask(app, "/")

@app.route('/')
def homepage():
    return "hi"
@ask.launch
def start_skill():
    welcome_message = "Welcome. What would you like?"
    return question(welcome_message)
@ask.intent("Shengus")
def share_headlines():
    msg = "Did you want to order the following items? "
    food = request.get_json()
    data = food["request"]["intent"]["slots"]["food"]["value"]
    # with open('data.json', 'w') as outfile:
    #     json.dump(data, outfile)
    curOrder = order()
    # for item in curOrder.dict:
    #     print(curOrder.dict[item])
    items = data.split(" ")
    print(items)
    for i in range(len(items)):
        # print(items[i])
        if (items[i] ==  "a" or items[i] ==  "an"):
            # print(items[i+1])
            curOrder.addItem(items[i+1])
    myOrd = curOrder.printOrder()

    return question(msg + myOrd[:-3])
@ask.intent("NoIntent")
def no_intent():
    bye = "bye"
    return statement(bye)

if __name__ == '__main__':
    app.run(debug=True)