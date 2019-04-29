#!/usr/bin/python3
import sys
import src.paths
import src
import logging
import re
import pydm

from pydm.widgets.label import PyDMLabel
from pydm.widgets.drawing import PyDMDrawingRectangle

from PyQt5 import QtCore, QtGui, QtWidgets
from src import FlowLayout

logger = logging.getLogger()

class Overview(pydm.Display):
    def __init__(self, parent=None, args=None, macros=None):
        super(Overview, self).__init__(parent=parent, args=args, macros=macros)
        self.macros = macros
        self.pvs = []
        self.load_pvs()
        self.mainArea.setWidgetResizable(True)
        layout = FlowLayout(self.scrollAreaContent)
        for pv in self.pvs:
            layout.addWidget(self.get_gauge(None,pv=pv))

    def load_pvs(self):
        from src.consts.mks937b import data
        ch_reg = re.compile(r':[A-C][0-9]')
        for d_row in data:
            if d_row.enable:
                i = 0
                for ch_prefix in d_row.channel_prefix:
                    if i >= 2:
                        # Filter out PR
                        continue
                    if ch_reg.match(ch_prefix[-3:]):
                        # Filter out unnused channels by it's name
                        continue

                    self.pvs.append({
                        'PV'    : ch_prefix + ':Pressure-Mon-s',
                        'DISP'  : ch_prefix + ':Pressure-Mon',
                        'ALARM' : ch_prefix + ':Pressure-Mon.STAT',
                        'DEVICE': d_row.device,
                        'SEC.'  : d_row.sector,
                        'RACK'  : d_row.rack,
                        'RS485' : d_row.rs485_id,
                        'IP'    : d_row.ip
                    })
                    i += 1


    def get_gauge(self, parent, pv):
        aux = []
        for k, v in pv.items():
            aux.append('{}\t{}\n'.format(k, v))
        tooltip = ''.join(aux)

        frame = QtWidgets.QFrame(parent)
        frame.setGeometry(QtCore.QRect(10, 10, 400, 80))
        frame.setMinimumSize(400,80)
        frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        frame.setFrameShadow(QtWidgets.QFrame.Raised)
        frame.setObjectName("frame")

        alarmRec = PyDMDrawingRectangle(frame)
        alarmRec.channel = "ca://{}".format(pv.get('ALARM', None))
        alarmRec.setGeometry(QtCore.QRect(0, 30, 400, 50))
        alarmRec.setToolTip(tooltip)
        alarmRec.setProperty("alarmSensitiveContent", True)
        brush = QtGui.QBrush(QtGui.QColor(180, 180, 180))
        brush.setStyle(QtCore.Qt.NoBrush)
        alarmRec.setProperty("brush", brush)
        alarmRec.setObjectName("alarmRec")
        alarmRec.setStyleSheet("\
            margin:5px; border:3px solid rgb(0, 0, 0); \
        ")

        alarmRec = PyDMDrawingRectangle(frame)
        alarmRec.channel = "ca://{}".format(pv.get('DEVICE', None) + ':Pressure:Read')
        alarmRec.setGeometry(QtCore.QRect(0, 0, 400, 30))
        alarmRec.setToolTip('Connection Indicator: {}\t{}'.format('DEVICE',pv.get('DEVICE', None) + ':Pressure:Read'))
        alarmRec.setProperty("alarmSensitiveContent", True)
        brush = QtGui.QBrush(QtGui.QColor(180, 180, 180))
        brush.setStyle(QtCore.Qt.NoBrush)
        alarmRec.setProperty("brush", brush)
        alarmRec.setObjectName("alarmRec")
        alarmRec.setStyleSheet("\
            border:3px solid rgb(0, 0, 0); \
        ")


        lblName = QtWidgets.QLabel(frame)
        lblName.setGeometry(QtCore.QRect(10, 50, 380, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        lblName.setFont(font)
        lblName.setAlignment(QtCore.Qt.AlignCenter)
        lblName.setText("{}".format(pv.get('DISP', None)))
        lblName.setObjectName("lblName")
        lblName.setToolTip(tooltip)


        lblVal = PyDMLabel(frame)
        lblVal.setGeometry(QtCore.QRect(10, 10, 380, 30))
        font = QtGui.QFont()
        font.setPointSize(16)
        lblVal.setFont(font)
        lblVal.setToolTip(tooltip)
        lblVal.setAlignment(QtCore.Qt.AlignCenter)
        lblVal.setProperty("showUnits", False)
        lblVal.setObjectName("lblVal")
        lblVal.channel = "ca://{}".format(pv.get('PV', None))
        lblVal.precisionFromPV = False
        lblVal.precision = 2
        if self.macros.get('FORMAT', '') == 'EXP':
            lblVal.displayFormat = PyDMLabel.DisplayFormat.Exponential
        return frame

    def ui_filename(self):
        return src.paths.OVERVIEW_UI

    def ui_filepath(self):
        return src.get_abs_path(src.paths.OVERVIEW_UI)