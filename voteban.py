from telebot import types
import database

#
#   Messages
#
poll_message = \
    "[{0}](tg://user?id={1}) запустил голосование за бан "\
    "[{2}](tg://user?id={3}).\n\n"\
    "Если ты считаешь, что *{2}* нарушил(а) правила чата, жми *\"Да\"*. "\
    "Иначе - жми *\"Нет\"*.\n\n"\
    "{4}"\

voteban_error_poll_already_created = \
    "Голосование за бан [{0}](tg://user?id={1}) уже существует."\
    "\n\nЯ перешлю голосование, если вы вдруг его потеряли."

voteban_error_no_reply = \
    "Выдели сообщение того, кто нарушает правила чата, "\
    "и ответь ему командой:\n"\
    "`/spam` - если сообщение является спамом\n"\
    "`/offense` - если сообщение нарушает другие правила чата"

voteban_error_self_complaint = \
    "В лицо себе выстрели. Больше пользы будет."

voteban_error_bot_complaint = \
    "Ублюдок, мать твою, решил ко мне лезть? "\
    "Ну иди сюда, попробуй меня трахнуть! "\
    "Я тебя сам трахну! Онанист чертов, будь ты проклят!"

voteban_error_admin_complaint = \
    "Ты на кого батон крошишь? Проблем захотел?"

callback_message = \
    "Твой голос: {0}"

callback_error_no_poll = \
    "Голосование окончено."

callback_error_vote_counted = \
    "Твой голос уже учтён."

result_message_innocent = \
    "Большинство решило, что [{0}](tg://user?id={1}) "\
    "не нарушал(а) правил чата. Голосование окончено."

result_message_guilty = \
    "Большинство решило, что [{0}](tg://user?id={1}) "\
    "нарушил(а) правила чата. Голосование окончено.\n\n"\
    "*Наказание:* {2}."


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
#   Verify method
#
def can_poll(bot, message):
    if not message.reply_to_message:
        return {
            "error": "no_reply",
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
            "error": "poll_already_created",
            "message": poll.message_id,
        }
    elif accused_id == accuser_id:
        return {
            "error": "self_complaint",
        }
    elif accused_id == bot_id:
        return {
            "error": "bot_complaint",
        }
    elif accused_id in admins_id:
        return {
            "error": "admin_complaint",
        }
    else:
        return {
            "error": None,
        }


#
#   Handle methods
#
def handle_voteban(bot, message, reason):
    if not (message.chat.type == "group" or message.chat.type == "supergroup"):
        return False

    user_can_poll = can_poll(
        bot=bot,
        message=message,
    )

    if user_can_poll["error"] == "no_reply":
        bot.reply_to(
            message=message,
            text=voteban_error_no_reply,
            parse_mode="markdown",
        )
        return False

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

    if not user_can_poll["error"]:
        sended_message = bot.send_message(
            chat_id=message.chat.id,
            text=poll_message.format(
                accuser_full_name,
                accuser_id,
                accused_full_name,
                accused_id,
                "*Причина:* Спам" if reason == "spam" else
                "*Сообщение:* " + message.reply_to_message.text,
            ),
            parse_mode="markdown",
            reply_markup=create_poll_keyboard()
        )

        poll_created = database.create_poll(
            chat_id=sended_message.chat.id,
            message_id=sended_message.message_id,
            accuser_id=accuser_id,
            accused_id=accused_id,
            message=message.reply_to_message.text,
            reason=reason
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
            reply_to_message_id=user_can_poll["message"],
            parse_mode="markdown",
        )
        return False

    if user_can_poll["error"] == "self_complaint":
        bot.reply_to(
            message=message,
            text=voteban_error_self_complaint,
            parse_mode="markdown",
        )
        return False

    if user_can_poll["error"] == "bot_complaint":
        bot.reply_to(
            message=message,
            text=voteban_error_bot_complaint,
            parse_mode="markdown",
        )
        return False

    if user_can_poll["error"] == "admin_complaint":
        bot.reply_to(
            message=message,
            text=voteban_error_admin_complaint,
            parse_mode="markdown",
        )
        return False
    return False


def handle_callback_vote(bot, call):
    poll = database.get_poll(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
    )

    if not poll:
        bot.answer_callback_query(
            callback_query_id=call.id,
            text=callback_error_no_poll,
            show_alert=True,
        )
        return False

    vote = database.get_vote(
        poll_id=poll.id,
        voted_id=call.from_user.id,
    )

    if not vote:
        database.create_vote(
            poll_id=poll.id,
            voted_id=call.from_user.id,
            to_ban=(call.data == "vote_for"),
        )
    elif (
        (vote.to_ban and call.data == "vote_for") or
        (not vote.to_ban and call.data == "vote_against")
    ):
        bot.answer_callback_query(
            callback_query_id=call.id,
            text=callback_error_vote_counted,
            show_alert=False,
        )
        return True
    else:
        database.update_vote(
            id=vote.id,
            to_ban=(call.data == "vote_for"),
        )

    poll_results = database.get_poll_results(
        poll_id=poll.id,
    )

    bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=create_poll_keyboard(
            votes_for_amount=poll_results["votes_for_amount"],
            votes_against_amount=poll_results["votes_against_amount"],
        ),
    )

    bot.answer_callback_query(
        callback_query_id=call.id,
        text=callback_message.format(
            "Да" if call.data == "vote_for" else "Нет"
        ),
        show_alert=False,
    )

    settings = database.get_settings(
        chat_id=call.message.chat.id
    )

    if (
        (poll_results["votes_for_amount"] < settings.votes_for_decision) and
        (poll_results["votes_against_amount"] < settings.votes_for_decision)
    ):
        bot.send_message(
            chat_id=call.message.chat.id,
            text="Голосов не достаточно для принятия",
            parse_mode="markdown",
        )
        return True

    accused_id = poll.accused_id
    accused = bot.get_chat_member(
        chat_id=call.message.chat.id,
        user_id=accused_id,
    )
    accused_full_name = "{} {}".format(
        accused.user.first_name,
        accused.user.last_name,
    )

    if (poll_results["votes_against_amount"] >= settings.votes_for_decision):
        bot.send_message(
            chat_id=call.message.chat.id,
            text=result_message_innocent.format(
                accused_full_name,
                accused_id,
            ),
            parse_mode="markdown",
        )
        # database.delete_poll(poll.id)
    else:
        bot.send_message(
            chat_id=call.message.chat.id,
            text=result_message_guilty.format(
                accused_full_name,
                accused_id,
                "Выебать в жопу"
            ),
            parse_mode="markdown",
        )
        # database.delete_poll(poll.id)

    return True
