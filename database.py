from pony import orm
from models import Poll, Vote


@orm.db_session
def create_poll(chat_id, message_id, accuser_id, accused_id):
    try:
        poll = Poll(
            chat_id=chat_id,
            message_id=message_id,
            accuser_id=accuser_id,
            accused_id=accused_id,
        )
        orm.commit()
    except:  # noqa
        poll = None
    finally:
        return poll


@orm.db_session
def get_poll(chat_id, message_id):
    return Poll.get(
        chat_id=chat_id,
        message_id=message_id,
    )


@orm.db_session
def check_poll(chat_id, accused_id):
    return Poll.get(
        chat_id=chat_id,
        accused_id=accused_id,
    )


@orm.db_session
def delete_poll(id):
    try:
        Poll[id].delete()
        orm.commit()
    except:  # noqa
        return False
    else:
        return True


@orm.db_session
def create_vote(poll_id, voted_id, to_ban):
    try:
        vote = Vote(
            poll_id=poll_id,
            voted_id=voted_id,
            to_ban=to_ban,
        )
        orm.commit()
    except:  # noqa
        vote = None
    finally:
        return vote


@orm.db_session
def get_vote(poll_id, voted_id):
    return Vote.get(
        poll_id=poll_id,
        voted_id=voted_id,
    )


@orm.db_session
def update_vote(id, to_ban):
    try:
        vote = Vote[id]
        vote.to_ban = to_ban
        orm.commit()
    except:  # noqa
        vote = None
    finally:
        return vote
