from telebot import types
import database

#
#   Messages
#
poll_message = \
    "[{0}](tg://user?id={1}) запустил голосование за бан "\
    "[{2}](tg://user?id={3})\n\nЕсли ты считаешь, что "\
    "*{2}* нарушил(а) правила чата, жми *\"Да\"*. "\
    "Иначе - жми *\"Нет\"*."

voteban_error_poll_already_created = \
    "Голосование за бан [{0}](tg://user?id={1}) уже существует"\
    "\n\nЯ перешлю голосование, если вы вдруг его потеряли"

voteban_error_no_reply = \
    "Выдели сообщение того, кто нарушает правила чата, "\
    "и ответь ему командой\n`/voteban`"

voteban_error_self_complaint = \
    "В лицо себе выстрели. Больше пользы будет."

voteban_error_bot_complaint = \
    "Ублюдок, мать твою, решил ко мне лезть? "\
    "Ну иди сюда, попробуй меня трахнуть! "\
    "Я тебя сам трахну! Онанист чертов, будь ты проклят!"

voteban_error_admin_complaint = \
    "Ты на кого батон крошишь? Проблем захотел?"


#
#   Database methods
#
def get_poll(bot, message):
    pass


def create_poll(bot, message):
    pass


def delete_poll(bot, call):
    pass


def get_vote(bot, call):
    pass


def create_vote(bot, call):
    pass


def update_vote(bot, call):
    pass


#
#   User punishment methods
#
def mute_user(bot, call):
    pass


def ban_user(bot, call):
    pass


def kick_user(bot, call):
    pass


#
#   Keyboard method
#
def create_poll_keyboard(votes_for_amount=0, votes_against_amount=0):
    keyboard = types.InlineKeyboardMarkup()
    button_yes = types.InlineKeyboardButton(
        text="Да: {}".format(votes_for_amount),
        callback_data="vote_for",
    )
    button_no = types.InlineKeyboardButton(
        text="Нет: {}".format(votes_against_amount),
        callback_data="vote_against",
    )
    keyboard.add(button_yes)
    keyboard.add(button_no)
    return keyboard


#
#   Verify methods
#
def can_poll(bot, message):
    if not message.reply_to_message:
        return {
            "success": False,
            "error": "no_reply"
        }

    accused_id = message.reply_to_message.from_user.id      # ID Обвиняемый
    accuser_id = message.from_user.id                       # ID Обвинитель
    admins = bot.get_chat_administrators(message.chat.id)
    admins_id = [admin.user.id for admin in admins]
    bot_id = bot.get_me().id
    poll = database.check_poll(
        chat_id=message.chat.id,
        accused_id=accused_id,
    )

    if poll:
        return {
            "success": False,
            "error": "poll_already_created",
            "message": poll.message_id,
        }
    elif accused_id == accuser_id:
        return {
            "success": False,
            "error": "self_complaint"
        }
    elif accused_id == bot_id:
        return {
            "success": False,
            "error": "bot_complaint"
        }
    elif accused_id in admins_id:
        return {
            "success": False,
            "error": "admin_complaint"
        }
    else:
        return {
            "success": True,
            "error": None,
        }


