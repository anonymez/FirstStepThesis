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

    ###############################
    #Get info about the system host
    #privilege: read-only
    ###############################
    print("##########################################")
    print("Get info about the system host")
    print("##########################################")
    hyp = content.about
    print(hyp)

    dataStore = content.rootFolder.childEntity
    for data in dataStore:
        print(data)
        vm = data.hostFolder.childEntity
        for host in vm:
            hostConfig = host.host
            for tool in hostConfig:
                #####################################################################################
                # CIS 4.1
                #####################################################################################
                print(tool.configManager.authenticationManager.info)
                print(tool.configManager.serviceSystem.serviceInfo)

                print(tool.configManager.powerSystem.capability)
                print(tool.configManager.powerSystem.info)

                print(tool.configManager)







if __name__ == "__main__":
    main()