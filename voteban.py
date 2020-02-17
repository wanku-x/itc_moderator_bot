from telebot import types
import database


def verify_poll(bot, message):
    if not message.reply_to_message:
        return {
            "success": False,
            "error": "no_reply"
        }

    accused_id = message.reply_to_message.from_user.id      # ID Обвиняемый
    accuser_id = message.from_user.id                       # ID Обвинитель
    admins = bot.get_chat_administrators(message.chat.id)
    admins_id = list(map(lambda admin: admin.user.id, admins))
    bot_id = bot.get_me().id

    if accused_id == accuser_id:
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


def create_keyboard(yes=0, no=0):
    keyboard = types.InlineKeyboardMarkup()
    button_yes = types.InlineKeyboardButton(
        text="Да: {}".format(yes),
        callback_data="yes",
    )
    button_no = types.InlineKeyboardButton(
        text="Нет: {}".format(no),
        callback_data="no",
    )
    keyboard.add(button_yes)
    keyboard.add(button_no)
    return keyboard


def handle_vote(bot, db, call, poll):
    vote = database.get_vote(
        db=db,
        poll_id=poll[0],
        voted_id=call.from_user.id,
    )

    if vote and ((vote[3] and call.data == "yes") or
       (not vote[3] and call.data == "no")):
        bot.answer_callback_query(
            callback_query_id=call.id,
            text="Твой голос уже учтён",
            show_alert=False,
        )
        return

    if not vote:
        database.create_vote(
            db=db,
            poll_id=poll[0],
            voted_id=call.from_user.id,
            to_ban=True if call.data == "yes" else False,
        )
    else:
        database.update_vote(
            db=db,
            vote_id=vote[0],
            to_ban=True if call.data == "yes" else False,
        )

    bot.answer_callback_query(
        callback_query_id=call.id,
        text="Твой голос: {}".format(
            "Да" if call.data == "yes" else "Нет"
        ),
        show_alert=False,
    )
    poll_results = database.get_poll_results(
        db=db,
        poll_id=poll[0],
    )
    bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=create_keyboard(
            poll_results[0],
            poll_results[1],
        ),
    )

    if (poll_results[0] >= 2):
        bot.send_message(
            chat_id=call.message.chat.id,
            text="Я забанил *username*",
            parse_mode="markdown",
        )

    if (poll_results[1] >= 2):
        bot.send_message(
            chat_id=call.message.chat.id,
            text="Я не буду банить *username*",
            parse_mode="markdown",
        )
