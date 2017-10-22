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
#    print(vim.ServiceInstance.RetrieveContent(si))

    ###########################################
    #Get CSC 1.1 information: search VMs
    # by network(s), for each foun
    #get informations.
    # Note: unable to find network informmation
    #on the vm, like ip address
    ###########################################
    dataStore = content.rootFolder.childEntity
    for data in dataStore:
        vmDatastore = data.datastore
        for d in vmDatastore:
            print(d.name)
            browser = d.browser.datastore
            for h in browser:
                print(h.vm)
                for v in h.vm:
                    print(v.name + "/" + v.name + ".vmx")
                    info = v.environmentBrowser.datastoreBrowser
                    infoSearch = info.Search(datastorePath = "[datastore1]" + v.name)
                    infoFile = infoSearch.info
#                    infoSearch.SetTaskState(state = "running")
#                    infoSearch.SetTaskState(state = "success")
                    #####################################################################################
                    # CIS 8.1.1
                    #####################################################################################
                    print("Entity: ", infoFile.entityName)
                    print("State: ", infoFile.state)
                    infoFileResult = infoFile.result
#                    print(infoFileResult)
                    for vmxFile in infoFileResult.file:
                        vmxFileInfo = vmxFile
#                        print(vmxFileInfo)
                        if(vmxFile.path == v.name + ".vmx"):
                            print(vmxFile)

                    #####################################################################################
                    # CIS 8.1.2
                    #####################################################################################
                    maxConnections = v.config.maxMksConnections
                    print(v.name + " Max connections: ", maxConnections)
 #                   print(content.taskManager)
            dVm = d.browser.Search(datastorePath = "[datastore1] Ubuntu3/Ubuntu3.vmxpcs")
#            print(dVm.info)#


if __name__ == "__main__":
    main()