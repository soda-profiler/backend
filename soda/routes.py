from sanic_cors import CORS

from .views.user import UserView
from .views.project import ProjectView
from .views.record import RecordView
from .views.health import healthView

def setup_routes(app):
  app.add_route(UserView.as_view(), '/api/v1.0/users')
  app.add_route(ProjectView.as_view(), '/api/v1.0/projects')
  app.add_route(RecordView.as_view(), '/api/v1.0/records', methods=['GET', 'POST', 'OPTIONS'])  
  app.add_route(healthView, '/api/v1.0/version', methods=['GET',])
  # app.router.add_static('/static/', path='../static', name='static')
  CORS(app, resources={
      r"/*": {"origins": "*"},
    }, 
    automatic_options=True
  )

  return app
