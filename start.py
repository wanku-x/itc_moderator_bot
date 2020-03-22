start_message = \
    "Привет! Я бот, который будет модерировать твой чат!\n\n"\
    "Я умею запускать голосование за наказание "\
    "провинившихся участников чата. "\
    "Также есть функции для быстрого бана/кика/мьюта участников чата и "\
    "другие плюшки.\n\n"\
    "Введи команду `/help`, чтобы узнать, как работать с ботом."


def handle_start(bot, message):
    if message.chat.type == "private":
        bot.send_message(
            chat_id=message.chat.id,
            text=start_message,
            parse_mode="markdown",
        )
        return True
    return False
