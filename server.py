from flask import Flask
from flask_ask import Ask, statement, question,session

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
    msg = "Thanks for the request. bye."
    return question(msg)
@ask.intent("NoIntent")
def no_intent():
    bye = "bye"
    return statement(bye)

if __name__ == '__main__':
    app.run(debug=True)