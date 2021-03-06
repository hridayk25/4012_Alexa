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
cfaimg='https://i.imgur.com/NXnRoK5.png'
red='https://imgur.com/e25PRAg.png'

@app.route('/')
def homepage():
    return "hi"

@ask.launch
def start_skill():
    curOrder.resetDict()
    print "started skill"
    message = "What would you like?"
    welcome_title = "Welcome"
    welcome_message = render_template('welcome')
    out = question(welcome_message).standard_card(title='Welcome', text='Testing')
    textContent = {
	'primaryText': {
	'text': message,
	'type':'RichText'
	}	
    }
    if context.System.device.supportedInterfaces.Display:
        out.display_render(
            template='BodyTemplate7',
            backButton='HIDDEN',
            background_image_url=red,
	    image=cfaimg,
#	    text=textContent,
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
    myImages, myPrices, myCals, myQuants = curOrder.getItemData()
    myList = myOrd.split(",")
    for item, image, price, cal, quant in zip(myList, myImages, myPrices, myCals, myQuants):
	if quant > 1:
		info = '$'+str(price)+' | '+str(round(cal,0))+' calories (each)',
	else:
		info = '$'+str(price)+' | '+str(round(cal,0))+' calories',

	listItem = {
                'image': {
			'sources': [
				{
					"url":image+'.png'
				}
			]
		},
		'textContent': {
			'primaryText': {
				'text':item,
				'type':"RichText"
			},
			'secondaryText': {
				'text':info[0],
				'type':"RichText"
			}
		}	
	}
	myListItems.append(listItem)
    msg = "My pleasure, is this correct?"
    myTotal = curOrder.getTotalCost()
    render = render_template('results', results=msg)
    out = question(render).standard_card(title='Your Order:', text='Testing')
    if context.System.device.supportedInterfaces.Display:
	out.list_display_render(
		template = 'ListTemplate1',
		title = 'Your Order Total: $'+str(round(myTotal,2)),
		backButton = 'HIDDEN',
        background_image_url=red,
		listItems = myListItems,
	)
    return out 
    # return statement("heres your food")
@ask.intent("CompleteIntent")
def complete_intent():
    # log the order
    print "Complete intent invoked"
    price = curOrder.getTotalCost()
    f = open('order.log','a')
    f.write(str(datetime.datetime.now()))
    f.write('\t')
    f.write(curOrder.printOrder())
    f.write('\t')
    f.write(str(price))
    f.write('\n')
    f.close()

    curOrder.resetDict()
    welcome_title = "Complete"
    if price == 0.0:
        return statement("You do not have enough items to complete an order. Exiting your order.")
    else:
        message = "Your order has been placed. Your total is $%.2f . Thank you for choosing Chick-Fil-A."%price
        return statement(message)

@ask.intent("NoIntent")
def no_intent():
    print "No intent invoked"
    bye = "bye"
    return question("At any point you can modify your order. To add an item to your order, say 'add'. To remove an item from your order, say 'remove'.")

@ask.intent("NewOrder")
def newOrder():
    print "New order intent invoked"
    curOrder.resetDict()
    message = "Welcome. What would you like?"
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
            template='BodyTemplate7',
            token=None,
	    background_image_url=red,
            backButton='HIDDEN',
        image=cfaimg,
        text=textContent
        )
    return out

@ask.intent("FallbackIntent")
def fallback_intent():
    print "Had to fallback"
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
    myImages, myPrices, myCals, myQuants = curOrder.getItemData()
    myList = myOrd.split(",")
    for item, image, price, cal, quant in zip(myList, myImages, myPrices, myCals, myQuants):
    	if quant > 1:
    		info = '$'+str(price)+' | '+str(cal)+' calories (each)',
    	else:
    		info = '$'+str(price)+' | '+str(cal)+' calories',
    	listItem = {
                    'image': {
    			'sources': [
    				{
    					"url":image+'.png'
    				}
    			]
    		},
                            
    		'textContent': {
    			'primaryText': {
    				'text':item,
    				'type':"RichText"
    			},
    			'secondaryText': {
    				'text':info[0],
    				'type':"RichText"
    			}
    		}	
    	}
    	myListItems.append(listItem)
    msg = "Is this correct?"
    myTotal = curOrder.getTotalCost()
    render = render_template('results', results=msg)
    out = question(render).standard_card(title='Your Order:', text='Testing')
    if context.System.device.supportedInterfaces.Display:
	out.list_display_render(
		template = 'ListTemplate1',
		title = 'Your Order Total: $'+str(round(myTotal,2)),
		backButton = 'HIDDEN',
        background_image_url=red,
		listItems = myListItems,
	)
    return out

@ask.intent("removeIntent")
def remove_intent():
    myListItems = []
    msg = "Did you want to order the following items?"
    food = request.get_json()
    text = food["request"]["intent"]["slots"]["food"]["value"]
    curOrder.remove_items(text)
    myOrd = curOrder.printOrder()
    myImages, myPrices, myCals, myQuants = curOrder.getItemData()
    myList = myOrd.split(",")
    for item, image, price, cal, quant in zip(myList, myImages, myPrices, myCals, myQuants):
    	if quant > 1:
    		info = '$'+str(price)+' | '+str(cal)+' calories (each)',
    	else:
    		info = '$'+str(price)+' | '+str(cal)+' calories',
    	listItem = {
                    'image': {
    			'sources': [
    				{
    					"url":image+'.png'
    				}
    			]
    		},
                            
    		'textContent': {
    			'primaryText': {
    				'text':item,
    				'type':"RichText"
    			},
    			'secondaryText': {
    				'text':info[0],
    				'type':"RichText"
    			}
    		}	
    	}
    	myListItems.append(listItem)
    msg = "Is this correct?"
    myTotal = curOrder.getTotalCost()
    render = render_template('results', results=msg)
    out = question(render).standard_card(title='Your Order:', text='Testing')
    if context.System.device.supportedInterfaces.Display:
	out.list_display_render(
		template = 'ListTemplate1',
		title = 'Your Order Total: $'+str(round(myTotal,2)),
		backButton = 'HIDDEN',
        background_image_url=red,
		listItems = myListItems,
	)
    return out

@ask.intent("cancelOrderIntent")
def cancel_order_intent():
    curOrder.resetDict()
    return statement("Your order has been canceled.")


if __name__ == '__main__':
    app.run(debug=True)
