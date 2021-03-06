#!/bin/bash
import datetime
import logging
import os
import platform
import urllib.request

import pkg_resources
import pytz

logger = logging.getLogger()


def get_abs_path(relative):
    return pkg_resources.resource_filename(__name__, relative)


FILE = get_abs_path('Redes e Beaglebones.xlsx')

SP_TZ = pytz.timezone("America/Sao_Paulo")
TIME_ZERO = datetime.timedelta(0)
ARCHIVER_URL = 'http://10.0.38.42/retrieval/data/getData.json'

url = 'http://10.0.38.42/streamdevice-ioc/Redes%20e%20Beaglebones.xlsx'
try:
    if not os.access(os.path.dirname(FILE), os.W_OK):
        FILE = '/tmp/Redes e Beaglebones.xlsx'

    urllib.request.urlretrieve(url, FILE)
    logger.info('File {} updated.'.format(FILE))
except:
    logger.exception(
        'Failed to update the spreadsheet from http://10.0.38.42/streamdevice-ioc/Redes%20e%20Beaglebones.xlsx ! Using old data ...')

IS_LINUX = (os.name == 'posix' or platform.system() == 'Linux')

ARGS_HIDE_ALL = ['--hide-nav-bar', '--hide-menu-bar', '--hide-status-bar']

DRAW_ALARMS_NO_INVALID_QSS = ''
with open(get_abs_path('css/draw_no-invalid.qss')) as f:
    DRAW_ALARMS_NO_INVALID_QSS = ''.join(f.readlines())

TABLE_ALARMS_QSS = ''
with open(get_abs_path('css/table-alarm.qss')) as f:
    TABLE_ALARMS_QSS = ''.join(f.readlines())

OVERVIEW_UI = get_abs_path('ui/overview.ui')

# Images
CNPEM_IMG = get_abs_path('images/CNPEM.jpg')
LNLS_IMG = get_abs_path('images/sirius-hla-as-cons-lnls.png')
LTB_IMG = get_abs_path('images/ltb.png')
BOOSTER_IMG = get_abs_path('images/booster.png')
BTS_IMG = get_abs_path('images/btts.png')
STORAGE_RING_IMG = get_abs_path('images/storage_ring.png')
RINGB1A_IMG = get_abs_path('images/ringB1A.png')
RINGB2A_IMG = get_abs_path('images/ringB2A.png')

BO , SI, TB, TS = 'BO', 'SI', 'TB', 'TS'