import sys
import os
import logging

from soda.main import create_app

LOG_FORMAT = '%(asctime)-15s %(levelname)s %(funcName)s line %(lineno)d  %(message)s'
logging.basicConfig(stream=sys.stdout, level=getattr(logging, os.getenv("LOG_LEVEL", "DEBUG")), format=LOG_FORMAT)

app = create_app()
