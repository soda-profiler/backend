from uuid import UUID
from datetime import datetime, date

def model_serializer(model):
  model = vars(model)
  serialized_model = {}
  for name, field in model.items():
    if isinstance(field, (date, datetime)):
      serialized_model[name] = field.totimestamp()

    elif isinstance(field, UUID):
      serialized_model[name] = str(field)
    
    else:
      serialized_model[name] = field

  return serialized_model
