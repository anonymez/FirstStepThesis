import atexit

import sys
from pyVim.connect import SmartConnectNoSSL, Disconnect
import pyVmomi
from pyVmomi import vim
import inspect



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
        for d in logDir:
        #####################################################################################
        # CIS 4.2
        #####################################################################################
            if d.key == "Security.PasswordQualityControl":
                print(d)
        #####################################################################################
        # CIS 4.3
        #####################################################################################
        print(configuration.authenticationManager.info)


#        print(configuration.serviceSystem.serviceInfo)

if __name__ == "__main__":
    main()