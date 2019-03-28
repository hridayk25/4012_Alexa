# https://stackoverflow.com/questions/2835559/parsing-values-from-a-json-file
# https://techtutorialsx.com/2017/01/07/flask-parsing-json-data/
from flask import Flask, request
from flask_ask import Ask, statement, question, session
import json
from order import Order
import re
import datetime

app = Flask(__name__)
ask = Ask(app, "/")
curOrder = Order()

@app.route('/')
def homepage():
    return "hi"
@ask.launch
def start_skill():
    print "started skill"
    welcome_message = "Welcome. What would you like?"
    return question(welcome_message)
@ask.intent("Shengus")
def orderFood():
    print "order intent invoked"
    msg = "Did you want to order the following items?"
    food = request.get_json()
    text = food["request"]["intent"]["slots"]["food"]["value"]
    curOrder.addFromText(text)
    myOrd = curOrder.printOrder()
    return question(msg + myOrd + ", to add to your order say add, to remove an item say remove, to finalize order say complete. ")
    # return statement("heres your food")
@ask.intent("CompleteIntent")
def complete_intent():
    # log the order
    f = open('order.log','a')
    f.write(str(datetime.datetime.now()))
    f.write('\t')
    f.write(curOrder.printOrder())
    f.write('\n')
    f.close()
    return question("Your order has been placed. To order something else, say new order")
@ask.intent("NoIntent")
def no_intent():
    bye = "bye"
    return statement(bye)
@ask.intent("NewOrder")
def newOrder():
    welcome_message = "Order increment. Welcome. What would you like?"
    curOrder.resetDict()
    return question(welcome_message)
@ask.intent("FallbackIntent")
def fallback_intent():
    bye = "bye"
    return statement(bye)

@ask.intent("addIntent")
def add_intent():
    msg = "Did you want to order the following items?"
    food = request.get_json()
    text = food["request"]["intent"]["slots"]["food"]["value"]
    curOrder.addFromText(text)
    myOrd = curOrder.printOrder()
    return question(msg + myOrd + ", to add to your order say add, to remove an item say remove, to finalize order say complete. ")

@ask.intent("removeIntent")
def remove_intent():
    msg = "Did you want to order the following items?"
    food = request.get_json()
    text = food["request"]["intent"]["slots"]["food"]["value"]
    curOrder.removeFromText(text)
    myOrd = curOrder.printOrder()
    return question(
        msg + myOrd + ", to add to your order say add, to remove an item say remove, to finalize order say complete. ")

if __name__ == '__main__':
    app.run(debug=True)