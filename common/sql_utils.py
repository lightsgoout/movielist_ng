def get_cursor(using=None):
    from django import db
    using = using or db.DEFAULT_DB_ALIAS
    cursor = db.connections[using].cursor()
    return cursor


def raw_execute(sql, close=True, params=None, cursor=None, using=None):
    if not sql:
        return

    cursor = cursor or get_cursor(using)
    try:
        cursor.execute(sql, params if params else {})
    except:
        raise

    if close:
        from django.db import transaction
        transaction.commit_unless_managed()

    return cursor


def raw_fetch_list(sql, params=None, cursor=None, count=None, index=0, using=None):
    cursor = raw_execute(sql, cursor=cursor, params=params, using=None)
    if count:
        resultset = cursor.fetchmany(size=count)
    else:
        resultset = cursor.fetchall()
    return [row[index] for row in resultset]
