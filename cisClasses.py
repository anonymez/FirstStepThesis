import atexit

import sys
from pyVim.connect import SmartConnectNoSSL, Disconnect
import pyVmomi
from pyVmomi import vim
import inspect

class cis_2_1:
    def __init__(self, host):
        self.cis_2_1_passed = False
        configuration = host.QueryHostConnectionInfo().host.host.configManager.dateTimeSystem.dateTimeInfo.ntpConfig
        if configuration == None:
            cis_2_1_passed = False
    def __str__(self):
        return str(self.cis_2_1_passed)


