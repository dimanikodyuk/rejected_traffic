import logging.config
import logging
from logging.handlers import RotatingFileHandler
from sys import platform
import os

if os.name == 'nt':
    dir = 'C:/GIT/rejected_traffic'
else:
    dir = '/root/rej_traffic/rejected_traffic/logs'

log_file_handler = RotatingFileHandler(f'{dir}/api.log', maxBytes=10485760,
                                       backupCount=10)
log_file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
log_file_handler.setLevel(logging.INFO)

print(dir)

dict_log_config = {
    'version': 1,
    'handlers': {
        'RotatingFileHandler': {
            'filename': f'{dir}/admitad.log',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 50000000,
            'backupCount': 10,
            'formatter': 'api_formatter',
        },
        'RotatingFileHandler2': {
            'filename': f'{dir}/finline.log',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 50000000,
            'backupCount': 10,
            'formatter': 'api_formatter',
        },
        'RotatingFileHandler3': {
            'filename': f'{dir}/finstorm.log',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 50000000,
            'backupCount': 10,
            'formatter': 'api_formatter',
        },
        'RotatingFileHandler4': {
            'filename': f'{dir}/teleport.log',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 50000000,
            'backupCount': 10,
            'formatter': 'api_formatter',
        },
        'RotatingFileHandler5': {
            'filename': f'{dir}/test.log',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 50000000,
            'backupCount': 10,
            'formatter': 'api_formatter',
        },
        'RotatingFileHandler6': {
            'filename': f'{dir}/ecpc.log',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 50000000,
            'backupCount': 10,
            'formatter': 'api_formatter',
        },
        'RotatingFileHandler7': {
            'filename': f'{dir}/credit_yes.log',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 50000000,
            'backupCount': 10,
            'formatter': 'api_formatter',
        },
    },
    'loggers': {
        'admitad': {
            'handlers': ['RotatingFileHandler'],
            'level': 'INFO'
        },
        'finline': {
            'handlers': ['RotatingFileHandler2'],
            'level': 'INFO'
        },
        'finstorm': {
            'handlers': ['RotatingFileHandler3'],
            'level': 'INFO'
        },
        'teleport': {
            'handlers': ['RotatingFileHandler4'],
            'level': 'INFO'
        },
        'test': {
            'handlers': ['RotatingFileHandler5'],
            'level': 'INFO'
        },
        'ecpc': {
            'handlers': ['RotatingFileHandler6'],
            'level': 'INFO'
        },
        'credit_yes': {
            'handlers': ['RotatingFileHandler7'],
            'level': 'INFO'
        },
    },
    'formatters': {
        'api_formatter': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
    }
}

logging.config.dictConfig(dict_log_config)
logger_admitad = logging.getLogger('admitad')
logger_finline = logging.getLogger('finline')
logger_finme = logging.getLogger('finme')
logger_teleport = logging.getLogger('teleport')
logger_finstorm = logging.getLogger('finstorm')
logger_test = logging.getLogger('test')
logger_ecpc = logging.getLogger('ecpc')
logger_credit_yes = logging.getLogger('credit_yes')
