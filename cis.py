import atexit

import sys
from pyVim.connect import SmartConnectNoSSL, Disconnect
import pyVmomi
from pyVmomi import vim
import inspect
import cisClasses



from tools import cli

import argparse
import getpass
import ssl

from pyVim import connect

def setup_args():

    """
    Get standard connection arguments
    """
    parser = cli.build_arg_parser()
    my_args = parser.parse_args()

    return cli.prompt_for_password(my_args)

def main():
    """
    Simple command-line program for listing the virtual machines on a host.
    """


    args = setup_args()
    si = None
    try:
        si = connect.ConnectNoSSL(host=args.host,
                               user=args.user,
                               pwd=args.password,
                               port=int(args.port))
        atexit.register(Disconnect, si)
        print("No SSL Connection: warning!!")
    except vim.fault.InvalidLogin:
        raise SystemExit("Unable to connect to host "
                         "with supplied credentials.")

    content = si.RetrieveContent()

    hostView = content.viewManager.CreateContainerView(content.rootFolder , [vim.VirtualMachine] ,True)
    viewHost = content.viewManager.viewList
    obj = [host for host in hostView.view]
    for host in obj:
        hostAnalisys = host.config.extraConfig
        cis = {
            'cis_8_4_5' : 0 , 'cis_8_4_6' : 0 , 'cis_8_4_7' : 0 , 'cis_8_4_8' : 0 , 'cis_8_4_9' : 0 , 'cis_8_4_10' : 0 ,
            'cis_8_4_11' : 0 , 'cis_8_4_12' : 0 , 'cis_8_4_13' : 0 , 'cis_8_4_14' : 0 , 'cis_8_4_15' : 0 ,
            'cis_8_4_16' : 0 , 'cis_8_4_17' : 0 , 'cis_8_4_18' : 0 , 'cis_8_4_19' : 0 , 'cis_8_4_20' : 0 ,
            'cis_8_4_21' : 0 , 'cis_8_4_22' : 0 , 'cis_8_4_23' : 0 , 'cis_8_4_24' : 0 , 'cis_8_4_25': 0 ,
            'cis_8_4_26' : 0 , 'cis_8_4_27' : 0 , 'cis_8_4_28' : 0 , 'cis_8_4_29' : 0 , 'cis_8_6_2': 0 ,
            'cis_8_6_3': 0 , 'cis_8_7_1': 0 , 'cis_8_7_3': 0
        }
        for config in hostAnalisys:
            if config.key == "isolation.tools.ghi.autologon.disable":
                print(cisClasses.cis_8_4_x('cis 8.4.5', config, True))
                cis['cis_8_4_5'] = 1
            if config.key == "isolation.bios.bbs.disable":
                print(cisClasses.cis_8_4_x('cis 8.4.6' , config , True))
                cis['cis_8_4_6'] = 1
            if config.key == "isolation.tools.ghi.protocolhandler.info.disable":
                print(cisClasses.cis_8_4_x('cis 8.4.7' , config , True))
                cis['cis_8_4_7'] = 1
            if config.key == "isolation.tools.unity.taskbar.disable":
                print(cisClasses.cis_8_4_x('cis 8.4.8' , config , True))
                cis['cis_8_4_8'] = 1
            if config.key == "isolation.tools.unityActive.disable":
                print(cisClasses.cis_8_4_x('cis 8.4.9' , config , True))
                cis['cis_8_4_9'] = 1
            if config.key == "isolation.tools.unity.windowContents.disable":
                print(cisClasses.cis_8_4_x('cis 8.4.10' , config , True))
                cis['cis_8_4_10'] = 1
            if config.key == "isolation.tools.unity.push.update.disable":
                print(cisClasses.cis_8_4_x('cis 8.4.11' , config , True))
                cis['cis_8_4_11'] = 1
            if config.key == "isolation.tools.vmxDnDVersionGet.disable":
                print(cisClasses.cis_8_4_x('cis 8.4.12' , config , True))
                cis['cis_8_4_12'] = 1
            if config.key == "isolation.tools.guestDnDVersionSet.disable":
                print(cisClasses.cis_8_4_x('cis 8.4.13' , config , True))
                cis['cis_8_4_13'] = 1
            if config.key == "isolation.ghi.host.shellAction.disable":
                print(cisClasses.cis_8_4_x('cis 8.4.14' , config , True))
                cis['cis_8_4_14'] = 1
            if config.key == "isolation.tools.dispTopoRequest.disable":
                print(cisClasses.cis_8_4_x('cis 8.4.15' , config , True))
                cis['cis_8_4_15'] = 1
            if config.key == "isolation.tools.trashFolderState.disable":
                print(cisClasses.cis_8_4_x('cis 8.4.16' , config , True))
                cis['cis_8_4_16'] = 1
            if config.key == "isolation.tools.ghi.trayicon.disable":
                print(cisClasses.cis_8_4_x('cis 8.4.17' , config , True))
                cis['cis_8_4_17'] = 1
            if config.key == "isolation.tools.unity.disable":
                print(cisClasses.cis_8_4_x('cis 8.4.18' , config , True))
                cis['cis_8_4_18'] = 1
            if config.key == "isolation.tools.unityInterlockOperation.disable":
                print(cisClasses.cis_8_4_x('cis 8.4.19' , config , True))
                cis['cis_8_4_19'] = 1
            if config.key == "isolation.tools.getCreds.disable":
                print(cisClasses.cis_8_4_x('cis 8.4.20' , config , True))
                cis['cis_8_4_20'] = 1
            if config.key == "isolation.tools.hgfsServerSet.disable":
                print(cisClasses.cis_8_4_x('cis 8.4.21' , config , True))
                cis['cis_8_4_21'] = 1
            if config.key == "isolation.tools.ghi.launchmenu.change":
                print(cisClasses.cis_8_4_x('cis 8.4.22' , config , True))
                cis['cis_8_4_22'] = 1
            if config.key == "isolation.tools.memSchedFakeSampleStats.disable":
                print(cisClasses.cis_8_4_x('cis 8.4.23' , config , True))
                cis['cis_8_4_23'] = 1
            if config.key == "isolation.tools.copy.disable":
                print(cisClasses.cis_8_4_x('cis 8.4.24' , config , True))
                cis['cis_8_4_24'] = 1
            if config.key == "isolation.tools.dnd.disable":
                print(cisClasses.cis_8_4_x('cis 8.4.25' , config , True))
                cis['cis_8_4_25'] = 1
            if config.key == "isolation.tools.setGUIOptions.enable":
                print(cisClasses.cis_8_4_x('cis 8.4.26' , config , False))
                cis['cis_8_4_26'] = 1
            if config.key == "isolation.tools.paste.disable":
                print(cisClasses.cis_8_4_x('cis 8.4.27' , config , True))
                cis['cis_8_4_27'] = 1
            if config.key == "RemoteDisplay.vnc.enabled":
                print(cisClasses.cis_8_4_x('cis 8.4.28' , config , False))
                cis['cis_8_4_28'] = 1
            if config.key == "svga.vgaOnly":
                print(cisClasses.cis_8_4_x('cis 8.4.29' , config , True))
                cis['cis_8_4_29'] = 1
            if config.key == "isolation.tools.diskShrink.disable":
                print(cisClasses.cis_8_4_x('cis 8.6.2' , config , True))
                cis['cis_8_6_2'] = 1
            if config.key == "isolation.tools.diskWiper.disable":
                print(cisClasses.cis_8_4_x('cis 8.6.3' , config , True))
                cis['cis_8_6_3'] = 1
            if config.key == "isolation.tools.vixMessage.disable":
                print(cisClasses.cis_8_4_x('cis 8.7.1' , config , True))
                cis['cis_8_7_1'] = 1
            if config.key == "tools.guestlib.enableHostInfo":
                print(cisClasses.cis_8_4_x('cis 8.7.3' , config , False))
                cis['cis_8_7_3'] = 1
        for key in cis:
            if(cis[key] == 0):
                print(cisClasses.notFound(key))


if __name__ == "__main__":
    main()