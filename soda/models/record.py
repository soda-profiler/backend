# coding: utf-8
from datetime import datetime
import uuid

from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model


class Record(Model):
  __keyspace__ = "soda"
  id            = columns.UUID(primary_key=True, default=uuid.uuid4)
  user_id       = columns.UUID(index=True)
  project_id    = columns.UUID(index=True)
  start_time    = columns.DateTime()
  end_time      = columns.DateTime()
  received_at   = columns.DateTime(default=datetime.now)
  function_name = columns.Text()
  arguments     = columns.Text()
  call_params   = columns.Text()
  type          = columns.Text()
