import uuid

from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model


class Project(Model):
  __keyspace__ = "soda"
  id           = columns.UUID(primary_key=True, default=uuid.uuid4)
  user_id      = columns.UUID(default=uuid.uuid4, index=True)
  name         = columns.Text(index=True)
  access_token = columns.Text()
