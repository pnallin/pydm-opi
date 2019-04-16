#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
from os import path

from pydm import Display
from pydm.utilities import IconFont
from pydm.widgets import PyDMRelatedDisplayButton, PyDMEmbeddedDisplay, PyDMLabel

from PyQt5.QtWidgets import QComboBox, QLabel, QTableWidgetItem
from PyQt5.QtCore import pyqtSlot, Qt, pyqtSignal

from src import get_label, TableDataController
from src.consts.mks937b import devices, COLD_CATHODE, PIRANI
from src.paths import get_abs_path, TABLE_UI, DEVICE_MENU

class MKSTableDataController(TableDataController):
    def __init__(self, table, devices=[], table_batch=24, horizontal_header_labels=[], *args, **kwargs):
        return super().__init__(table, devices=devices, table_batch=table_batch, horizontal_header_labels=horizontal_header_labels, *args, **kwargs)

    def init_table(self):
        self.table.setRowCount(self.table_batch)
        self.table.setColumnCount(len(self.horizontalHeaderLabels))
        self.table.setHorizontalHeaderLabels(self.horizontalHeaderLabels)
        for actual_row in range(self.table_batch):
                self.table.setCellWidget(actual_row, 0, QLabel(''))
                self.table.setCellWidget(actual_row, 1, QLabel(''))
                self.table.setCellWidget(actual_row, 2, get_label(self.table, '', '', displayFormat=3, precision=2))
                self.table.setCellWidget(actual_row, 3, get_label(self.table, '', ''))
                self.table.setCellWidget(actual_row, 4, get_label(self.table, '', ''))
                rel = PyDMRelatedDisplayButton(self.table, get_abs_path(DEVICE_MENU))
                rel.openInNewWindow = True
                self.table.setCellWidget(actual_row, 5, rel)

    def filter(self, pattern):
        if pattern != self.filter_pattern:
            self.filter_pattern = pattern if pattern != None else ''
            self.batch_offset = 0
            self.filter_pattern = pattern

            for data in self.table_data:
                data['render'] = self.filter_pattern in data['device'] or self.filter_pattern in data['gauge']
            self.update_content.emit()

    def load_table_data(self):
        self.table_data = []
        for device in self.devices:
            # Gauges are from data[4:]
            # Device is data[0]
            macro = \
                '{"DEVICE" :"' +  device[0] + '",\
                "G1":"' + device[4] + '",\
                "G2":"' + device[5] + '",\
                "G3":"' + device[6] + '",\
                "G4":"' + device[7] + '",\
                "G5":"' + device[8] + '",\
                "G6":"' + device[9] + '",\
                "A":"' + device[1] + '",\
                "B":"' + device[2] + '", \
                "C":"' + device[3] + '"}'

            for item in device[4:]:
                self.table_data.append({'device':device[0], 'gauge':item, 'macro':macro, 'render':True})
        self.total_rows = len(self.table_data)
        self.update_content.emit()

    def update_table_content(self):

        # Maximum Allowed
        if self.batch_offset >= self.total_rows:
            return

        # Adding New Content
        actual_row = 0
        dataset_row = 0
        self.table.setVerticalHeaderLabels([str(i) for i in range(self.batch_offset, self.table_batch + self.batch_offset)])

        for data in self.table_data:
            if actual_row == self.table_batch:
                continue

            # To render or not to render  ...
            if data['render'] and dataset_row >= self.batch_offset:
                self.table.setRowHidden(actual_row, False)
                # Channel Access
                device_ca = 'ca://' + data['device']
                channel_ca = 'ca://' + data['gauge']

                self.table.cellWidget(actual_row, 0).setText(data['gauge'])
                self.table.cellWidget(actual_row, 1).setText(data['device'])
                self.connect_widget(actual_row, 2, channel_ca + ':Pressure-Mon-s')
                self.connect_widget(actual_row, 3, channel_ca + ':Pressure-Mon.STAT')
                self.connect_widget(actual_row, 4, device_ca + ':Unit')
                self.connect_widget(actual_row, 5, None, data['macro'])
                actual_row += 1

            dataset_row += 1

        for row in range(actual_row, self.table_batch):
            self.table.setRowHidden(row, True)


class MKS(Display):

    def __init__(self, parent=None, args=[], macros=None):
        super(MKS, self).__init__(
            parent=parent, args=args, macros=macros)

        table_batch = len(devices) * 6
        horizontal_header_labels = [
            'Gauge',
            'Device',
            'Pressure',
            'Alarm',
            'Unit',
            'Details']

        self.tdc = MKSTableDataController(self.table,
                    devices=devices, table_batch=table_batch, horizontal_header_labels=horizontal_header_labels)

        self.tfFilter.editingFinished.connect(
            lambda: self.filter(self.tfFilter.text()))

        self.btnNavLeft.clicked.connect(lambda: self.update_navbar(False))
        self.btnNavLeft.setIcon(IconFont().icon('arrow-left'))
        self.btnNavRight.clicked.connect(lambda: self.update_navbar(True))
        self.btnNavRight.setIcon(IconFont().icon('arrow-right'))

    def filter(self, pattern):
        self.tdc.filter(pattern)

    def update_navbar(self, increase = True):
        self.tdc.changeBatch(increase)

    def filter(self, pattern):
        self.tdc.filter(pattern)

    def ui_filename(self):
        return TABLE_UI

    def ui_filepath(self):
        return get_abs_path(TABLE_UI)
