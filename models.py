from pony import orm

db = orm.Database()


class Poll(db.Entity):
    id = orm.PrimaryKey(int, size=64, auto=True)
    chat_id = orm.Required(int, size=64)
    message_id = orm.Required(int, size=64)
    accuser_id = orm.Required(int, size=64)
    accused_id = orm.Required(int, size=64)
    votes = orm.Set("Vote")
    orm.composite_key(chat_id, message_id)
    orm.composite_key(chat_id, accused_id)


class Vote(db.Entity):
    id = orm.PrimaryKey(int, size=64, auto=True)
    poll_id = orm.Required(Poll)
    voted_id = orm.Required(int, size=64)
    to_ban = orm.Required(bool)
    orm.composite_key(poll_id, voted_id)


class Settings(db.Entity):
    id = orm.PrimaryKey(int, size=64, auto=True)
    chat_id = orm.Required(int, size=64, unique=True)
    votes_for_decision = orm.Required(int)
    punishment = orm.Required(str)
    days = orm.Required(int)
