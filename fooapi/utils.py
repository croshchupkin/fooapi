# -*- coding: utf-8 -*-
def validation_errors_to_unicode_message(messages_dict):
    msg_parts = []
    for key, messages in messages_dict.iteritems():
        if key == '_schema':
            key = u'schema'
        msg = u'{key}: {messages}'.format(
            key=key,
            messages=u' '.join(unicode(m) for m in messages))
        msg_parts.append(msg)

    return u' '.join(msg_parts)
