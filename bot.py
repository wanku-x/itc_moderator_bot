import telebot
import configparser
# import mysql.connector

config = configparser.ConfigParser()
config.read('settings.ini')
bot = telebot.TeleBot(config['DEFAULT']['token'])


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hello from Bot")

# db = mysql.connector.connect(
#     host=config['DEFAULT']['DB_host'],
#     user=config['DEFAULT']['DB_username'],
#     passwd=config['DEFAULT']['DB_password'],
#     database=config['DEFAULT']['DB_database'],
# )

# start_message = "Привет! Я бот, который будет модерировать твой чат!\n\n"\
#                 "Я умею запускать голосование за бан участников!"

# help_private_message = "Это помощь по моим командам!\n\n"\
#                        "Это личное сообщение"

# help_group_message = "Это помощь по моим командам!\n\n"\
#                      "Это публичное сообщение"

# @bot.message_handler(commands=['start'])
# def handle_start(message):
#     if message.chat.type == "private":
#         bot.send_message(
#             chat_id=message.chat.id,
#             text=start_message,
#             parse_mode="markdown",
#         )


# @bot.message_handler(commands=['help'])
# def handle_help(message):
#     if message.chat.type == "private":
#         bot.send_message(
#             chat_id=message.chat.id,
#             text=help_private_message,
#             parse_mode="markdown",
#         )
#     if message.chat.type == "group" or message.chat.type == "supergroup":
#         bot.send_message(
#             chat_id=message.chat.id,
#             text=help_group_message,
#             parse_mode="markdown",
#         )


# @bot.message_handler(commands=['voteban'])
# def handle_voteban(message):
#     if (message.chat.type == "group" or message.chat.type == "supergroup"):
#         verify_poll_status = voteban.verify_poll(bot, message)
#         if verify_poll_status["success"]:
#             sended_message = bot.send_message(
#                 chat_id=message.chat.id,
#                 text="Баним *username*?",
#                 parse_mode="markdown",
#                 reply_markup=voteban.create_keyboard()
#             )
#             database.create_poll(
#                 db=db,
#                 chat_id=sended_message.chat.id,
#                 message_id=sended_message.message_id,
#                 accuser_id=message.from_user.id,
#                 accused_id=message.reply_to_message.from_user.id,
#             )
#         elif verify_poll_status["error"] == "no_reply":
#             bot.send_message(
#                 chat_id=message.chat.id,
#                 text="No reply",
#                 parse_mode="markdown",
#             )
#         elif verify_poll_status["error"] == "self_complaint":
#             bot.send_message(
#                 chat_id=message.chat.id,
#                 text="Self complaint",
#                 parse_mode="markdown",
#             )
#         elif verify_poll_status["error"] == "bot_complaint":
#             bot.send_message(
#                 chat_id=message.chat.id,
#                 text="Bot complaint",
#                 parse_mode="markdown",
#             )
#         elif verify_poll_status["error"] == "admin_complaint":
#             bot.send_message(
#                 chat_id=message.chat.id,
#                 text="Admin complaint",
#                 parse_mode="markdown",
#             )


# @bot.callback_query_handler(func=lambda call: True)
# def callback_voteban(call):
#     poll = database.get_poll(
#         db=db,
#         chat_id=call.message.chat.id,
#         message_id=call.message.message_id,
#     )
#     if not poll:
#         bot.answer_callback_query(
#             callback_query_id=call.id,
#             text="Данное голосование отсутствует в базе данных.",
#             show_alert=True,
#         )
#     elif call.data == "yes" or call.data == "no":
#         voteban.handle_vote(bot, db, call, poll)
#     else:
#         bot.answer_callback_query(
#             callback_query_id=call.id,
#             text="Ты нажал на какую-то магическую кнопку, "
#                  "которой не должно существовать.",
#             show_alert=True,
#         )


# if __name__ == '__main__':
#     bot.polling(none_stop=True)
