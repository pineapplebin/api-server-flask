import os
import json
from flask import render_template, current_app

from ..controller import CustomController

apidoc_controller = CustomController(
    name='apidoc', prefix='/apidoc', import_name=__name__,
    template_folder='templates')
apidoc_controller.REQUIRED_ENV = 'development'


@apidoc_controller.get('/')
def index():
    json_path = os.path.join(
        current_app.config['PROJECT_ROOT'], 'app', 'doc.json')
    with open(json_path, 'r') as f:
        apidoc = json.loads(f.read())

    return render_template(
        'apidoc.html', doc=apidoc['doc'], extra=apidoc['extra'],
        socketdoc={}, dumps=json.dumps)
