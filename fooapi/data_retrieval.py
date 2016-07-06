# -*- coding: utf-8 -*-
from fooapi.models import db, User, Contact


def get_users_list(limit=None, offset=None):
    """
    limit int - the results' limit
    offset int - the results' offset

    returns the list of User objects and the total number of users.
    """
    query = User\
        .query\
        .options(db.joinedload(User.contacts))\
        .order_by(User.created_at.asc())

    total = query.count()

    query = _limit_and_offset_query(query, limit, offset)
    return query.all(), total


def add_user_data(data):
    pass


def _limit_and_offset_query(query, limit=None, offset=None):
    if limit is not None:
        query = query.limit(limit)
    if offset is not None:
        query = query.offset(offset)
    return query
