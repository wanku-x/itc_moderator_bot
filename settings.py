from schema import Schema, And, SchemaError
import json

import database

settings_message_error = \
    'Чтобы записать настройки чата, необходимо отправить сообщение '\
    'cледующего вида:\n'\
    '```'\
    '/settings\n'\
    '{\n'\
    '  "votes_for_decision": Integer,\n'\
    '  "punishment": "mute"|"kick"|"ban",\n'\
    '  "days": Integer\n'\
    '}\n'\
    '```\n\n'\
    '*votes_for_decision* - Сколько голосов необходимо '\
    'для принятия решения (банить/не банить)\n\n'\
    '*punishment* - Вид наказания (бан/кик/мьют)\n\n'\
    '*days* - Количество дней мьюта '\
    '(если наказание не мьют - ставьте значение 0)'\

settings_message_success = \
    'Настройки успешно установлены!'

settings_schema = Schema({
    'votes_for_decision': And(int),
    'rules': [
        {
            'description': And(str),
            'punishment': And(str, lambda p: (
                p == 'mute' or p == 'kick' or p == 'ban'
            )),
            'days': And(int),
        }
    ]
})


def validate_settings(settings_schema, settings):
    try:
        settings_schema.validate(settings)
        return True
    except SchemaError:
        return False


def handle_settings(bot, message):
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
        settings_from_message = json.loads(message.text[9:].strip())
    except json.decoder.JSONDecodeError:
        settings_from_message = None

    if not (
        settings_from_message and
        validate_settings(settings_schema, settings_from_message)
    ):
        bot.send_message(
            chat_id=message.chat.id,
            text=settings_message_error,
            parse_mode="markdown",
        )
        return False

    settings = database.get_settings(
        chat_id=message.chat.id,
    )

    if not settings:
        database.create_settings(
            chat_id=message.chat.id,
            votes_for_decision=settings_from_message["votes_for_decision"],
            rules=settings_from_message["rules"],
        )
    else:
        database.update_settings(
            id=settings.id,
            votes_for_decision=settings_from_message["votes_for_decision"],
            rules=settings_from_message["rules"],
        )

    bot.send_message(
        chat_id=message.chat.id,
        text=settings_message_success,
        parse_mode="markdown",
    )

    return True
