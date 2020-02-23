help_private_message = "Это помощь по моим командам!\n\n"\
                       "Это личное сообщение"

help_group_message = "Это помощь по моим командам!\n\n"\
                     "Это публичное сообщение"


def handle_help(bot, message):
    if message.chat.type == "private":
        bot.send_message(
            chat_id=message.chat.id,
            text=help_private_message,
            parse_mode="markdown",
        )
        return True
    if message.chat.type == "group" or message.chat.type == "supergroup":
        bot.send_message(
            chat_id=message.chat.id,
            text=help_group_message,
            parse_mode="markdown",
        )
        return True
    return False
