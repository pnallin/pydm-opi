#!/usr/bin/python3
import sys
import src.paths
import src
import logging
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
            layout.addWidget(self.get_gauge(None,macros=pv))

    def load_pvs(self):
        if self.macros.get('device','') == 'UHV':
            from src.consts.agilent4uhv import devices
            for d in devices:
                self.pvs.append({'PV':d[1]+':Pressure-Mon', 'ALARM':d[1]+':Pressure-Mon.STAT'})
                self.pvs.append({'PV':d[2]+':Pressure-Mon', 'ALARM':d[2]+':Pressure-Mon.STAT'})
                self.pvs.append({'PV':d[3]+':Pressure-Mon', 'ALARM':d[3]+':Pressure-Mon.STAT'})
                self.pvs.append({'PV':d[4]+':Pressure-Mon', 'ALARM':d[4]+':Pressure-Mon.STAT'})
        elif self.macros.get('device','') == 'MKS':
            from src.consts.mks937b import devices
            for d in devices:
                self.pvs.append({'PV':d[4]+':Pressure-Mon-s', 'ALARM':d[4]+':Pressure-Mon.STAT'})
                self.pvs.append({'PV':d[5]+':Pressure-Mon-s', 'ALARM':d[5]+':Pressure-Mon.STAT'})
                self.pvs.append({'PV':d[6]+':Pressure-Mon-s', 'ALARM':d[6]+':Pressure-Mon.STAT'})
                self.pvs.append({'PV':d[7]+':Pressure-Mon-s', 'ALARM':d[7]+':Pressure-Mon.STAT'})
                self.pvs.append({'PV':d[8]+':Pressure-Mon-s', 'ALARM':d[8]+':Pressure-Mon.STAT'})
                self.pvs.append({'PV':d[9]+':Pressure-Mon-s', 'ALARM':d[9]+':Pressure-Mon.STAT'})
        else:
            logger.error('Wrong macro[\'device\'] ! {} '.format(self.macros))

    def get_gauge(self, parent, macros):
        frame = QtWidgets.QFrame(parent)
        frame.setGeometry(QtCore.QRect(10, 10, 400, 80))
        frame.setMinimumSize(400,80)
        frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        frame.setFrameShadow(QtWidgets.QFrame.Raised)
        frame.setObjectName("frame")

        alarmRec = PyDMDrawingRectangle(frame)
        alarmRec.channel = "ca://{}".format(macros.get('ALARM', None))
        alarmRec.setGeometry(QtCore.QRect(0, 0, 400, 80))
        alarmRec.setToolTip("ca://{}".format(macros.get('ALARM', None)))
        alarmRec.setProperty("alarmSensitiveContent", True)
        brush = QtGui.QBrush(QtGui.QColor(180, 180, 180))
        brush.setStyle(QtCore.Qt.NoBrush)
        alarmRec.setProperty("brush", brush)
        alarmRec.setObjectName("alarmRec")
        alarmRec.setStyleSheet("\
            margin:5px; border:3px solid rgb(0, 0, 0); \
        ")


        lblName = QtWidgets.QLabel(frame)
        lblName.setGeometry(QtCore.QRect(10, 50, 380, 20))
        lblName.setAlignment(QtCore.Qt.AlignCenter)
        lblName.setText("{}".format(macros.get('PV', None)))
        lblName.setObjectName("lblName")
        lblName.setToolTip("{}".format(macros.get('PV', None)))

        lblVal = PyDMLabel(frame)
        lblVal.setGeometry(QtCore.QRect(10, 10, 380, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        lblVal.setFont(font)
        lblVal.setToolTip("ca://{}".format(macros.get('PV', None)))
        lblVal.setAlignment(QtCore.Qt.AlignCenter)
        lblVal.setProperty("showUnits", False)
        lblVal.setObjectName("lblVal")
        lblVal.channel = "ca://{}".format(macros.get('PV', None))
        return frame

    def ui_filename(self):
        return src.paths.OVERVIEW_UI

    def ui_filepath(self):
        return src.get_abs_path(src.paths.OVERVIEW_UI)