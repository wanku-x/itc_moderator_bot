import telebot
import configparser
from pony import orm
from models import db

import database
import start
import help
import settings
import voteban
import admin_utils
import utils

config = configparser.ConfigParser()
config.read('/home/wanku/itc_moderator_bot/settings.ini')
bot = telebot.TeleBot(config['DEFAULT']['token'], threaded=False)

db.bind(
    provider='mysql',
    host=config['DEFAULT']['db_host'],
    user=config['DEFAULT']['db_username'],
    passwd=config['DEFAULT']['db_password'],
    db=config['DEFAULT']['db_database'],
)
db.generate_mapping(create_tables=True)


@bot.message_handler(commands=['start'])
def handle_start(message):
    start.handle_start(bot, message)


@bot.message_handler(commands=['help'])
def handle_help(message):
    help.handle_help(bot, message)


@bot.message_handler(commands=['settings'])
def handle_settings(message):
    settings.handle_settings(bot, message)


@bot.message_handler(commands=['offense'])
def handle_offense(message):
    voteban.handle_voteban(bot, message, 'other')


@bot.message_handler(commands=['spam'])
def handle_spam(message):
    voteban.handle_voteban(bot, message, 'spam')


@bot.message_handler(commands=['ban'])
def handle_ban(message):
    admin_utils.handle_ban(bot, message)


@bot.message_handler(commands=['kick'])
def handle_kick(message):
    admin_utils.handle_kick(bot, message)


@bot.message_handler(commands=['mute'])
def handle_mute(message):
    admin_utils.handle_mute(bot, message)


@bot.message_handler(commands=['nometa'])
def handle_nometa(message):
    utils.handle_nometa(bot, message)


@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    if call.data == "vote_for" or call.data == "vote_against":
        voteban.handle_callback_vote(bot, call)
    else:
        bot.answer_callback_query(
            callback_query_id=call.id,
            text="Ты нажал кнопку, которой не должно существовать.",
            show_alert=True,
        )
