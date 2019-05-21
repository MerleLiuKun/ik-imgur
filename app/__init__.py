from sanic import Sanic
from werkzeug.utils import find_modules, import_string

import config


def register_blueprints(root, app):
    for name in find_modules(root, recursive=True):
        mod = import_string(name)
        if hasattr(mod, 'bp'):
            uri = name.split('.')
            version = uri[2].replace('_', '.')
            prefix = '/{0}/{1}'.format(uri[1], version)
            app.register_blueprint(mod.bp, url_prefix=prefix)


def create_app():
    app = Sanic(__name__)
    # parse config.
    app.config.from_object(config)

    # blueprints
    register_blueprints('app.api', app)

    return app
