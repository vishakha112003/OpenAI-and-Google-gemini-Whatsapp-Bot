#LOADING THE NECESSARY LIBRARIES 
import os 
import google.generativeai as bot
from flask import Flask 
from flask import request
from twilio.rest import Client 

app = Flask(__name__)
key = "" #gemini key
wp_number = "whatsapp:+14155238886"
acc_id = ""
acc_token = "


#selecting model
def response_system(msg):
        bot.configure(api_key=key)

        model = bot.GenerativeModel("gemini-pro")
    
    
    #checking the response
        response = model.generate_content(msg)
        return(response.text)

def send_msg(msg, recepient):
    cleint = Client(acc_id,acc_token)
    cleint.messages.create(
        from_=wp_number,
        body=msg,
        to=recepient
    )

def length_char(text):
      words = text.split()
      return len(words)

def process_msg(msg, sender):
      response = ""
      inputs = ["HI","hii" ,"hi", "start", "Start", "START", "Hello", "HELLO", "hello","Hi","Hey", 'hey', "Hii"]
      end_put = ["STOP", "stop", "end", "thankyou", "Thank You", "Thank you", "thankyou", "bye", "Bye", "BYE"]
      if msg in inputs:
            response = f"Hello {sender} , How may I help you Today"

      elif msg  in end_put:
            response = f"Bye {sender}"
      else:
            answer = response_system(msg)
            
            length = length_char(answer)
            if length > 250:
                  sh_ans = response_system(msg+"under 200 words")
                  response = f"CAUTION : We have a word limit of 250 words per response.To ensure the response are easy to read and concise. \n\n"
                  response += sh_ans
            else:
                  response = answer
            

            
      return (response)
@app.route("/webhook", methods = ["POST"])
def webhook():
    print(request)
    # print("OKay Working")
    f = request.form
    msg = f['Body']
    sender = f['From']
    name = f['ProfileName']
    print(f"**********************************************************\nSender : {sender}\nName :  {name}\nMessage Recieved : {msg}")
    response = process_msg(msg, name)
    print(f"Message Sent : {response}")
    send_msg(response,sender)
    return "OK", 200

        

