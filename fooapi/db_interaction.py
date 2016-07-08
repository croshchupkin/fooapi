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


def get_single_user(user_id):
    return User.query.options(db.joinedload(User.contacts)).get_or_404(user_id)


def add_user(data):
    user = User(**data)
    db.session.add(user)
    db.session.commit()
    return user.id


def update_user(user_id, data):
    user = User.query.get_or_404(user_id)
    user.set_fields(data)
    db.session.commit()


def delete_user(user_id):
    db.session.delete(User.query.get_or_404(user_id))
    db.session.commit()


def get_user_contacts_list(user_id, limit=None, offset=None):
    # so that we could show a 404 page when a non-existent user id is passed
    # to the API endpoint
    User.query.get_or_404(user_id)

    query = Contact\
        .query\
        .filter_by(user_id=user_id)\
        .order_by(Contact.created_at.asc())
    total = query.count()
    query = _limit_and_offset_query(query, limit, offset)
    return query.all(), total


def add_user_contact(user_id, contact_data):
    user = User.query.options(db.joinedload(User.contacts)).get_or_404(user_id)
    contact = Contact(**contact_data)
    user.contacts.append(contact)
    db.session.commit()
    return contact.id


def delete_contact(contact_id):
    db.session.delete(Contact.query.get_or_404(contact_id))
    db.session.commit()


def delete_all_user_contacts(user_id):
    # so that we could show a 404 page when a non-existent user id is passed
    # to the API endpoint
    User.query.get_or_404(user_id)
    Contact.query.filter_by(user_id=user_id).delete()
    db.session.commit()


def get_single_contact(contact_id, join_user=False):
    if join_user:
        return Contact\
            .query\
            .options(db.joinedload(Contact.user))\
            .get_or_404(contact_id)
    else:
        return Contact.query.get_or_404(contact_id)


def update_contact(contact_id, data):
    contact = Contact.query.get_or_404(contact_id)
    contact.set_fields(data)
    db.session.commit()


def _limit_and_offset_query(query, limit=None, offset=None):
    if limit is not None:
        query = query.limit(limit)
    if offset is not None:
        query = query.offset(offset)
    return query
