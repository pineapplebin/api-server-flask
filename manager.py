import os
import datetime
from functools import wraps
from gevent import monkey, wsgi

monkey.patch_all()

from app import create_core
from flask_script import Manager
from flask_migrate import MigrateCommand

env = os.getenv('ENVIRONMENT', 'default')
core = create_core(env)
app = core.app
manager = Manager(app)

manager.add_command('db', MigrateCommand)

@manager.command
def runserver():
    if app.config['DEBUG']:
        # wsgi.WSGIServer(('0.0.0.0', 5000), app).serve_forever()
        app.run(host='0.0.0.0')
    else:
        wsgi.WSGIServer(('0.0.0.0', 5000), app).serve_forever()


@manager.command
def apidoc():
    import os
    import json
    from app.controllers import controllers

    json_path = os.path.join(os.path.dirname(__file__), 'app', 'doc.json')
    doc = dict()
    for c in controllers:
        doc[c.name] = c.format_doc()

    extra = dict()
    extra['updated_at'] = ' '.join(
        datetime.datetime.now().isoformat().split('T'))
    with open(json_path, 'w') as f:
        f.writelines(json.dumps(dict(doc=doc, extra=extra), indent=2))
    print('Update api document successed')


if __name__ == '__main__':
    manager.run(default_command='runserver')
