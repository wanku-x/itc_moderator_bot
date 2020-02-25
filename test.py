import telebot
import configparser

config = configparser.ConfigParser()
config.read('/home/wanku/itc_moderator_bot/settings.ini')
bot = telebot.TeleBot(config['DEFAULT']['token'], threaded=False)


@bot.message_handler(func=lambda message: True)
def handle_test(message):
    if not message.chat.type == "private":
        return False
    print(message.text)


bot.polling()