#
#   Handle methods
#
def handle_voteban(bot, message):
    if not (message.chat.type == "group" or message.chat.type == "supergroup"):
        return False

    user_can_poll = can_poll(bot, message)

    accused_id = message.reply_to_message.from_user.id
    accused_full_name = "{} {}".format(
        message.reply_to_message.from_user.first_name,
        message.reply_to_message.from_user.last_name,
    )
    accuser_id = message.from_user.id
    accuser_full_name = "{} {}".format(
        message.from_user.first_name,
        message.from_user.last_name,
    )

    if user_can_poll["success"]:
        sended_message = bot.send_message(
            chat_id=message.chat.id,
            text=poll_message.format(
                accuser_full_name,
                accuser_id,
                accused_full_name,
                accused_id,
            ),
            parse_mode="markdown",
            reply_markup=create_poll_keyboard()
        )

        poll_created = database.create_poll(
            chat_id=sended_message.chat.id,
            message_id=sended_message.message_id,
            accuser_id=accuser_id,
            accused_id=accused_id,
        )

        if not poll_created:
            bot.delete_message(
                chat_id=sended_message.chat.id,
                message_id=sended_message.message_id,
            )
            return False
        return True

    if user_can_poll["error"] == "poll_already_created":
        bot.send_message(
            chat_id=message.chat.id,
            text=voteban_error_poll_already_created.format(
                accused_full_name,
                accused_id,
            ),
            parse_mode="markdown",
        )
        bot.forward_message(
            chat_id=message.chat.id,
            from_chat_id=message.chat.id,
            message_id=user_can_poll["message"],
        )
        # bot.send_message(
        #     chat_id=message.chat.id,
        #     text=voteban_error_poll_already_created.format(
        #         accused_full_name,
        #         accused_id,
        #     ),
        #     reply_to_message_id=user_can_poll["message"],
        #     parse_mode="markdown",
        # )
        return False

    if user_can_poll["error"] == "no_reply":
        bot.send_message(
            chat_id=message.chat.id,
            text=voteban_error_no_reply,
            parse_mode="markdown",
        )
        return False

    if user_can_poll["error"] == "self_complaint":
        bot.send_message(
            chat_id=message.chat.id,
            text=voteban_error_self_complaint,
            parse_mode="markdown",
        )
        return False

    if user_can_poll["error"] == "bot_complaint":
        bot.send_message(
            chat_id=message.chat.id,
            text=voteban_error_bot_complaint,
            parse_mode="markdown",
        )
        return False

    if user_can_poll["error"] == "admin_complaint":
        bot.send_message(
            chat_id=message.chat.id,
            text=voteban_error_admin_complaint,
            parse_mode="markdown",
        )
        return False
    return False


def handle_callback_vote(bot, call):
    pass
    # poll = database.get_poll(
    #     db=db,
    #     chat_id=call.message.chat.id,
    #     message_id=call.message.message_id,
    # )

    # if not poll:
    #     bot.answer_callback_query(
    #         callback_query_id=call.id,
    #         text="Данное голосование отсутствует в базе данных.",
    #         show_alert=True,
    #     )
    #     return False

    # vote = database.get_vote(
    #     db=db,
    #     poll_id=poll[0],
    #     voted_id=call.from_user.id,
    # )

    # if vote and ((vote[3] and call.data == "yes") or
    #    (not vote[3] and call.data == "no")):
    #     bot.answer_callback_query(
    #         callback_query_id=call.id,
    #         text="Твой голос уже учтён",
    #         show_alert=False,
    #     )
    #     return False

    # if not vote:
    #     database.create_vote(
    #         db=db,
    #         poll_id=poll[0],
    #         voted_id=call.from_user.id,
    #         to_ban=(call.data == "vote_for"),
    #     )
    # else:
    #     database.update_vote(
    #         db=db,
    #         vote_id=vote[0],
    #         to_ban=(call.data == "vote_for"),
    #     )

    # bot.answer_callback_query(
    #     callback_query_id=call.id,
    #     text="Твой голос: {}".format(
    #         "Да" if call.data == "vote_for" else "Нет"
    #     ),
    #     show_alert=False,
    # )
    # poll_results = database.get_poll_results(
    #     db=db,
    #     poll_id=poll[0],
    # )
    # bot.edit_message_reply_markup(
    #     chat_id=call.message.chat.id,
    #     message_id=call.message.message_id,
    #     reply_markup=create_keyboard(
    #         poll_results[0],
    #         poll_results[1],
    #     ),
    # )

    # if (poll_results[0] >= 2):
    #     bot.send_message(
    #         chat_id=call.message.chat.id,
    #         text="Я забанил *username*",
    #         parse_mode="markdown",
    #     )

    # if (poll_results[1] >= 2):
    #     bot.send_message(
    #         chat_id=call.message.chat.id,
    #         text="Я не буду банить *username*",
    #         parse_mode="markdown",
    #     )
