import logging
from pydm import Display
from epics import caput

from siriushlacon.agilent4uhv.consts import AGILENT_DEVICE_UI

logger = logging.getLogger()


class AgilentDevice(Display):

    def __init__(self, parent=None, args=[], macros=None):
        super(AgilentDevice, self).__init__(parent=parent, args=args, macros=macros, ui_filename=AGILENT_DEVICE_UI)
        self.macros = macros
        self.pv_protect_sp = 'ca://{}:Protect-SP_Backend'.format(self.macros['PREFIX'])
        self.pv_step_sp = 'ca://{}:Step-SP_Backend'.format(self.macros['PREFIX'])

        self.btnWriteProtect.clicked.connect(self.write_protect)
        self.btnWriteStep.clicked.connect(self.write_step)

    def write_protect(self):
        data = 0
        if self.chProtect1.isChecked():
            data |= 1 << 0
        if self.chProtect2.isChecked():
            data |= 1 << 1
        if self.chProtect3.isChecked():
            data |= 1 << 2
        if self.chProtect4.isChecked():
            data |= 1 << 3
        data = float(data)
        caput(pvname=self.pv_protect_sp, wait=False, timeout=0.5, value=data)
        logger.info('Write protect {0:4b} to {1}'.format(data, self.pv_protect_sp))

    def write_step(self):
        data = 0
        if self.chStep1.isChecked():
            data |= 1 << 0
        if self.chStep2.isChecked():
            data |= 1 << 1
        if self.chStep3.isChecked():
            data |= 1 << 2
        if self.chStep4.isChecked():
            data |= 1 << 3
        caput(pvname=self.pv_step_sp, wait=False, timeout=0.5, value=data)
        logger.info('Write step {0:4b} to {1}'.format(int(data), self.pv_step_sp))
