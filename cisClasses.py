class cisControl:
    def cis_2_1(self, host):
        cis_2_1_passed = ""
        configuration = host.QueryHostConnectionInfo().host.host.configManager.dateTimeSystem.dateTimeInfo.ntpConfig
#        print('In class: ', configuration)
        if str(configuration.server)[7] == ']':
            cis_2_1_passed = False
        else:
            for server in configuration.server:
                cis_2_1_passed = server
        return cis_2_1_passed

    def cis_2_2(self, host, firewallList = list):
        cis_2_2_passed = False
        configuration = host.QueryHostConnectionInfo().host.host.configManager.firewallSystem.firewallInfo.ruleset
        counter = 1
        benchmark = 0
        ruleSetArray = len(configuration)
        ruleSet = 0
        while(ruleSet < ruleSetArray - 1):
            if (configuration[ruleSet].rule[0].port == firewallList[benchmark].rule[0].port
                and configuration[ruleSet].rule[0].direction == firewallList[benchmark].rule[0].direction
                and configuration[ruleSet].rule[0].protocol == firewallList[benchmark].rule[0].protocol):
                counter = counter + 1
                benchmark = benchmark + 1
                ruleSet = 0
            ruleSet = ruleSet + 1
        if counter == ruleSetArray:
            cis_2_2_passed = True
        return cis_2_2_passed

#input:
#host: a host managed object
#used: boolean, wether SNMP is used or not
#maxTrap: int, the nmax number of allowed destinations for communications
#if SNMP is not used, it should be disabled;
#if SNMP is used, trap number and configuration should be correct
#configuration cannot be checked, the library does not extract this value
    def cis_2_5(self, host, used = False, maxTrap = int(0)):
        cis_2_5_passed = False
        configuration = host.QueryHostConnectionInfo().host.host.configManager.snmpSystem.configuration.enabled
        if configuration == False and used == False:
            cis_2_5_passed = True
        elif configuration == True and used == True:
            maxTrapDestinations = host.QueryHostConnectionInfo().host.host.configManager.snmpSystem.limits.maxTrapDestinations
            if maxTrapDestinations == maxTrap:
                cis_2_5_passed = True
#        print(host.QueryHostConnectionInfo().host.host.configManager.snmpSystem.configuration)
        return cis_2_5_passed

#input
#logDirKey: a vim.option.OptionValue managed object
#datastore: the name of the non-persistent datastore folder the logDir is in
#if the word is in the path, cis is not passed
    def cis_3_2(self, option, datastore = str):
        cis_3_2_passed = False
        if 'scratch' in option.value:
            cis_3_2_passed = False
        elif (datastore != '') and (datastore == option.value):
            cis_3_2_passed = False
        else:
            cis_3_2_passed = True
        return cis_3_2_passed

#input:
#logDirKey: a vim.option.OptionValue managed object
#server: the name of the logHost server
#if names are the same, cis has passed
    def cis_3_3(self , option , syslogServer = str):
        cis_3_3_passed = False
        if option.value != '':
            if option.value == syslogServer:
                cis_3_3_passed = True
        return cis_3_3_passed

#input:
#logDirKey: a vim.option.OptionValue managed object
#if parsed value parameters equal cis, then cis has passed
    def cis_4_2(self, option):
        cis_4_2_passed = False
        valueString = option.value
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
                        cis_4_2_passed = True
        return cis_4_2_passed, option.value

#input:
#host: a host
#domain: the domain of the ActiveDirectory
#if ActiveDirectory is in and parameters are correct, then cis has passed
#########################################################################
#to check: joinedDomain, trustedDomain's list, domainMembershopStatus
#to check(2): localAuthenticationInfo, if enabled need to be true
#########################################################################
    def cis_4_3(self, host, domain = ''):
        cis_4_3_passed = False
        hostAnalisys = host.QueryHostConnectionInfo()
        configuration = hostAnalisys.host.host.configManager
        activeDomain = configuration.authenticationManager.info
        for authInfo in activeDomain.authConfig:
            if ('ActiveDirectoryInfo' in authInfo.__class__.__name__ and authInfo.enabled == True):
                cis_4_3_passed = True
        return cis_4_3_passed

#cis 5.1 to 5.3
#input:
#service: the service the class is looking for
#policy values: 'automatic' -> start and stop with firewall ports,
#               'on'        -> start and stop with host
#               'off'       -> start and stop manually
    def cis_5_1(self, service):
        cis_5_1_passed = False
        if service.policy == 'off':
            cis_5_1_passed = True
        return cis_5_1_passed
    def cis_5_2(self, service):
        cis_5_2_passed = False
        print(service)
        if service.policy == 'off':
            cis_5_2_passed = True
        return cis_5_2_passed
    def cis_5_3(self, service):
        cis_5_3_passed = False
        if service.policy == 'off':
            cis_5_3_passed = True
        return cis_5_3_passed

#cis 5.7 to 5.9
#input:
#option: the option the cis is looking for
    def cis_5_7(self, option):
        cis_5_7_passed = False
        if option.value <= 300:
            cis_5_7_passed = True
        ESXiShellInteractiveTimeOut = option.value
        return cis_5_7_passed, ESXiShellInteractiveTimeOut
    def cis_5_8(self , option):
        cis_5_8_passed = False
        if option.value <= 3600:
            cis_5_8_passed = True
            ESXiShellTimeOut = option.value
        return cis_5_8_passed, ESXiShellTimeOut

