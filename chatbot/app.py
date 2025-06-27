from flask import Flask, request, jsonify, render_template
from chatbot import SmartChatBot  # Make sure your SmartChatBot class is in chatbot.py

app = Flask(__name__)
bot = SmartChatBot("GrokLite")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data.get('message', '')
    response = bot.get_response(user_input)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
