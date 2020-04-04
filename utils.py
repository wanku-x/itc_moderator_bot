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


def remove_unwanted_message(bot, message):
    if not (message.chat.type == "supergroup"):
        return False

    # if not (
    #     message.new_chat_members or
    #     message.left_chat_member or
    #     message.new_chat_title or
    #     message.new_chat_photo or
    #     message.audio or
    #     message.document or
    #     message.game or
    #     message.video or
    #     message.voice or
    #     message.video_note or
    #     message.contact or
    #     message.location or
    #     message.venue or
    #     message.invoice or
    #     message.successful_payment
    # ):
    #     return True

    bot.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id,
    )
    return True