#input:
#host: the host the cis is looking for
#mutualChapAuthenticationType: chapRequired   -> chap can be required by the target
#                              chapProhibited -> chap can be prohibited by the target
#                              chapProhibited -> chap not allowed (see authChap to be set false)
#                              chapPreferred  -> default auth with chap

    def cis_6_1(self , storage):
        cis_6_1_passed = False
        storageFolder = storage.config.storageDevice.hostBusAdapter
        for s in storageFolder:
            if s.__class__.__name__ == 'vim.host.InternetScsiHba':
#                print(s)
                chapCap = s.authenticationCapabilities
                chapProp = s.authenticationProperties
                if(chapCap.chapAuthSettable == True and chapCap.mutualChapSettable == True
                   and chapProp.chapAuthEnabled == True and chapProp.chapName != ''
                   and chapProp.mutualChapName != '' and chapProp.mutualChapAuthenticationType == 'chapRequired'):
                       cis_6_1_passed = True
        return cis_6_1_passed

#cis 7.1 to 7.3
#input:
#portGroup: the port the cis is looking for
    def cis_7_1(self , portGroup):
        cis_7_1_passed = False
        forgedTransmit = portGroup.computedPolicy.security
        if (forgedTransmit.forgedTransmits == False):
            cis_7_1_passed = True
        return cis_7_1_passed

    def cis_7_2(self , portGroup):
        cis_7_2_passed = False
        macAddresChange = portGroup.computedPolicy.security
        if (macAddresChange.macChanges == False):
            cis_7_2_passed = True
        return cis_7_2_passed

    def cis_7_3(self , portGroup):
        cis_7_3_passed = False
        promiscuousMode = portGroup.computedPolicy.security
        if (promiscuousMode.allowPromiscuous == False):
            cis_7_3_passed = True
        return cis_7_3_passed

    def cis_7_4(self , switch, nativeVlan = [1]):
        cis_7_4_passed = False
        vlan = switch.spec.vlanId
        if(vlan not in nativeVlan and vlan != 1 and vlan != 4095):
            cis_7_4_passed = True
        else:
            cis_7_4_passed = False
        return cis_7_4_passed, vlan

    def cis_7_6(self , switch, vgtEnabled = False):
        vlan = switch.spec.vlanId
        cis_7_6_passed = vlan
        if(vlan == 4095 and vgtEnabled == True):
            cis_7_6_passed = str(cis_7_6_passed) + (' ok only for VGT mode')
        elif(vlan == 4095 and vgtEnabled == False):
            cis_7_6_passed = False
        else:
            cis_7_6_passed = True
        return cis_7_6_passed

    def cis_8_2_2_to_8_2_7(self, virtualMachine, deviceToCheck = str, needed = False):
        cis_8_2_1_passed = False
        cis_8_2_2_passed = False
        cis_8_2_3_passed = False
        cis_8_2_4_passed = False
        cis_8_2_5_passed = False
        cis_8_2_6_passed = False
        deviceList = virtualMachine.config.hardware.device
        floppyCounter = 0
        cdCounter = 0
        parallelCounter = 0
        serialCounter = 0
        usbCounter = 0
        for device in deviceList:
            if(device.connectable != None):
                startConnected = device.connectable.startConnected
                allowGuestControl = device.connectable.allowGuestControl
                connected = device.connectable.connected
                if('Floppy' in device.__class__.__name__):
                    cdCounter = 1
                    if(startConnected == needed and allowGuestControl == needed and connected == needed):
                        cis_8_2_1_passed = True
                elif('VirtualCdrom' in device.__class__.__name__):
                    floppyCounter = 1
                    if (startConnected == needed and allowGuestControl == needed and connected == needed):
                        cis_8_2_2_passed = True
                elif('Parallel' in  device.__class__.__name__):
                    parallelCounter = 1
                    if (startConnected == needed and allowGuestControl == needed and connected == needed):
                        cis_8_2_3_passed = True
                elif('Serial' in device.__class__.__name__):
                    serialCounter = 1
                    if(startConnected == needed and allowGuestControl == needed and connected == needed):
                        cis_8_2_4_passed = True
                elif('USB' in device.__class__.__name__):
                    usbCounter = 1
                    if (startConnected == needed and allowGuestControl == needed and connected == needed):
                        cis_8_2_5_passed = True
        if(cdCounter == 0):
            cis_8_2_1_passed = True
        if(floppyCounter == 0):
            cis_8_2_2_passed = True
        if(parallelCounter == 0):
            cis_8_2_3_passed = True
        if(serialCounter == 0):
            cis_8_2_4_passed = True
        if(usbCounter == 0):
            cis_8_2_5_passed = True
        return cis_8_2_1_passed, cis_8_2_2_passed, cis_8_2_3_passed, cis_8_2_4_passed, cis_8_2_5_passed

    def cis_8_4_x(self, key, default = False):
        cis_8_4_x_passed = False
        if(str(key.value).lower() == str(default).lower()):
            cis_8_4_x_passed = True
        return cis_8_4_x_passed