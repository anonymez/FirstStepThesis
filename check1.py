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

    global cpuTotNum, cpuVmNum, ramTot, ramVm
    args = setup_args()
    si = None
    try:
        si = connect.ConnectNoSSL(host=args.host,
                               user=args.user,
                               pwd=args.password,
                               port=int(args.port))
        atexit.register(Disconnect, si)
    except vim.fault.InvalidLogin:
        raise SystemExit("Unable to connect to host "
                         "with supplied credentials.")

    content = si.RetrieveContent()
#    print(vim.ServiceInstance.RetrieveContent(si))

    ###############################
    #Get info about the system host
    #privilege: read-only
    ###############################
    print("##########################################")
    print("Get info about the system host")
    print("##########################################")
    hyp = content.about
    print(hyp)

    ###############################
    #Get inf about current user session
    #privilege: readOnly
    ###############################
    print("##########################################")
    print("Get info about current user session")
    print("##########################################")
    session = content.sessionManager.currentSession
    print(session)

    ###############################
    #Get info about VMs this
    #user can access
    ###############################

    hostView = content.viewManager.CreateContainerView(content.rootFolder, [vim.HostSystem], True)
    obj = [host for host in hostView.view]
    hostView.Destroy()

    for host in obj:
        print("##########################################")
        print("Get info about VMs this user can access")
        print("##########################################")
        vMachine = host.vm
        print(vMachine)
        role = content.authorizationManager

        for v in vMachine:
            print(v.summary.config)
#            print(role.RetrieveEntityPermissions(v , True))

        print("##########################################")
        print("Get info about host's hardware")
        print("##########################################")
#        print(host.boh)
        hwMachine = host.hardware
        #print(hwMachine)



    getRole = content.rootFolder.childEntity
    for child in getRole:
        datacenter = child
        vmFolder = child.vmFolder
        vmList = vmFolder.childEntity
        keySession = content.sessionManager.currentSession
        print(keySession)
        for vm in vmList:
            print(content.authorizationManager.RetrieveEntityPermissions(vm, True))
#            getRole = role.HasPrivilegeOnEntity(vm, keySession)

    pList = role.privilegeList
    rList = role.roleList
    print("=" * 80)
    print(rList)
#    print(content.userDirectory.RetrieveUserGroups(searchStr='' , exactMatch=False , findUsers=True , findGroups=False))
    for a in vim.vm.guest.GuestOperationsManager:
        print a


if __name__ == "__main__":
    main()