import json
import logging


class LogglyJSONFormatter(logging.Formatter):

    def formatException(self, exc_info):
        """
        Format an exception so that it prints on a single line.
        """
        result = super(LogglyJSONFormatter, self).formatException(exc_info)
        return repr(result)

    def format(self, record):
        """
        :param record: sample record object: {
            'name': 'loki',
            'msg': 'some text',
            'args': (),
            'levelname': 'INFO',
            'levelno': 20,
            'pathname': 'server.py',
            'filename': 'server.py',
            'module': 'server',
            'exc_info': None,
            'exc_text': None,
            'stack_info': None,
            'lineno': 42,
            'funcName': 'get',
            'created': 1498404672.572333,
            'msecs': 572.3330974578857,
            'relativeCreated': 4496.434211730957,
            'thread': 140735896224704,
            'threadName': 'MainThread',
            'processName': 'MainProcess',
            'process': 5735}
        :return: 
        """
        if isinstance(record.msg, dict):
            message = json.dumps(record.msg)
        else:
            message = '{}'.format(record.msg)
        return json.dumps({
            'name': record.name,
            'module': record.module,
            'level': record.levelname,
            'lineno': record.lineno,
            'message': message
        })
