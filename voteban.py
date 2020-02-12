def verify_vote(bot, message):
    if not message.reply_to_message:
        return {
            "success": False,
            "error": "no_reply"
        }

    accused_id = message.reply_to_message.from_user.id          # ID Обвиняемый
    accuser_id = message.from_user.id                           # ID Обвинитель
    admins = bot.get_chat_administrators(message.chat.id)       # Админимтраторы
    admins_id = list(map(lambda admin: admin.user.id, admins))  # ID Админимтраторов
    bot_id = bot.get_me().id                                    # ID Бота

    if accused_id == accuser_id:
        return {
            "success": False,
            "error": "self_complaint"
        }
    elif accused_id == bot_id:
        return {
            "success": False,
            "error": "bot_complaint"
        }
    elif accused_id in admins_id:
        return {
            "success": False,
            "error": "admin_complaint"
        }
    else:
        return {
            "success": True,
            "error": None,
        }