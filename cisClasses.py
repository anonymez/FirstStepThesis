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

#input:
#host: a host managed object
#used: boolean, wether SNMP is used or not
#maxTrap: int, the nmax number of allowed destinations for communications
#if SNMP is not used, it should be disabled;
#if SNMP is used, trap number and configuration should be correct
#configuration cannot be checked, the library does not extract this value
class cis_2_3:
    def __init__(self, host, used = False, maxTrap = int):
        self.cis_2_3_passed = False
        configuration = host.QueryHostConnectionInfo().host.host.configManager.snmpSystem.configuration.enabled
        if configuration == False and used == False:
            self.cis_2_3_passed = True
        elif configuration == True and used == True:
            maxTrapDestinations = host.QueryHostConnectionInfo().host.host.configManager.snmpSystem.limits.maxTrapDestinations
            if maxTrapDestinations == maxTrap:
                self.cis_2_3_passed = True
    def __str__(self):
        return str(self.cis_2_3_passed)

#input
#logDirKey: a vim.option.OptionValue managed object
#datastore: the name of the non-persistent datastore folder the logDir is in
#if the word is in the path, cis is not passed
class cis_3_2:
    def __init__(self, logDirKey, datastore = str):
        self.cis_3_2_passed = False
        if 'scratch' in logDirKey.value:
            self.cis_3_2_passed = False
        else:
            self.cis_3_2_passed = True
    def __str__(self):
        return str(self.cis_3_2_passed)

#input:
#logDirKey: a vim.option.OptionValue managed object
#server: the name of the logHost server
#if names are the same, cis has passed
class cis_3_3:
    def __init__(self , logDirKey , syslogServer = str):
        self.cis_3_3_passed = False
        if logDirKey.value == syslogServer:
            self.cis_3_3_passed = True
    def __str__(self):
        return str(self.cis_3_3_passed)

#input:
#logDirKey: a vim.option.OptionValue managed object
#if parsed value parameters equal cis, then cis has passed
class cis_4_2:
    def __init__(self, logDirKey):
        self.cis_4_2_passed = False
        valueString = logDirKey.value
        if 'retry=' in valueString:
            retryIndex = valueString.index('retry=')
            retryIndexLength = len('retry=')
            retryTimesPosition = retryIndex + retryIndexLength
            if int(valueString[retryTimesPosition]) < 5:
                if 'min=' in valueString:
                    minIndex = valueString.index('min=')
                    minIndexLength = len('min=')
                    minPosition = minIndex + minIndexLength
                    minN0Value = ''
                    minN1Value = ''
                    minN2Value = ''
                    minN3Value = ''
                    minN4Value = ''
                    commaCounter = 0
                    while (minPosition < len(valueString)):
                        if(valueString[minPosition] == ','):
                            commaCounter = commaCounter + 1
                            minPosition = minPosition + 1
                        if(commaCounter < 1):
                            minN0Value = minN0Value + valueString[minPosition]
                        elif(commaCounter < 2):
                            minN1Value = minN1Value + valueString[minPosition]
                        elif(commaCounter < 3):
                            minN2Value = minN2Value + valueString[minPosition]
                        elif(commaCounter < 4):
                            minN3Value = minN3Value + valueString[minPosition]
                        else:
                            minN4Value = minN4Value + valueString[minPosition]
                        minPosition = minPosition + 1

                    if minN0Value == 'disabled' and minN1Value == 'disabled' and minN2Value == 'disabled'\
                            and minN3Value == 'disabled' and minN4Value != 'disabled' and int(minN4Value) >= 14:
                        self.cis_4_2_passed = True
    def __str__(self):
        return str(self.cis_4_2_passed)

#input:
#host: a host
#domain: the domain of the ActiveDirectory
#if ActiveDirectory is in and parameters are correct, then cis has passed
#########################################################################
#to check: joinedDomain, trustedDomain's list, domainMembershopStatus
#to check(2): localAuthenticationInfo, if enable need to be true
#########################################################################
class cis_4_3:
    def __init__(self, host, domain = ''):
        self.cis_4_3_passed = False
        hostAnalisys = host.QueryHostConnectionInfo()
        configuration = hostAnalisys.host.host.configManager
        activeDomain = configuration.authenticationManager.info
        for authInfo in activeDomain.authConfig:
            if ('AxctiveDirectoryInfo' in authInfo.__class__.__name__ and authInfo.enabled == True):
                self.cis_4_3_passed = True

    def __str__(self):
            return str(self.cis_4_3_passed)

#cis 5.1 to 5.3
#input:
#service: the service the class is looking for
#policy values: 'automatic' -> start and stop with firewall ports,
#               'on'        -> start and stop with host
#               'off'       -> start and stop manually
class cis_5_1:
    def __init__(self, service):
        self.cis_5_1_passed = False
        if service.policy == 'off':
            self.cis_5_1_passed = True
    def __str__(self):
        return str(self.cis_5_1_passed)
