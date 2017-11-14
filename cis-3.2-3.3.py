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

    hostView = content.viewManager.CreateContainerView(content.rootFolder , [vim.HostSystem] ,True)
    viewHost = content.viewManager.viewList
    obj = [host for host in hostView.view]
    for host in obj:
        hostAnalisys = host.QueryHostConnectionInfo()
        configuration = hostAnalisys.host.host.configManager

        logDir = configuration.advancedOption.setting
        cis = { 'cis_8_3_2': 0 , 'cis_8_3_3': 0 }
        for d in logDir:
#            print(d)
        #####################################################################################
        # CIS 3.2
        #####################################################################################
            if d.key == "Syslog.global.logDir":
                print('cis_3_2_passed: '),
                print(cisClasses.cis_3_2(d))
                cis['cis_8_3_2'] = 1
#                print("logDir: ", d)
        #####################################################################################
        # CIS 3.3
        #####################################################################################
            if d.key == "Syslog.global.logHost":
                print('cis_3_3_passed: '),
                print(cisClasses.cis_3_3(d))
                cis['cis_8_3_3'] = 1
#                print("logHost", d)
#        print(configuration.advancedOption.supportedOption)
        #####################################################################################
        # CIS 5.1
        #####################################################################################
        hostService = configuration.serviceSystem.serviceInfo.service
        print(hostService)
        for service in hostService:
            #####################################################################################
            # CIS 5.1
            #####################################################################################
            if service.key == "DCUI":
                print(service)
            #####################################################################################
            # CIS 5.2
            #####################################################################################
            if service.key == "TSM":
                print(service)
            #####################################################################################
            # CIS 5.3
            #####################################################################################
            if service.key == "TSM-SSH":
                print(service)
            #####################################################################################
            # CIS 5.4
            #####################################################################################
            if service.key == "sfcbd-watchdog":
                print(service)

        #####################################################################################
        # CIS 5.5 - not valid: should be ignored; supported only in Virtual Center
        #####################################################################################
        print(host.config.lockdownMode)

        option = host.config.option
        for o in option:
            #####################################################################################
            # CIS 5.7
            #####################################################################################
            if o.key == "UserVars.ESXiShellInteractiveTimeOut":
                print(o)
            #####################################################################################
            # CIS 5.8
            #####################################################################################
            if o.key == "UserVars.ESXiShellTimeOut":
                print(o)
            #####################################################################################
            # CIS 5.9
            #####################################################################################
            if o.key == "DCUI.Access":
                print(o)
#        print(host.config)
    for key in cis:
        if (cis[key] == 0):
            print(cisClasses.notFound(key))

#        print(configuration.serviceSystem.serviceInfo)

if __name__ == "__main__":
    main()