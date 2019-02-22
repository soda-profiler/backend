import hashlib
import hmac
import uuid
from datetime import datetime

from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model


class User(Model):
    __keyspace__ = "soda"
    id = columns.UUID(primary_key=True, default=uuid.uuid4)
    email = columns.Text()
    password = columns.Text()
    created_at = columns.DateTime(default=datetime.now)
    is_valid = columns.Boolean(default=False)
    scopes = columns.List(value_type=columns.Text)
