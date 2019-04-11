<<<<<<< HEAD
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
    curOrder.add_items(text)
    myOrd = curOrder.printOrder()
    return question(msg + myOrd + ", to add to your order say add, to remove an item say remove, to finalize order say complete. ")
    # return statement("heres your food")
@ask.intent("CompleteIntent")
def complete_intent():
    # Get the price
    price = curOrder.getTotalCost()
    # log the order
    f = open('order.log','a')
    f.write(str(datetime.datetime.now()))
    f.write('\t')
    f.write(curOrder.printOrder())
    f.write('\t')
    f.write(str(price))
    f.write('\n')
    f.close()

    curOrder.resetDict()
    return question("Your order has been placed. Your total for this order is $%.2f. To order something else, say new order"%price)
@ask.intent("NoIntent")
def no_intent():
    bye = "bye"
    return statement(bye)
@ask.intent("NewOrder")
def newOrder():
    welcome_message = "Order increment. Welcome. What would you like?"
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
    print(text)
    curOrder.add_items(text)
    myOrd = curOrder.printOrder()
    return question(msg + myOrd + ", to add to your order say add, to remove an item say remove, to finalize order say complete. ")

@ask.intent("removeIntent")
def remove_intent():
    msg = "Did you want to order the following items?"
    food = request.get_json()
    text = food["request"]["intent"]["slots"]["food"]["value"]
    curOrder.remove_items(text)
    myOrd = curOrder.printOrder()
    return question(
        msg + myOrd + ", to add to your order say add, to remove an item say remove, to finalize order say complete. ")


@ask.intent("cancelOrderIntent")
def cancel_order_intent():
    curOrder.resetDict()
    return question("Your order has been cancelled. What would you like?")


if __name__ == '__main__':
    app.run(debug=True)
=======
# https://stackoverflow.com/questions/2835559/parsing-values-from-a-json-file
# https://techtutorialsx.com/2017/01/07/flask-parsing-json-data/
from flask import Flask, request, render_template
from flask_ask import Ask, statement, question, session, context
import json
from order import Order
import re
import datetime

app = Flask(__name__)
ask = Ask(app, "/")
curOrder = Order()
cfaimg='https://16jhl82mq2imp4wet2y0c7og-wpengine.netdna-ssl.com/wp-content/uploads/2010/01/Chick-fil-A-Logo-Update-RBMM.jpg'
white='https://www.publicdomainpictures.net/pictures/30000/velka/plain-white-background.jpg'

@app.route('/')
def homepage():
    return "hi"
@ask.launch
def start_skill():
    print "started skill"
    message = "What would you like?"
    welcome_title = "Welcome"
    welcome_message = render_template('welcome')
    out = question(welcome_message).standard_card(title='Welcome', text='Testing')
    textContent = {
	'primaryText': {
	'text':message,
	'type':'RichText'
	}	
    }
    if context.System.device.supportedInterfaces.Display:
        out.display_render(
            template='BodyTemplate2',
            title=welcome_title,
            token=None,
            backButton='HIDDEN',
	    image=cfaimg,
	    text=textContent,
	    hintText="I want a chiken sandwich and a lemonade."
        )
    return out
    # return question(welcome_message)
    # .standard_card(title='Welcome', text='What would you like?', large_image_url=cfaimg)
@ask.intent("Shengus")
def orderFood():
    print "order intent invoked"
    myListItems = []
    msg = "Did you want to order the following items?"
    food = request.get_json()
    text = food["request"]["intent"]["slots"]["food"]["value"]
    curOrder.add_items(text)
    myOrd = curOrder.printOrder()
    myList = myOrd[1:-1].split(",")
    for item in myList:
	listItem = {
		'token': None,
		'textContent': {
			'primaryText': {
				'text':item,
				'type':"RichText"
			}
		}	
	}
	myListItems.append(listItem)
    print myListItems
    msg = msg + myOrd
    render = render_template('results', results=msg)
    out = question(render).standard_card(title='Your Order:', text='Testing')
    if context.System.device.supportedInterfaces.Display:
	out.list_display_render(
		template = 'ListTemplate1',
		title = 'Your Order:',
		backButton = 'HIDDEN',
		listItems = myListItems,
		hintText="add Instructions here"
	)
    return out 
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

    curOrder.resetDict()
    return question("Your order has been placed. To order something else, say new order")
@ask.intent("NoIntent")
def no_intent():
    bye = "bye"
    return statement(bye)
@ask.intent("NewOrder")
def newOrder():
    welcome_message = "Order increment. Welcome. What would you like?"
    return question(welcome_message)
@ask.intent("FallbackIntent")
def fallback_intent():
    bye = "bye"
    return statement(bye)

@ask.intent("addIntent")
def add_intent():
    myListItems = []
    msg = "Did you want to order the following items?"
    food = request.get_json()
    text = food["request"]["intent"]["slots"]["food"]["value"]
    print(text)
    curOrder.add_items(text)
    myOrd = curOrder.printOrder()
    # return question(msg + myOrd + ", to add to your order say add, to remove an item say remove, to finalize order say complete. ")
    myList = myOrd[1:-1].split(",")
    for item in myList:
	listItem = {
		'token': None,
		'textContent': {
			'primaryText': {
				'text':item,
				'type':"RichText"
			}
		}	
	}
	myListItems.append(listItem)
    print myListItems
    msg = msg + myOrd
    render = render_template('results', results=msg)
    out = question(render).standard_card(title='Your Order:', text='Testing')
    if context.System.device.supportedInterfaces.Display:
	out.list_display_render(
		template = 'ListTemplate1',
		title = 'Your Order:',
		backButton = 'HIDDEN',
		listItems = myListItems,
		hintText="add Instructions here"
	)
    return out 
    # return statement("heres your food")

@ask.intent("removeIntent")
def remove_intent():
    myListItems = []
    msg = "Did you want to order the following items?"
    food = request.get_json()
    text = food["request"]["intent"]["slots"]["food"]["value"]
    curOrder.remove_items(text)
    myOrd = curOrder.printOrder()
    # return question(msg + myOrd + ", to add to your order say add, to remove an item say remove, to finalize order say complete. ")
    myList = myOrd[1:-1].split(",")
    for item in myList:
	listItem = {
		'token': None,
		'textContent': {
			'primaryText': {
				'text':item,
				'type':"RichText"
			}
		}	
	}
	myListItems.append(listItem)
    print myListItems
    msg = msg + myOrd
    render = render_template('results', results=msg)
    out = question(render).standard_card(title='Your Order:', text='Testing')
    if context.System.device.supportedInterfaces.Display:
	out.list_display_render(
		template = 'ListTemplate1',
		title = 'Your Order:',
		backButton = 'HIDDEN',
		listItems = myListItems,
		hintText="add Instructions here"
	)
    return out 
    # return statement("heres your food")


@ask.intent("cancelOrderIntent")
def cancel_order_intent():
    curOrder.resetDict()
    return question("Your order has been cancelled. What would you like?")


if __name__ == '__main__':
    app.run(debug=True)
>>>>>>> 6269603294b1ebb28ca2bc1a5725a54e764ed3bf