class cis_5_2:
    def __init__(self, service):
        self.cis_5_2_passed = False
        if service.policy == 'off':
            self.cis_5_2_passed = True
    def __str__(self):
        return str(self.cis_5_2_passed)
class cis_5_3:
    def __init__(self, service):
        self.cis_5_3_passed = False
        if service.policy == 'off':
            self.cis_5_3_passed = True
    def __str__(self):
        return str(self.cis_5_3_passed)

#cis 5.7 to 5.9
#input:
#option: the option the cis is looking for
class cis_5_7:
    def __init__(self, option):
        self.cis_5_7_passed = False
        if option.value <= 300:
            self.cis_5_7_passed = True
    def __str__(self):
        return str(self.cis_5_7_passed)
class cis_5_8:
    def __init__(self , option):
        self.cis_5_8_passed = False
        if option.value <= 3600:
            self.cis_5_8_passed = True
    def __str__(self):
        return str(self.cis_5_8_passed)
class cis_5_9:
    def __init__(self , option):
        self.cis_5_9_passed = option.value
    def __str__(self):
        return str(self.cis_5_9_passed)

#input:
#host: the host the cis is looking for
#mutualChapAuthenticationType: chapRequired   -> chap can be required by the target
#                              chapProhibited -> chap can be prohibited by the target
#                              chapProhibited -> chap not allowed (see authChap to be set false)
#                              chapPreferred  -> default auth with chap
###############################################################################################
#chapPreferred to be checked in mutualChapAuth
###############################################################################################

class cis_6_1:
    def __init__(self , host):
        self.cis_6_1_passed = False
        storage = host.config.storageDevice.hostBusAdapter
        for s in storage:
            if s.__class__.__name__ == 'vim.host.InternetScsiHba':
#                print(s)
                chapCap = s.authenticationCapabilities
                chapProp = s.authenticationProperties
                if(chapCap.chapAuthSettable == True and chapCap.mutualChapSettable == True
                   and chapProp.chapAuthEnabled == True and chapProp.chapName != ''
                   and chapProp.mutualChapName != ''):
                       self.cis_6_1_passed = True
    def __str__(self):
        return str(self.cis_6_1_passed)

#cis 7.1 to 7.3
#input:
#portGroup: the port the cis is looking for
class cis_7_1:
    def __init__(self , portGroup):
        self.cis_7_1_passed = False
        forgedTransmit = portGroup.computedPolicy.security
        if (forgedTransmit.forgedTransmits == False):
            self.cis_7_1_passed = True
    def __str__(self):
        return str(self.cis_7_1_passed)

class cis_7_2:
    def __init__(self , portGroup):
        self.cis_7_2_passed = False
        macAddresChange = portGroup.computedPolicy.security
        if (macAddresChange.macChanges == False):
            self.cis_7_2_passed = True
    def __str__(self):
        return str(self.cis_7_2_passed)

class cis_7_3:
    def __init__(self , portGroup):
        self.cis_7_3_passed = False
        promiscuousMode = portGroup.computedPolicy.security
        if (promiscuousMode.allowPromiscuous == False):
            self.cis_7_3_passed = True
    def __str__(self):
        return str(self.cis_7_3_passed)

class cis_7_4:
    def __init__(self , portGroup, nativeVlan = 1):
        self.cis_7_4_passed = False
        vlan = portGroup.spec.vlanId
        if(vlan != nativeVlan):
            self.cis_7_4_passed = True
    def __str__(self):
        return str(self.cis_7_4_passed)
class cis_7_6:
    def __init__(self , portGroup):
        vlan = portGroup.spec.vlanId
        self.cis_7_6_passed = str(vlan)
        if(vlan == 4095):
            self.cis_7_6_passed = self.cis_7_6_passed + (' ok only for VGT mode')
    def __str__(self):
        return str(self.cis_7_6_passed)

class cis_8_2_2_to_8_2_7:
    def __init__(self, virtualMachine, needed = False):
        self.cis_8_2_2_passed = False
        self.cis_8_2_3_passed = False
        deviceList = virtualMachine.config.hardware.device
        floppyCounter = 0
        cdCounter = 0
        for device in deviceList:
            if(device.connectable != None):
                startConnected = device.connectable.startConnected
                allowGuestControl = device.connectable.allowGuestControl
                connected = device.connectable.connected
            if('VirtualCdrom' in device.__class__.__name__):
                cdCounter = 1
                if(startConnected == False and allowGuestControl == False and connected == False):
                    self.cis_8_2_2_passed = True
            elif('Floppy' in device.__class__.__name__):
                floppyCounter = 1
                if (startConnected == False and allowGuestControl == False and connected == False):
                    self.cis_8_2_3_passed = True
        if(cdCounter == 0):
            self.cis_8_2_2_passed = True
        if(floppyCounter == 0):
            self.cis_8_2_3_passed = True

    def __repr__(self):
        return repr(['cis 8.2.2: ' + str(self.cis_8_2_2_passed), 'cis 8.2.1: ' + str(self.cis_8_2_3_passed)])