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
        #####################################################################################
        # CIS 2.1 - need to select a  server to let it appears in the list
        #####################################################################################
        #configuration = hostAnalisys.host.host.configManager
        #print(configuration.dateTimeSystem.dateTimeInfo)
        print('cis 2.1 passed: '),
        print(cisClasses.cis_2_1(host))
        #####################################################################################
        # CIS 2.2
        #####################################################################################
        print(hostAnalisys.host.host.configManager.firewallSystem.firewallInfo)

        #####################################################################################
        # CIS 2.5
        #####################################################################################
        #print(configuration.snmpSystem.configuration)
        #print(configuration.snmpSystem.limits)

if __name__ == "__main__":
    main()