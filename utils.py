nometa_message = \
    "Не задавай мета-вопросов в чате. Почему? Читай тут:\n\n"\
    "https://nometa.xyz/"


def handle_nometa(bot, message):
    if not (message.chat.type == "supergroup"):
        return False

    if not message.reply_to_message:
        return False

    bot.reply_to(
        message=message.reply_to_message,
        text=nometa_message,
        parse_mode="markdown",
    )
    return True
