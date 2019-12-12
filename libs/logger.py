import os

import logging
from logging import config

__all__ = ['logger']

LOG_PATH = './logs/.log'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'basic_formatter': {
            'format': '%(asctime)s %(levelname)-8s >> %(message)s'
        },
    },
    'filters':{},
    "loggers":{
            "scripts":{
                "handlers":["basic_stream", "basic_file"],
                "level": logging.DEBUG,
            }
        },
    'handlers': {
        'basic_stream': {
            'level': logging.DEBUG,
            'class': 'logging.StreamHandler',
            'formatter': 'basic_formatter',
            "stream": "ext://sys.stdout"
        },
        'basic_file': {
            'level' : logging.DEBUG,
            'class': 'logging.FileHandler',
            'formatter': 'basic_formatter',
            'filename': LOG_PATH
        },
    }
}
if not os.path.exists(LOG_PATH):
    dirs_path = '/'.join(LOG_PATH.split('/')[:-1])
    os.makedirs(dirs_path, exist_ok=True)

config.dictConfig(LOGGING)
logger = logging.getLogger("scripts")