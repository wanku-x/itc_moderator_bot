import telebot
import configparser
import mysql.connector

import start
import help
import voteban

config = configparser.ConfigParser()
config.read('/home/wanku/itc_moderator_bot/settings.ini')
bot = telebot.TeleBot(config['DEFAULT']['token'], threaded=False)

db = mysql.connector.connect(
    host=config['DEFAULT']['DB_host'],
    user=config['DEFAULT']['DB_username'],
    passwd=config['DEFAULT']['DB_password'],
    database=config['DEFAULT']['DB_database'],
)


@bot.message_handler(commands=['start'])
def handle_start(message):
    start.handle_start(bot, message)


@bot.message_handler(commands=['help'])
def handle_help(message):
    help.handle_help(bot, message)


@bot.message_handler(commands=['voteban'])
def handle_voteban(message):
    voteban.handle_voteban(bot, db, message)


@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    if call.data == "vote_for" or call.data == "vote_against":
        voteban.handle_callback_vote(bot, db, call)
    else:
        bot.answer_callback_query(
            callback_query_id=call.id,
            text="Ты нажал кнопку, которой не должно существовать.",
            show_alert=True,
        )
