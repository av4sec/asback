import os
import logging
import sqlite3

from logging import handlers


HTTP_OK_BASIC = 200
HTTP_OK_CREATED = 201
HTTP_OK_ACCEPTED = 202
HTTP_OK_NORESPONSE = 204
HTTP_BAD_REQUEST = 400
HTTP_BAD_UNAUTHORIZED = 401
HTTP_BAD_FORBIDDEN = 403
HTTP_BAD_NOTFOUND = 404
HTTP_BAD_CONFLICT = 409
HTTP_SERVICE_UNAVAILABLE = 503
HTTP_INTERNAL_TIMEOUT = 504


class InvalidAPIUsage(Exception):
    status_code = HTTP_BAD_REQUEST

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        ret_val = dict(self.payload or ())
        ret_val['message'] = self.message
        return ret_val


class LogFormatter(logging.Formatter):
    datefmt = '%Y-%m-%d %H:%M:%S'

    def format(self, record):
        error_location = "%s.%s" % (record.name, record.funcName)
        line_number = "%s" % (record.lineno)
        location_line = error_location[:32] + ":" + line_number
        s = "%.19s [%-8s] [%-36s] %s" % (self.formatTime(record, self.datefmt),
                                         record.levelname,  location_line,
                                         record.getMessage())
        return s


def setup_logger():
    generated_files = 'logs'
    ALL_LOG_FILENAME = '{0}/all.log'.format(generated_files)
    ERROR_LOG_FILENAME = '{0}/error.log'.format(generated_files)
    if not os.path.exists(generated_files):
        os.makedirs(generated_files)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to info
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    handler.setFormatter(LogFormatter())
    logger.addHandler(handler)

    # create error file handler and set level to error
    handler = logging.handlers.RotatingFileHandler(ERROR_LOG_FILENAME,
                                                   maxBytes=1000000,
                                                   backupCount=100)
    handler.setLevel(logging.ERROR)
    handler.setFormatter(LogFormatter())
    logger.addHandler(handler)

    # create debug file handler and set level to debug
    handler = logging.handlers.RotatingFileHandler(ALL_LOG_FILENAME,
                                                   maxBytes=1000000,
                                                   backupCount=100)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(LogFormatter())
    logger.addHandler(handler)

    print('Logging into directory {}\n'.format(generated_files))


def get_db(app):
    if not hasattr(app, 'sqlite_db'):
        rv = sqlite3.connect(app.config['DATABASE'])
        rv.row_factory = sqlite3.Row
        app.sqlite_db = rv
        with app.open_resource('schema.sql', mode='r') as f:
            app.sqlite_db.cursor().executescript(f.read())
            app.sqlite_db.commit()
    return app.sqlite_db


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
