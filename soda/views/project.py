
from uuid import uuid4
from sanic.views import HTTPMethodView
import sanic.response as res
from sanic_jwt.decorators import protected, scoped, inject_user
from cassandra.cqlengine.query import LWTException

from ..models.user import User
from ..models.project import Project
from .serializer import model_serializer

class ProjectView(HTTPMethodView):
  decorators = [protected(), scoped('user'), inject_user()]

  async def post(self, request, user):
    payload = request.json
    
    payload['access_token'] = "some_token"
    payload['user_id'] = user['id']

    if 'name' not in payload:
      return res.json({
          "message": "name is required"
      }, status=400)
    
    project_exists = Project.objects(name=payload['name'], user_id=user['id']).allow_filtering().first()
    if project_exists:
      return res.json({
        "message": "Project Already Exists",
      }, status=409)

    project = Project.create(**payload)

    return res.json({
      "message": "Project Created",
      "project_id": str(project.id)
    }, status=200)


  async def get(self, request, user):
    print(user)
    payload = Project.objects(user_id=user['id']).all()
    payload = [{
      **p,
      "id": str(p['id']), 
      "user_id": str(p['user_id'])
      } for p in payload]

    return res.json(payload)
