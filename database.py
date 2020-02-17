def create_poll(db, chat_id, message_id, accuser_id, accused_id):
    db_cursor = db.cursor()
    db_cursor.execute(
        "INSERT INTO `polls` "
        "(`id`, `chat_id`, `message_id`, `accuser_id`, `accused_id`) "
        "VALUES (NULL, %s, %s, %s, %s)",
        (
            chat_id,
            message_id,
            accuser_id,
            accused_id,
        )
    )
    db.commit()


def get_poll(db, chat_id, message_id):
    db_cursor = db.cursor()
    db_cursor.execute(
        "SELECT * FROM `polls` WHERE `chat_id`=%s AND `message_id`=%s",
        (
            chat_id,
            message_id,
        )
    )
    return db_cursor.fetchone()


def delete_poll(db, chat_id, message_id):
    pass


def get_poll_results(db, poll_id):
    db_cursor = db.cursor()
    db_cursor.execute(
        "SELECT SUM(`to_ban`), "
        "SUM(CASE WHEN `to_ban` = 1 THEN 0 ELSE 1 END) "
        "FROM `votes` WHERE `poll_id`=%s",
        (
            poll_id,
        )
    )
    return db_cursor.fetchone()


def create_vote(db, poll_id, voted_id, to_ban):
    db_cursor = db.cursor()
    db_cursor.execute(
        "INSERT INTO `votes` (`id`, `poll_id`, `voted_id`, `to_ban`) "
        "VALUES (NULL, %s, %s, %s)",
        (
            poll_id,
            voted_id,
            to_ban,
        )
    )
    db.commit()


def update_vote(db, vote_id, to_ban):
    db_cursor = db.cursor()
    db_cursor.execute(
        "UPDATE `votes` SET `to_ban`=%s "
        "WHERE `id`=%s",
        (
            to_ban,
            vote_id,
        )
    )
    db.commit()


def get_vote(db, poll_id, voted_id):
    db_cursor = db.cursor()
    db_cursor.execute(
        "SELECT * FROM `votes` WHERE `poll_id`=%s AND `voted_id`=%s",
        (
            poll_id,
            voted_id,
        )
    )
    return db_cursor.fetchone()
