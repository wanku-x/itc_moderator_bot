from functools import reduce
from pony import orm
from models import Poll, Vote, Settings


#
#   Poll methods
#
@orm.db_session
def create_poll(
    chat_id,
    message_id,
    accuser_id,
    accused_id,
    accused_message,
    accused_message_id,
    reason,
):
    try:
        poll = Poll(
            chat_id=chat_id,
            message_id=message_id,
            accuser_id=accuser_id,
            accused_id=accused_id,
            accused_message=accused_message,
            accused_message_id=accused_message_id,
            reason=reason,
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
def get_poll_results(poll_id):
    votes = Vote.select(lambda vote: vote.poll_id.id == poll_id)[:]
    poll_results = [vote.to_ban for vote in votes]
    votes_for_amount = sum(poll_results)
    votes_against_amount = len(poll_results) - votes_for_amount
    return {
        "votes_for_amount": votes_for_amount,
        "votes_against_amount": votes_against_amount,
    }


@orm.db_session
def delete_poll(id):
    try:
        Poll[id].delete()
        orm.commit()
    except:  # noqa
        return False
    else:
        return True


#
#   Vote methods
#
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


#
#   Settings methods
#
@orm.db_session
def create_settings(chat_id, votes_for_decision, punishment, days):
    try:
        settings = Settings(
            chat_id=chat_id,
            votes_for_decision=votes_for_decision,
            punishment=punishment,
            days=days,
        )
        orm.commit()
    except:  # noqa
        settings = None
    finally:
        return settings


@orm.db_session
def update_settings(id, votes_for_decision, punishment, days):
    try:
        settings = Settings[id]
        settings.votes_for_decision = votes_for_decision
        settings.punishment = punishment
        settings.days = days
        orm.commit()
    except:  # noqa
        settings = None
    finally:
        return settings


@orm.db_session
def get_settings(chat_id):
    return Settings.get(
        chat_id=chat_id,
    )
