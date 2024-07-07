import uuid_utils as uuid


def uuid_factory():
    return uuid.uuid7().hex


def now_factory():
    from datetime import datetime
    return str(datetime.now())
