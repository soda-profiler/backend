from datetime import datetime
import json
import logging
from uuid import uuid4

from sanic.views import HTTPMethodView
import sanic.response as res
from sanic_jwt.decorators import protected, scoped, inject_user
from cassandra.cqlengine.query import LWTException

from ..models.user import User
from ..models.record import Record
from ..models.project import Project

logger = logging.getLogger(__name__)


class RecordView(HTTPMethodView): 
  decorators = [protected(), scoped('user'), inject_user()]
  
  async def post(self, request, user):

    payload = request.json

    project = Project.objects(name=payload['project_name']).first()
    payload = {
        "function_name": payload['name'],
        "start_time": datetime.fromtimestamp(payload['start']),
        "end_time": datetime.fromtimestamp(payload['end']),
        "arguments": json.dumps(payload['arguments']),
        "call_params": json.dumps(payload['call_params']),
        "type": payload['type'],        
        "project_id": project.id,
        "user_id": user['id'],
    }
    print(payload)

    record =  Record.create(**payload)

    return res.json({
      "status": 201,
      "message": "Record Created",
      "record_id": str(record.id)
    })


  async def get(self, request, user):
    payload = request.raw_args
    print(request.raw_args)
    project = Project.objects(name=payload['project_name']).allow_filtering().first()
    records = Record.objects(user_id=user['id'], project_id=project.id).allow_filtering().all()
    
    for record in records:
        if record['arguments']:
            record['arguments'] = json.loads(record['arguments'])  
            
        if record['call_params']:   
            record['call_params'] = json.loads(record['call_params'])
    payload = [{
      **r,
      "start_time": r['start_time'].timestamp(),
      "end_time": r['end_time'].timestamp(),
      "id": str(r['id']), 
      "project_id": str(r['project_id']),
      "user_id": str(r['user_id'])
      } for r in records]

    return res.json(payload)
