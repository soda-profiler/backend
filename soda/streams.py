
# @sio.on('recordsChange')
async def add_item(sid):
    await sio.emit('recordsChanged', list())


# @app.route("/backend")
async def socket_connection(request):
    return res.json({ })
