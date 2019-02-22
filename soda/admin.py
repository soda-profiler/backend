from pathlib import Path

from .models.user import User
from .models.project import Project
from .models.record import Record
from aiohttp_admin.layout_utils import generate_config


base_url = '/admin'
entities = [
    ("user", "id", User)
    ("Project", "id", Project),
    ("Record", "id", Record),
]

config_str = generate_config(entities, base_url)
path = Path(__file__).parent.absolute()

config_location = path / '..' / 'static/js/config2.js'
with open(str(config_location), 'w') as f:
    f.write(config_str)
