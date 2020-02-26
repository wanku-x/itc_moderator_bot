import database

rules_message_success = \
    'Правила чата:\n\n'

rules_message_error = \
    'В чате ещё не заданы правила.'


def handle_rules(bot, message):
    if not (message.chat.type == "group" or message.chat.type == "supergroup"):
        return False

    settings = database.get_settings(
        chat_id=message.chat.id
    )

    if not settings:
        bot.send_message(
            chat_id=message.chat.id,
            text=rules_message_error,
            parse_mode="markdown",
        )
        return False

    for i in range(settings.rules):
        rules_message_success = \
            rules_message_success + i + '. ' + settings.rules[i] + '\n'

    bot.send_message(
        chat_id=message.chat.id,
        text=rules_message_success,
        parse_mode="markdown",
    )

    return True
