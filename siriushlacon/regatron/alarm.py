import datetime
import logging

from pydm import Display
from qtpy.QtCore import QDateTime
from qtpy.QtWidgets import QTreeWidgetItem

from siriushlacon.regatron.consts import ALARM_UI, STD_READINGS, EXT_READINGS, EXTENDED_MAP, STANDARD_MAP
from siriushlacon.utils.alarm import Alarm, Severity
from siriushlacon.utils.archiver import get_data_from_archiver
from siriushlacon.utils.consts import SP_TZ

logger = logging.getLogger()


class AlarmDisplay(Display):
    """
    Query alarms from the archiver appliance and display in a human readable format
    """

    @staticmethod
    def reading_tree_item(reading, mapping: dict = None):
        """
        Get data from archiver and transform into a node with branches according to the bit value defined by the mapping.

        :param reading: A data item from the archiver request
        :param mapping: Mapping for each bit on the integer where the key is an integer from
        representing the bit position starting from zero and the key is a string with it's meaning
        :return: A QTreeWidgetItem
        """
        # Timestamp
        if mapping is None:
            mapping = {0: 'Zero', 1: 'One', 2: 'Two'}
        timestamp = str(datetime.datetime.fromtimestamp(reading['secs']).astimezone(SP_TZ))
        severity = Severity.nameOf(reading['severity'])
        alarm_status = Alarm.nameOf(reading['status'])
        value = reading['val']

        node = QTreeWidgetItem(['{} {} {} {}'.format(timestamp, value, severity, alarm_status)])

        # A meaning per bit defined at the "mapping"
        for k, v in mapping.items():
            if value & 1 << k:
                node_child = QTreeWidgetItem(['{}: {}'.format(k, v)])
                node.addChild(node_child)

        return node

    def __init__(self, parent=None, macros=None, **kwargs):
        super().__init__(parent=parent, macros=macros, ui_filename=ALARM_UI)
        self.macros = macros
        self.btnNow.clicked.connect(self.set_time_now)
        self.btnSearch.clicked.connect(self.search_alarms)

        # Tree Widget
        self.treeStdWarn.setColumnCount(1)
        self.treeStdWarn.setHeaderLabels(['Standard Warning'])

        self.treeStdErr.setColumnCount(1)
        self.treeStdErr.setHeaderLabels(['Standard Error'])

        self.treeExtWarn.setColumnCount(1)
        self.treeExtWarn.setHeaderLabels(['Extended Warning'])

        self.treeExtErr.setColumnCount(1)
        self.treeExtErr.setHeaderLabels(['Extended Error'])

        self.set_time_now()
        self.search_alarms()

    def get_PV(self, signal, std=False, error=False):
        """
        Build a PV name

        :param signal: Signal name, the last component of the PV
        :param std: True for 'Std' else 'Ext'
        :param error: True for 'Err' else 'Warn'
        :return: the PV name
        """
        return '{}:{}-{}{}{}'.format(self.macros['P'], self.macros['T'],
                                     'Std' if std else 'Ext', 'Err' if error else 'Warn', signal)

    def set_time_now(self):
        """ Set current date and time to the "dfTo" widget """
        self.dtTo.setDateTime(QDateTime.currentDateTime())

    def do_search(self, alarm_tree, time_to, time_from, std, error):
        """
        Query and build the alarm tree

        :param alarm_tree: QTreeWidget to append the alarms
        :param time_to: final time
        :param time_from: initial time
        :param std: True for 'Std' else 'Ext', defines if it's a standard or extended alarm
        :param error: True for 'Err' else 'Warn', defines if it's an error or a warning
        """
        alarm_tree.clear()
        # For each PV
        for signal in ['Group-Mon', *(STD_READINGS if std else EXT_READINGS)]:
            pv = self.get_PV(signal, std=std, error=error)
            response = get_data_from_archiver(pv=pv, to=time_to, from_=time_from, fetch_latest_metadata=False)
            pv_node = QTreeWidgetItem(['{}'.format(pv)])
            alarm_tree.addTopLevelItem(pv_node)

            if response.status_code == 200:
                logger.debug(response.text)
                if len(response.json()) > 0:
                    for data in response.json()[0]['data']:
                        pv_node_child = self.reading_tree_item(data, mapping=STANDARD_MAP if std else EXTENDED_MAP)
                        pv_node.addChild(pv_node_child)
                else:
                    logger.info('empty response for request {} from {} to {}'.format(pv, time_from, time_to))
            else:
                logger.warning('invalid status code for request {} from {} to {}'.format(pv, time_from, time_to))

    def search_alarms(self):
        """ Update all tree widgets """

        time_to = self.dtTo.dateTime().toPyDateTime().astimezone(SP_TZ)
        time_from = self.dtFrom.dateTime().toPyDateTime().astimezone(SP_TZ)

        self.do_search(alarm_tree=self.treeStdWarn, time_to=time_to, time_from=time_from, std=True, error=False)
        self.do_search(alarm_tree=self.treeStdErr, time_to=time_to, time_from=time_from, std=True, error=True)
        self.do_search(alarm_tree=self.treeExtWarn, time_to=time_to, time_from=time_from, std=False, error=False)
        self.do_search(alarm_tree=self.treeExtErr, time_to=time_to, time_from=time_from, std=False, error=True)
