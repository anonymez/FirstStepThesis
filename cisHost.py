from pyVmomi import vim
import cisClasses
import cis


def hostControls(si):
    content = si.RetrieveContent()

    hostView = content.viewManager.CreateContainerView(content.rootFolder, [vim.HostSystem], True)
    obj = [host for host in hostView.view]
    cis_2_1 = []
    cis_2_2 = []
    cis_2_5 = []
    #    cis_2_6 = []
    cis_3_2 = []
    cis_3_3 = []
    cis_4_2 = []
    cis_4_2_value = []
    cis_4_3 = []
    cis_5_1 = []
    cis_5_2 = []
    cis_5_3 = []
    cis_5_4 = []
    cis_5_5 = []
    cis_5_7 = []
    cis_5_7_value = []
    cis_5_8 = []
    cis_5_8_value = []
    cis_5_9 = []
    cis_6_1 = []
    cis_7_1 = []
    cis_7_2 = []
    cis_7_3 = []
    cis_7_4 = []
    cis_7_5 = []
    cis_7_6 = []

    for host in obj:
        hostAnalisys = host.QueryHostConnectionInfo()
        print('processing..')
        #####################################################################################
        # CIS 2.1 - need to select a  server to let it appears in the list
        #####################################################################################
        configuration = hostAnalisys.host.host.configManager
        print('cis 2.1 passed: '),
        server = cisClasses
        control = server.cis_2_1(host)
        print(control)
        cis_2_1.append(control)
        #####################################################################################
        # CIS 2.2
        #####################################################################################
        print('cis_2_2_passed: '),
        control = server.cis_2_2(host, configuration.firewallSystem.firewallInfo.ruleset)
        print(control)
        cis_2_2.append(control)
        #####################################################################################
        # CIS 2.5
        #####################################################################################
        print('cis_2_5_passed: '),
        control = server.cis_2_5(host)
        print(control)
        cis_2_5.append(control)

        optionList = configuration.advancedOption.setting
        for option in optionList:
            #####################################################################################
            # CIS 2.6
            #####################################################################################
            #            if option.key == "Net.DVFilterBindIpAddress":
            #                print('cis_2_6_passed: ') ,
            #                control = server.cis_2_6(option)
            #                print(control)

            #####################################################################################
            # CIS 3.2
            #####################################################################################
            if option.key == "Syslog.global.logDir":
                print('cis_3_2_passed: '),
                control = server.cis_3_2(option)
                print(control)
                cis_3_2.append(control)
                #####################################################################################
                # CIS 3.3
                #####################################################################################
            if option.key == "Syslog.global.logHost":
                print('cis_3_3_passed: '),
                control = server.cis_3_3(option)
                print(control)
                cis_3_3.append(control)
                #####################################################################################
                # CIS 4.2
                #####################################################################################
            if option.key == "Security.PasswordQualityControl":
                print("cis_4_2_passed: "),
                control = server.cis_4_2(option)
                print(control[0]),
                print(", value: "),
                print(control[1])
                cis_4_2.append(control[0])
                cis_4_2_value = control[1]
            #####################################################################################
            # CIS 4.3
            #####################################################################################
        print('cis_4_3_passed: '),
        control = server.cis_4_3(host)
        print(control)
        cis_4_3.append(control)

        hostService = configuration.serviceSystem.serviceInfo.service
        for service in hostService:
            #####################################################################################
            # CIS 5.1
            #####################################################################################
            if service.key == "DCUI":
                print('cis_5_1_passed: '),
                control = server.cis_5_1(service)
                print(control)
                configuration.serviceSystem.UpdateServicePolicy("DCUI", "on")
                cis_5_1.append(control)
            #####################################################################################
            # CIS 5.2
            #####################################################################################
            if service.key == "TSM":
                print('cis_5_2_passed: '),
                control = server.cis_5_2(service)
                print(control)
                cis_5_2.append(control)
            #####################################################################################
            # CIS 5.3
            #####################################################################################
            if service.key == "TSM-SSH":
                print('cis_5_3_passed: '),
                control = server.cis_5_3(service)
                print(control)
                cis_5_3.append(control)
        optionValue = host.config.option
        for option in optionValue:
            #####################################################################################
            # CIS 5.7
            #####################################################################################
            if option.key == "UserVars.ESXiShellInteractiveTimeOut":
                print('cis_5_7_passed: '),
                control = server.cis_5_7(option)
                print(control)
                cis_5_7.append(control[0])
                cis_5_7_value = control[1]
            #####################################################################################
            # CIS 5.8
            #####################################################################################
            if option.key == "UserVars.ESXiShellTimeOut":
                print('cis_5_8_passed: '),
                control = server.cis_5_8(option)
                print(control)
                cis_5_8.append(control[0])
                cis_5_8_value = control[1]
            #####################################################################################
            # CIS 5.9
            #####################################################################################
        datacenter = content.rootFolder.childEntity
        for data in datacenter:
            hostFolder = data.hostFolder.childEntity
            for dataFolder in hostFolder:
                storageFolder = dataFolder.host
                for storage in storageFolder:
                    chapCheck = storage.config.storageDevice.hostBusAdapter
                    chap = chapCheck[3]
                    #####################################################################################
                    # CIS 6.1
                    #####################################################################################
                    print('cis_6_1_passed: '),
                    control = server.cis_6_1(storage)
                    print(control)
                    cis_6_1.append(control)

        pgs = host.config.network.portgroup

        for switch in pgs:
            #####################################################################################
            # CIS 7.1
            #####################################################################################
            print('cis_7_1: '),
            control = server.cis_7_1(switch)
            print(control)
            cis_7_1.append(control)
            #####################################################################################
            # CIS 7.2
            #####################################################################################
            print('cis_7_2_passed: '),
            control = server.cis_7_2(switch)
            print(control)
            cis_7_2.append(control)
            #####################################################################################
            # CIS 7.3
            #####################################################################################
            print('cis_7_3_passed: '),
            control = server.cis_7_3(switch)
            print(control)
            cis_7_3.append(control)

            #####################################################################################
            # CIS 7.4
            #####################################################################################
            print("cis_7_4: "),
            control = server.cis_7_4(switch)
            print(control)
            cis_7_4.append(control[0])
            cis_7_4_value = control[1]
            #####################################################################################
            # CIS 7.5 (partial: document needed)
            #####################################################################################
            #####################################################################################
            # CIS 7.6 (partial: VGT needed)
            #####################################################################################
            print("cis_7_6 [not scored]: "),
            control = server.cis_7_6(switch, True)
            print(control)
            cis_7_6.append(control)

    cisHostDict = {
        'cis_2_1_esit': 1, 'cis_2_2_esit': 1, 'cis_2_5_esit': 1, 'cis_3_2_esit': 1, 'cis_3_3_esit': 1,
        'cis_4_2_esit': 1, 'cis_4_3_esit': 1, 'cis_5_1_esit': 1, 'cis_5_2_esit': 1, 'cis_5_3_esit': 1,
        'cis_5_4_esit': 1, 'cis_5_5_esit': 1, 'cis_5_7_esit': 1, 'cis_5_8_esit': 1, 'cis_5_9_esit': 1,
        'cis_6_1_esit': 1, 'cis_7_1_esit': 1, 'cis_7_2_esit': 1, 'cis_7_3_esit': 1, 'cis_7_4_esit': 1,
        'cis_7_5_esit': 1
    }

    for passed in cis_2_1:
        if passed != cis_2_1[0] or 'False' in str(passed):
            cisHostDict['cis_2_1_esit'] = 0
    for passed in cis_2_2:
        if not passed:
            cisHostDict['cis_2_2_esit'] = 0
    for passed in cis_2_5:
        if not passed:
            cisHostDict['cis_2_5_esit'] = 0
    for passed in cis_3_2:
        if not passed:
            cisHostDict['cis_3_2_esit'] = 0
    for passed in cis_3_3:
        if not passed:
            cisHostDict['cis_3_3_esit'] = 0
    for passed in cis_4_2:
        if not passed:
            cisHostDict['cis_4_2_esit'] = 0
    for passed in cis_4_3:
        if not passed:
            cisHostDict['cis_4_3_esit'] = 0
    for passed in cis_5_1:
        if not passed:
            cisHostDict['cis_5_1_esit'] = 0
    for passed in cis_5_2:
        if not passed:
            cisHostDict['cis_5_2_esit'] = 0
    for passed in cis_5_3:
        if not passed:
            cisHostDict['cis_5_3_esit'] = 0
    for passed in cis_5_4:
        if not passed:
            cisHostDict['cis_5_4_esit'] = 0
    for passed in cis_5_5:
        if not passed:
            cisHostDict['cis_5_5_esit'] = 0
    for passed in cis_5_7:
        if not passed:
            cisHostDict['cis_5_7_esit'] = 0
    for passed in cis_5_8:
        if not passed:
            cisHostDict['cis_5_8_esit'] = 0
    for passed in cis_5_9:
        if not passed:
            cisHostDict['cis_5_9_esit'] = 0
    for passed in cis_6_1:
        if not passed:
            cisHostDict['cis_6_1_esit'] = 0
    for passed in cis_7_1:
        if not passed:
            cisHostDict['cis_7_1_esit'] = 0
    for passed in cis_7_2:
        if not passed:
            cisHostDict['cis_7_2_esit'] = 0
    for passed in cis_7_3:
        if not passed:
            cisHostDict['cis_7_3_esit'] = 0
    for passed in cis_7_4:
        if not passed:
            cisHostDict['cis_7_4_esit'] = 0
    for passed in cis_7_5:
        if not passed:
            cisHostDict['cis_7_5_esit'] = 0

    return cisHostDict, cis_4_2_value, cis_5_7_value, cis_5_8_value, cis_7_4_value, cis_7_6
