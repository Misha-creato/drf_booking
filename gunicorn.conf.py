from utils.logger import get_logger

from gunicorn.glogging import Logger as GLogger


logger = get_logger(__name__, 'gunicorn')


class GunicornLogger(GLogger):
    def setup(self, cfg):
        super(GunicornLogger, self).setup(cfg)
        self.access_log = logger
        self.error_log = logger


wsgi_app = 'config.wsgi'
worker_class = 'gevent'
logger_class = GunicornLogger


