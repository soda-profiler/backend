
import sanic.response as res

async def healthView(request):
  return res.json({
    "status": "OK"
  })