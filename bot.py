from flask import Flask
import threading, telebot, os

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)
@app.route('/')
def home():
    return "Rsb-Shop OK"

def run_web():
    app.run(host='0.0.0.0', port=10000)

@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, "Привет! Rsb-Shop работает! 🛍️")

threading.Thread(target=run_web, daemon=True).start()
bot.infinity_polling()
