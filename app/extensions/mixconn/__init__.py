
from .pool import Pool


class MixConn:

    def __init__(self, app=None):
        """Flask extension"""
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """create and register a blueprint with the Flask application.

        :param app:
            An application instance
        """

        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['mixconn'] = self
        app.context_processor(lambda: {'mixconn': self})
        self.pool = Pool()
