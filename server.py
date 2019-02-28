# https://stackoverflow.com/questions/2835559/parsing-values-from-a-json-file
# https://techtutorialsx.com/2017/01/07/flask-parsing-json-data/
from flask import Flask, request
from flask_ask import Ask, statement, question, session
import json
from order import Order
import re

app = Flask(__name__)
ask = Ask(app, "/")

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
    curOrder = Order()
    curOrder.addFromText(text)
    myOrd = curOrder.printOrder()
    return question(msg + myOrd)
    # return statement("heres your food")
@ask.intent("YesIntent")
def yes_intent():
	return statement("Your order has been placed")
@ask.intent("NoIntent")
def no_intent():
    bye = "bye"
    return statement(bye)
@ask.intent("FallbackIntent")
def fallback_intent():
    bye = "bye"
    return statement(bye)

if __name__ == '__main__':
    app.run(debug=True)