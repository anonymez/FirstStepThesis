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

    dataStore = content.rootFolder.childEntity
    for data in dataStore:
        vmFolder = data.hostFolder.childEntity
        for dataVm in vmFolder:
            host = dataVm.host
            for h in host:
                storage = h.config.storageDevice.hostBusAdapter
                chap = storage[3]
                #####################################################################################
                # CIS 6.1
                #####################################################################################
                print('Bidirectional Chap Auth [cis 6.1]: '),
                print(cisClasses.cis_6_1(h))
#                print(chap.authenticationProperties)
#                print(chap)


if __name__ == "__main__":
    main()