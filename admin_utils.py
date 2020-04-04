import time

punishment_message = \
    "Пользователь [{0}](tg://user?id={1}) был {2} админом{3}."

punishment_time_message = \
    " на {0}д"


def can_use_admin_utils(bot, message):
    if not (message.chat.type == "supergroup"):
        return False

    member_status = bot.get_chat_member(
        chat_id=message.chat.id,
        user_id=message.from_user.id,
    ).status

    if not (member_status == "creator" or member_status == "administrator"):
        return False

    if not message.reply_to_message:
        return False

    return True


def handle_ban(bot, message):
    if not can_use_admin_utils(bot, message):
        return False

    accused_id = message.reply_to_message.from_user.id
    accused_full_name = "{} {}".format(
        message.reply_to_message.from_user.first_name,
        message.reply_to_message.from_user.last_name,
    )

    bot.kick_chat_member(
        chat_id=message.chat.id,
        user_id=accused_id,
        until_date=time.time(),
    )

    bot.send_message(
        chat_id=message.chat.id,
        text=punishment_message.format(
            accused_full_name,
            accused_id,
            "забанен",
            "",
        ),
        parse_mode="markdown",
    )
    return True


def handle_kick(bot, message):
    if not can_use_admin_utils(bot, message):
        return False

    accused_id = message.reply_to_message.from_user.id
    accused_full_name = "{} {}".format(
        message.reply_to_message.from_user.first_name,
        message.reply_to_message.from_user.last_name,
    )

    bot.kick_chat_member(
        chat_id=message.chat.id,
        user_id=accused_id,
        until_date=time.time() + 60,
    )

    bot.send_message(
        chat_id=message.chat.id,
        text=punishment_message.format(
            accused_full_name,
            accused_id,
            "кикнут",
            "",
        ),
        parse_mode="markdown",
    )
    return True


def handle_mute(bot, message):
    if not can_use_admin_utils(bot, message):
        return False

    try:
        days = int(message.text[5:].strip())
    except ValueError:
        days = None

    if not days:
        return False

    accused_id = message.reply_to_message.from_user.id
    accused_full_name = "{} {}".format(
        message.reply_to_message.from_user.first_name,
        message.reply_to_message.from_user.last_name,
    )

    bot.restrict_chat_member(
        chat_id=message.chat.id,
        user_id=accused_id,
        until_date=time.time()+days*86400,
    )

    bot.send_message(
        chat_id=message.chat.id,
        text=punishment_message.format(
            accused_full_name,
            accused_id,
            "замьючен",
            punishment_time_message.format(days)
        ),
        parse_mode="markdown",
    )
    return True
