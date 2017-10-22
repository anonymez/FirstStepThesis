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
    print(content.about)
    for data in dataStore:
        net = data.network
        for network in net:
            print(network.summary)
            print(network.vm)
            vm = network.vm
            print(network.host)
        for virtual in vm:
#            print("Hosts: ", virtual.summary)
            print("Vm num: ", virtual.summary.vm)
            print("Name: ",virtual.summary.config.name)
            print("Path: ", virtual.summary.config.vmPathName)
            print("UUID: ", virtual.summary.config.uuid)
        stores = data.datastore
        for datas in stores:
            datasNames = datas.info
            print(datasNames)
            print("name:", datasNames.name)
            print("url: ", datasNames.url)
            print("UUID: ", datasNames.vmfs.uuid)
            print("Capacity: ", datasNames.vmfs.capacity)

    hostSystem = sys.argv[2]
    print(hostSystem)

#    tryView = content.viewManager
#    vmView = tryView.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
#    vmObj = [virtMach for virtMach in vmView.view]

    hostView = content.viewManager.CreateContainerView(content.rootFolder, [vim.HostSystem], True)
    obj = [host for host in hostView.view]
    hostView.Destroy()

    hostPgDict = {}
    for host in obj:
        pgs = host.config.network.portgroup
#        for i in pgs:
#            print(i)
        print("host {} done.".format(host.name))


        for s in pgs:
            switch = s.vswitch
#            print("prova2", switch)
            #####################################################################################
            #CIS 7.1
            #CIS 7.2
            #CIS 7.3
            #####################################################################################
            print("prova2", s.computedPolicy)
            key = s.key
            port = [p.mac for p in s.port]
            #####################################################################################
            #CIS 7.4
            #CIS 7.5 (partial: document needed)
            #CIS 7.6 (partial: VGT needed)
            #####################################################################################
            print("VLANID:", s.spec.vlanId)
            print("KEY: {} ->".format(key)) ,
            print("SWITCH: {} ->".format(switch)),
            print("MAC: {}".format(port))
#            for p in port:
#                print("KEY: {} ->".format(key)),
#                print("SWITCH: {} ->".format(switch)),
#                print("MAC: {}".format(p.mac))

        newSwitch = host.config.network.vnic

        dns = host.config.network.dnsConfig
        print("################")
        print("DNS")
        print("################")
        print("HostName {} ->".format(dns.hostName)),
        print("DomainName {} ->".format(dns.domainName)),
        print("DHCP {} ->".format(dns.dhcp)),
        print("DNS IP {} ->".format(dns.address)),
        print("vNIC {}".format(dns.virtualNicDevice))

#        fw = host.config.storageDevice
#        print(fw)






if __name__ == "__main__":
    main()