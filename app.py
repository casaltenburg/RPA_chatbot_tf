from flask import Flask, render_template, request
from chatbot_model import *
import re
import mysql.connector
import datetime
import robot_connector

#load variables

app = Flask(__name__)
email = ""
messageCount = 0

#connection with database

mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Butterfly1.",
        database="chatbot_db"
        )

mycursor = mydb.cursor()

#route to index template

@app.route('/')
def home():
    return render_template("index.html")

# get function from user input in message function

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    date = datetime.date.today()
    global messageCount
    #check if message is the first message
    if messageCount > 0 and messageCount % 2 :
        #if not the first message add user message to database
        add_message(email, date, messageCount, userText, "User")
        messageCount += 1
    print(messageCount, userText)
    if messageCount == 0:
        # check if it is a correct mail adress
        if re.match(r"[^@]+@[^@]+\.[^@]", userText):
            set_email(userText)
            messageCount = 1
            print(messageCount)
            # start of the conversation
            return "Wat voor onderneming heeft u?"
        else:
            return "Geef een geldig e-mailadres"
    else:
        #when its not the first message let the Chatbot return an answer
        stringResponse = response(userText, 123)
        # add chatbot message to database
        add_message(email, date, messageCount, stringResponse, "Bot")
        messageCount += 1
        return stringResponse;

# set email
def set_email(corr_email):
    global email
    email = corr_email
    robot_connector.send_email(email)
    #print(email)


# add message to the database
def add_message(email, date, count, userText, sender):
    sql = "INSERT INTO conversation (email,c_date, message_count,message,sender ) VALUES (%s,%s,%s,%s,%s)"
    val = (email, date, messageCount, userText, sender)
    mycursor.execute(sql, val)
    mydb.commit()



if __name__ == '__main__':
    app.run(threaded=True)
