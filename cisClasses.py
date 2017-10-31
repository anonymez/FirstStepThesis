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

class cis_2_2:
    def __init__(self, host, firewallList = list):
        self.cis_2_2_passed = False
        configuration = host.QueryHostConnectionInfo().host.host.configManager.firewallSystem.firewallInfo.ruleset
        if len(configuration) != len(firewallList):
            self.cis_2_2_passed = False
        counter = 1
        benchmark = 0#
        #for c in configuration:
        #    print(c.rule)
        #    print(len(configuration))
        ruleSetArray = len(configuration)
        ruleSet = 0
        while(ruleSet < ruleSetArray - 1):
#            print(configuration[ruleSet].rule[0])
#            print(firewallList[ruleSet].rule)
            if (configuration[ruleSet].rule[0].port == firewallList[benchmark].rule[0].port
                and configuration[ruleSet].rule[0].direction == firewallList[benchmark].rule[0].direction
                and configuration[ruleSet].rule[0].protocol == firewallList[benchmark].rule[0].protocol):
                counter = counter + 1
                benchmark = benchmark + 1
                ruleSet = -1
            ruleSet = ruleSet + 1
        if counter == ruleSetArray:
            self.cis_2_2_passed = True


    def __str__(self):
        return str(self.cis_2_2_passed)

class cis_2_3:
    def __init__(self, host, snmpList = None):
        self.cis_2_3_passed = False
        configuration = host.QueryHostConnectionInfo().host.host.configManager.dateTimeSystem.dateTimeInfo.ntpConfig
        if configuration == None:
            cis_2_3_passed = False
    def __str__(self):
        return str(self.cis_2_3_passed)