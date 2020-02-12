import configparser
import telebot
import voteban

config = configparser.ConfigParser()
config.read('settings.ini')
bot = telebot.TeleBot(config['DEFAULT']['Token'])

start_message = "Привет! Я бот, который будет модерировать твой чат!\n\n"\
                "Я умею запускать голосование за бан участников!"

help_private_message = "Это помощь по моим командам!\n\n"\
                       "Это личное сообщение"

help_group_message = "Это помощь по моим командам!\n\n"\
                     "Это публичное сообщение"


@bot.message_handler(commands=['start'])
def handle_start(message):
    if message.chat.type == "private":
        bot.send_message(
            message.chat.id,
            start_message,
            parse_mode = "markdown",
        )


@bot.message_handler(commands=['help'])
def handle_help(message):
    if message.chat.type == "private":
        bot.send_message(
            message.chat.id,
            help_private_message,
            parse_mode = "markdown",
        )
    if message.chat.type == "group" or message.chat.type == "supergroup":
        bot.send_message(
            message.chat.id,
            help_group_message,
            parse_mode = "markdown",
        )


@bot.message_handler(commands=['voteban'])
def handle_voteban(message):
    if (message.chat.type == "group" or message.chat.type == "supergroup"):
        verify_vote_status = voteban.verify_vote(bot, message)
        if verify_vote_status["success"]:
            poll = telebot.types.Poll(question = "Ban?")
            poll.add("Да")
            poll.add("Нет")
            bot.send_poll(
                chat_id = message.chat.id,
                poll = poll,
            )
        elif verify_vote_status["error"] == "no_reply":
            bot.send_message(
                message.chat.id,
                "No reply",
                parse_mode = "markdown",
            )
        elif verify_vote_status["error"] == "self_complaint":
            bot.send_message(
                message.chat.id,
                "Self complaint",
                parse_mode = "markdown",
            )
        elif verify_vote_status["error"] == "bot_complaint":
            bot.send_message(
                message.chat.id,
                "Bot complaint",
                parse_mode = "markdown",
            )
        elif verify_vote_status["error"] == "admin_complaint":
            bot.send_message(
                message.chat.id,
                "Admin complaint",
                parse_mode = "markdown",
            )
        

"""
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)
    print(message)
"""

bot.polling()