# https://stackoverflow.com/questions/2835559/parsing-values-from-a-json-file
# https://techtutorialsx.com/2017/01/07/flask-parsing-json-data/
from flask import Flask, request, json, render_template
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
    return question(welcome_message).standard_card(title='Welcome', text='What would you like?', large_image_url='https://16jhl82mq2imp4wet2y0c7og-wpengine.netdna-ssl.com/wp-content/uploads/2010/01/Chick-fil-A-Logo-Update-RBMM.jpg')

@ask.intent("Shengus")
def orderFood():
    print "order intent invoked"
    msg = "Did you want to order the following items?"
    food = request.get_json()
    text = food["request"]["intent"]["slots"]["food"]["value"]
    curOrder.addFromText(text)
    myOrd = curOrder.printOrder()
    return question(msg + myOrd)
    # return statement("heres your food")
@ask.intent("YesIntent")
def yes_intent():
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

if __name__ == '__main__':
    app.run(debug=True)
