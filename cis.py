from pyVmomi import vim
import cisClasses

def controls_vm(si):

    content = si.RetrieveContent()

    hostView = content.viewManager.CreateContainerView(content.rootFolder , [vim.HostSystem] , True)
    obj = [host for host in hostView.view]

    cis = {
        'cis_8_2_1' : [0] , 'cis_8_2_2' : [0] , 'cis_8_2_3' : [0], 'cis_8_2_4'  : [0],
        'cis_8_2_5' : [0] , 'cis_8_2_6' : [0] , 'cis_8_2_7' : [0] , 'cis_8_4_5' : [0] ,
        'cis_8_4_6' : [0] , 'cis_8_4_7' : [0] , 'cis_8_4_8' : [0] , 'cis_8_4_9' : [0] ,
        'cis_8_4_10' : [0] , 'cis_8_4_11' : [0] , 'cis_8_4_12' : [0] , 'cis_8_4_13' : [0] ,
        'cis_8_4_14' : [0] , 'cis_8_4_15' : [0] , 'cis_8_4_16' : [0] , 'cis_8_4_17' : [0] ,
        'cis_8_4_18' : [0] , 'cis_8_4_19' : [0] , 'cis_8_4_20' : [0] , 'cis_8_4_21' : [0] ,
        'cis_8_4_22' : [0] , 'cis_8_4_23' : [0] , 'cis_8_4_24' : [0] , 'cis_8_4_25' : [0] ,
        'cis_8_4_26' : [0] , 'cis_8_4_27' : [0] , 'cis_8_4_28' : [0] , 'cis_8_4_29' : [0] ,
        'cis_8_6_2' : [0] , 'cis_8_6_3' : [0] , 'cis_8_7_1' : [0] , 'cis_8_7_3' : [0]
    }

    for host in obj:

        vmView = content.viewManager.CreateContainerView(content.rootFolder , [vim.VirtualMachine] ,True)
        viewHost = content.viewManager.viewList

        counter = 0

        vmObj = [vms for vms in vmView.view]
        for vm in vmObj:
            hostAnalisys = vm.config.extraConfig

            for config in hostAnalisys:
                server = cisClasses.cisControl()
                if config.key == "isolation.device.edit.disable":
                    print('cis 8.2.6: '),
                    control = server.cis_8_4_x(config , True)
                    print(control)
                    if control == True and counter == 0:
                        cis['cis_8_2_6'] = [1]
                    elif control == True and counter != 0:
                        cis['cis_8_2_6'].append(1)
                if config.key == "isolation.device.connectable.disable":
                    print('cis 8.2.7: '),
                    control = server.cis_8_4_x(config, True)
                    print (control)
                    if control == True and counter == 0:
                        cis['cis_8_2_7'] = [1]
                    elif control == True and counter != 0:
                        cis['cis_8_2_7'].append(1)
                if config.key == "isolation.tools.ghi.autologon.disable":
                    print('cis 8.4.5: ') ,
                    control = server.cis_8_4_x(config, True)
                    print (control)
                    if control == True and counter == 0:
                        cis['cis_8_4_5'] = [1]
                    elif control == True and counter != 0:
                        cis['cis_8_4_5'].append(1)
                if config.key == "isolation.bios.bbs.disable":
                    print('cis 8.4.6: ') ,
                    control = server.cis_8_4_x(config, True)
                    print (control)
                    if control == True and counter == 0:
                        cis['cis_8_4_6'] = [1]
                    elif control == True and counter != 0:
                        cis('cis_8_4_6').append(1)
                if config.key == "isolation.tools.ghi.protocolhandler.info.disable":
                    print('cis 8.4.7: ') ,
                    control = server.cis_8_4_x(config , True)
                    print (control)
                    if control == True and counter == 0:
                        cis['cis_8_4_7'] = [1]
                    elif control == True and counter != 0:
                        cis('cis_8_4_7').append(1)
                if config.key == "isolation.tools.unity.taskbar.disable":
                    print('cis 8.4.8: ') ,
                    control = server.cis_8_4_x(config , True)
                    print (control)
                    if control == True and counter == 0:
                        cis['cis_8_4_8'] = [1]
                    elif control == True and counter != 0:
                        cis('cis_8_4_8').append(1)
                if config.key == "isolation.tools.unityActive.disable":
                    print('cis 8.4.9: ') ,
                    control = server.cis_8_4_x(config , True)
                    print (control)
                    if control == True and counter == 0:
                        cis['cis_8_4_9'] = [1]
                    elif control == True and counter != 0:
                        cis('cis_8_4_9').append(1)
                if config.key == "isolation.tools.unity.windowContents.disable":
                    print('cis 8.4.10: ') ,
                    control = server.cis_8_4_x(config , True)
                    print (control)
                    if control == True and counter == 0:
                        cis['cis_8_4_10'] = [1]
                    elif control == True and counter != 0:
                        cis('cis_8_4_10').append(1)
                if config.key == "isolation.tools.unity.push.update.disable":
                    print('cis 8.4.11: ') ,
                    control = server.cis_8_4_x(config , True)
                    print (control)
                    if control == True and counter == 0:
                        cis['cis_8_4_11'] = [1]
                    elif control == True and counter != 0:
                        cis('cis_8_4_11').append(1)
                if config.key == "isolation.tools.vmxDnDVersionGet.disable":
                    print('cis 8.4.12: ') ,
                    control = server.cis_8_4_x(config , True)
                    print (control)
                    if control == True and counter == 0:
                        cis['cis_8_4_12'] = [1]
                    elif control == True and counter != 0:
                        cis('cis_8_4_12').append(1)
                if config.key == "isolation.tools.guestDnDVersionSet.disable":
                    print('cis 8.4.13: ') ,
                    control = server.cis_8_4_x(config , True)
                    print (control)
                    if control == True and counter == 0:
                        cis['cis_8_4_13'] = [1]
                    elif control == True and counter != 0:
                        cis('cis_8_4_13').append(1)
                if config.key == "isolation.ghi.host.shellAction.disable":
                    print('cis 8.4.14: ') ,
                    control = server.cis_8_4_x(config , True)
                    print (control)
                    if control == True and counter == 0:
                        cis['cis_8_4_14'] = [1]
                    elif control == True and counter != 0:
                        cis('cis_8_4_14').append(1)
                if config.key == "isolation.tools.dispTopoRequest.disable":
                    print('cis 8.4.15: ') ,
                    control = server.cis_8_4_x(config , True)
                    print (control)
                    if control == True and counter == 0:
                        cis['cis_8_4_15'] = [1]
                    elif control == True and counter != 0:
                        cis('cis_8_4_15').append(1)
                if config.key == "isolation.tools.trashFolderState.disable":
                    print('cis 8.4.16: ') ,
                    control = server.cis_8_4_x(config , True)
                    print (control)
                    if control == True and counter == 0:
                        cis['cis_8_4_16'] = [1]
                    elif control == True and counter != 0:
                        cis('cis_8_4_16').append(1)
                if config.key == "isolation.tools.ghi.trayicon.disable":
                    print('cis 8.4.17: ') ,
                    control = server.cis_8_4_x(config , True)
                    print (control)
                    if control == True and counter == 0:
                        cis['cis_8_4_17'] = [1]
                    elif control == True and counter != 0:
                        cis('cis_8_4_17').append(1)
                if config.key == "isolation.tools.unity.disable":
                    print('cis 8.4.18: ') ,
                    control = server.cis_8_4_x(config , True)
                    print (control)
                    if control == True and counter == 0:
                        cis['cis_8_4_18'] = [1]
                    elif control == True and counter != 0:
                        cis('cis_8_4_18').append(1)
                if config.key == "isolation.tools.unityInterlockOperation.disable":
                    print('cis 8.4.19: ') ,
                    control = server.cis_8_4_x(config , True)
                    print (control)
                    if control == True and counter == 0:
                        cis['cis_8_4_19'] = [1]
                    elif control == True and counter != 0:
                        cis('cis_8_4_19').append(1)
                if config.key == "isolation.tools.getCreds.disable":
                    print('cis 8.4.20: ') ,
                    control = server.cis_8_4_x(config , True)
                    print (control)
                    if control == True and counter == 0:
                        cis['cis_8_4_20'] = [1]
                    elif control == True and counter != 0:
                        cis('cis_8_4_20').append(1)
                if config.key == "isolation.tools.hgfsServerSet.disable":
                    print('cis 8.4.21: ') ,
                    control = server.cis_8_4_x(config , True)
                    print (control)
                    if control == True and counter == 0:
                        cis['cis_8_4_21'] = [1]
                    elif control == True and counter != 0:
                        cis('cis_8_4_21').append(1)
                if config.key == "isolation.tools.ghi.launchmenu.change":
                    print('cis 8.4.22: ') ,
                    control = server.cis_8_4_x(config , True)
                    print (control)
                    if control == True and counter == 0:
                        cis['cis_8_4_22'] = [1]
                    elif control == True and counter != 0:
                        cis('cis_8_4_22').append(1)
                if config.key == "isolation.tools.memSchedFakeSampleStats.disable":
                    print('cis 8.4.23: ') ,
                    control = server.cis_8_4_x(config , True)
                    print (control)
                    if control == True and counter == 0:
                        cis['cis_8_4_23'] = [1]
                    elif control == True and counter != 0:
                        cis('cis_8_4_23').append(1)
                if config.key == "isolation.tools.copy.disable":
                    print('cis 8.4.24: ') ,
                    control = server.cis_8_4_x(config , True)
                    print (control)
                    if control == True and counter == 0:
                        cis['cis_8_4_24'] = [1]
                    elif control == True and counter != 0:
                        cis('cis_8_4_24').append(1)
                if config.key == "isolation.tools.dnd.disable":
                    print('cis 8.4.25: ') ,
                    control = server.cis_8_4_x(config , True)
                    print (control)
                    if control == True and counter == 0:
                        cis['cis_8_4_25'] = [1]
                    elif control == True and counter != 0:
                        cis('cis_8_4_25').append(1)
                if config.key == "isolation.tools.setGUIOptions.enable":
                    print('cis 8.4.26: ') ,
                    control = server.cis_8_4_x(config , False)
                    print (control)
                    if control == True and counter == 0:
                        cis['cis_8_4_26'] = [1]
                    elif control == True and counter != 0:
                        cis('cis_8_4_26').append(1)
                if config.key == "isolation.tools.paste.disable":
                    print('cis 8.4.27: ') ,
                    control = server.cis_8_4_x(config , True)
                    print (control)
                    if control == True and counter == 0:
                        cis['cis_8_4_27'] = [1]
                    elif control == True and counter != 0:
                        cis('cis_8_4_27').append(1)
                if config.key == "RemoteDisplay.vnc.enabled":
                    print('cis 8.4.28: ') ,
                    control = server.cis_8_4_x(config , False)
                    print (control)
                    if control == True and counter == 0:
                        cis['cis_8_4_28'] = [1]
                    elif control == True and counter != 0:
                        cis('cis_8_4_28').append(1)
                if config.key == "svga.vgaOnly":
                    print('cis 8.4.29: ') ,
                    control = server.cis_8_4_x(config , True)
                    print (control)
                    if control == True and counter == 0:
                        cis['cis_8_4_29'] = [1]
                    elif control == True and counter != 0:
                        cis('cis_8_4_29').append(1)
                if config.key == "isolation.tools.diskShrink.disable":
                    print('cis 8.6.2: ') ,
                    control = server.cis_8_4_x(config , True)
                    print (control)
                    if control == True and counter == 0:
                        cis['cis_8_6_2'] = [1]
                    elif control == True and counter != 0:
                        cis('cis_8_6_2').append(1)
                if config.key == "isolation.tools.diskWiper.disable":
                    print('cis 8.6.3: ') ,
                    control = server.cis_8_4_x(config , True)
                    print (control)
                    if control == True and counter == 0:
                        cis['cis_8_6_3'] = [1]
                    elif control == True and counter != 0:
                        cis('cis_8_6_3').append(1)
                if config.key == "isolation.tools.vixMessage.disable":
                    print('cis 8.7.1: ') ,
                    control = server.cis_8_4_x(config , True)
                    print (control)
                    if control == True and counter == 0:
                        cis['cis_8_7_1'] = [1]
                    elif control == True and counter != 0:
                        cis('cis_8_7_1').append(1)
                if config.key == "tools.guestlib.enableHostInfo":
                    print('cis 8.7.3: ') ,
                    control = server.cis_8_4_x(config , False)
                    print (control)
                    if control == True and counter == 0:
                        cis['cis_8_7_3'] = [1]
                    elif control == True and counter != 0:
                        cis('cis_8_7_3').append(1)

            control = server.cis_8_2_2_to_8_2_7(vm)
            print(control[0], counter)
            if control[0] == True and counter == 0:
                cis['cis_8_2_1'] = [1]
            elif control[0] == True and counter != 0:
                cis['cis_8_2_1'].append(1)
            if control[1] == True and counter == 0:
                cis['cis_8_2_2'] = [1]
            elif control[1] == True and counter != 0:
                cis['cis_8_2_2'].append(1)
            if control[2] == True and counter == 0:
                cis['cis_8_2_3'] = [1]
            elif control[2] == True and counter != 0:
                cis['cis_8_2_3'].append(1)
            if control[3] == True and counter == 0:
                cis['cis_8_2_4'] = [1]
            elif control[3] == True and counter != 0:
                cis['cis_8_2_4'].append(1)
            if control[4] == True and counter == 0:
                cis['cis_8_2_5'] = [1]
            elif control[4] == True and counter != 0:
                cis['cis_8_2_5'].append(1)

            if counter != 0:
                for key , value in cis.items():
                    if len(value) <= (counter):
                        cis[key].append(0)
            counter = counter + 1

    cisReturn = {
        'cis_8_2_1' : 0, 'cis_8_2_2' : 0, 'cis_8_2_3' : 0, 'cis_8_2_4' : 0,
        'cis_8_2_5': 0 , 'cis_8_2_6' : 0, 'cis_8_2_7' : 0, 'cis_8_4_5' : 0,
        'cis_8_4_6' : 0, 'cis_8_4_7' : 0, 'cis_8_4_8' : 0, 'cis_8_4_9' : 0,
        'cis_8_4_10' : 0, 'cis_8_4_11' : 0, 'cis_8_4_12': 0, 'cis_8_4_13': 0,
        'cis_8_4_14': 0, 'cis_8_4_15': 0, 'cis_8_4_16': 0, 'cis_8_4_17': 0,
        'cis_8_4_18': 0, 'cis_8_4_19': 0, 'cis_8_4_20': 0, 'cis_8_4_21': 0,
        'cis_8_4_22': 0, 'cis_8_4_23': 0, 'cis_8_4_24': 0, 'cis_8_4_25': 0,
        'cis_8_4_26': 0, 'cis_8_4_27': 0, 'cis_8_4_28': 0, 'cis_8_4_29': 0,
        'cis_8_6_2': 0, 'cis_8_6_3': 0, 'cis_8_7_1': 0, 'cis_8_7_3': 0
    }
    for key, value in cis.items():
        counter = 0
        for val in value:
            if val == 1:
                counter = counter + 1
        if counter == len(value):
            cisReturn[key] = 1

    return cisReturn