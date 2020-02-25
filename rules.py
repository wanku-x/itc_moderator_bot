import logging

logging.basicConfig(
    filename="/home/wanku/itc_moderator_bot/debug.log",
    level=logging.INFO
)

rules_message = \
    "Правила чата:\n\n"\
    "1. Хуй сосать\n"\
    "2. Еблом качать\n"\
    "3. Хуйней страдать"

setrules_message = \
    "Чтобы создать правила чата, необходимо отправить сообщение "\
    "следующего вида:"


def handle_rules(bot, message):
    if message.chat.type == "group" or message.chat.type == "supergroup":
        bot.send_message(
            chat_id=message.chat.id,
            text=rules_message,
            parse_mode="markdown",
        )
        return True
    return False


def handle_setrules(bot, message):
    member_status = bot.get_chat_member(
        chat_id=message.chat.id,
        user_id=message.from_user.id,
    ).status

    if not (message.chat.type == "private"):
        return False

# if not (
#     (message.chat.type == "group" or message.chat.type == "supergroup") and
#     (member_status == "creator" or member_status == "administrator")
# ):
#     return False

    logging.info(message.text[9:])
    return True
