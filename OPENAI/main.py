from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
import os
import openai

app = Flask(__name__)
load_dotenv()

my_key = os.getenv("OPENAI_API_KEY")
openai.api_key = my_key

def generate_answer(question):
    model_engine = "gpt-3.5-turbo"
    prompt = f"Q: {question}\nA:"

    try:
        response = openai.ChatCompletion.create(
            model=model_engine,
            messages=[{"role": "system", "content": "You are a helpful assistant."},
                      {"role": "user", "content": prompt}]
        )

        answer = response['choices'][0]['message']['content'].strip()
        return answer
    except Exception as e:
        return f"Error generating answer: {e}"
    
@app.route('/chatgpt', methods=['POST'])
def chatgpt():
    incoming_que = request.values.get('Body', '').lower()
    print(incoming_que)

    answer = generate_answer(incoming_que)
    print(answer)

    bot_resp = MessagingResponse()
    msg = bot_resp.message()
    msg.body(answer)

    return str(bot_resp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=5000)
    