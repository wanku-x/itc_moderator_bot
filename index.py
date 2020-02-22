from flask import Flask, request, abort
import telebot
import configparser
import bot

config = configparser.ConfigParser()
config.read('settings.ini')
app = Flask(__name__)

bot.remove_webhook()
bot.set_webhook(url='{}/{}'.format(
    config['DEFAULT']['url_base'],
    config['DEFAULT']['secret']
))


@app.route('/{}'.format(config['DEFAULT']['secret']), methods=["POST"])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        abort(403)
