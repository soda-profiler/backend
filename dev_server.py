import sys
import os
import logging

from soda.main import create_app

logging.basicConfig(
    stream=sys.stdout,
    level=getattr(logging, os.getenv("LOG_LEVEL", "DEBUG")),
)

app = create_app()
app.run(host='0.0.0.0', port=80, debug=True)
