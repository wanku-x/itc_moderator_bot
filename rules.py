from schema import Schema, And, Use, SchemaError
import logging
import json

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
    "cледующего вида:\n"\
    '```'\
    '/setrules\n'\
    '{\n'\
    '  "votes_for_decision": Number,\n'\
    '  "rules":[\n'\
    '    {\n'\
    '      "description": String,\n'\
    '      "punishment": "mute"|"kick"|"ban",\n'\
    '      "days": Number\n'\
    '    },\n'\
    '  ]\n'\
    '}\n'\
    '```'

rules_schema = Schema({
    'votes_for_decision': And(Use(int)),
    'rules': [
        {
            'description': And(Use(str)),
            'punishment': And(Use(str)),
            'days': And(Use(int)),
        }
    ]
})


def validate_rules(rules_schema, rules):
    try:
        rules_schema.validate(rules)
        return True
    except SchemaError:
        return False


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

    if not (
        (message.chat.type == "group" or message.chat.type == "supergroup") and
        (member_status == "creator" or member_status == "administrator")
    ):
        return False

    try:
        rules = json.loads(message.text[9:].strip())
    except json.decoder.JSONDecodeError:
        rules = None

    if not (rules and validate_rules(rules_schema, rules)):
        bot.send_message(
            chat_id=message.chat.id,
            text=setrules_message,
            parse_mode="markdown",
        )
        return False

    logger.info(rules)

    return True
