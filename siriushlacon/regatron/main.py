#!/usr/bin/python3
import json
import pkg_resources
import logging

from pydm import Display
from pydm.widgets.channel import PyDMChannel
from pydm.widgets.related_display_button import PyDMRelatedDisplayButton
from pydm.widgets.label import PyDMLabel

from qtpy.QtGui import QPixmap
from qtpy.QtWidgets import QWidget, QGridLayout, QPushButton, QLabel, QSpacerItem, QSizePolicy
from qtpy.QtGui import QFont

from siriushlacon.regatron.consts import REGATRON_UI, DETAILS_MAIN, SIMPLE_MAIN, DETAILS_MAIN,\
    DATA_JSON, COMPLETE_MAIN
from siriushlacon.utils.consts import CNPEM_IMG, LNLS_IMG

logger = logging.getLogger()

def load_data():
    data = None
    with open(DATA_JSON, 'rb') as f:
        data = json.load(f)
    return data

def get_overview_detail(name):
    overview = PyDMRelatedDisplayButton(name)
    overview.macros = ['{"P":"' + name + '"}']
    overview.filenames = [COMPLETE_MAIN]
    overview.openInNewWindow = True
    overview.showIcon = False
    return overview

# def log(x):
    # logger.info(x)

class Launcher(Display):
    DIP = 'DIP'
    QUA = 'QUA'
    SEX = 'SEX'

    def __init__(self, parent=None, macros=None, **kwargs):
        super().__init__(parent=parent, ui_filename=REGATRON_UI)
        self.logo_cnpem.setPixmap(QPixmap(CNPEM_IMG))
        self.logo_lnls.setPixmap(QPixmap(LNLS_IMG))

        self.data = load_data()
        self.layoutDipoles = QGridLayout()
        self.layoutQuadrupoles = QGridLayout()
        self.layoutSextupoles = QGridLayout()

        self.tabDipoles.setLayout(self.layoutDipoles)
        self.tabQuadrupoles.setLayout(self.layoutQuadrupoles)
        self.tabSextupoles.setLayout(self.layoutSextupoles)

        self.dipole = []
        self.quadrupole = []
        self.sextupole = []

        for e in self.data:
            if e['type'] == self.QUA:
                self.quadrupole.append(e['pv'])
            elif e['type'] == self.DIP:
                self.dipole.append(e['pv'])
            elif e['type'] == self.SEX:
                self.sextupole.append(e['pv'])

        self.render(self.layoutDipoles, self.dipole)
        self.render(self.layoutQuadrupoles, self.quadrupole)
        self.render(self.layoutSextupoles, self.sextupole)

    def render(self, layout, data):
        i = 0
        for name in data:
            overview  = get_overview_detail(name)
            layout.addWidget(overview, i, 0)
            i += 1
        layout.setRowStretch(len(data), 10)

