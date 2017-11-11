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

    hostView = content.viewManager.CreateContainerView(content.rootFolder, [vim.HostSystem], True)
    obj = [host for host in hostView.view]
    hostView.Destroy()

    for host in obj:
        pgs = host.config.network.portgroup

        for s in pgs:
            switch = s.vswitch
            #####################################################################################
            #CIS 7.1
            #####################################################################################
            print('Forged Transmit Policy [cis 7.1]: '),
            print(cisClasses.cis_7_1(s))
            #####################################################################################
            #CIS 7.2
            #####################################################################################
            print('MAC Address Change Policy [cis 7.2]: ') ,
            print(cisClasses.cis_7_2(s))
            #####################################################################################
            #CIS 7.3
            #####################################################################################
            print('Promiscuous Mode Policy [cis 7.3]: ') ,
            print(cisClasses.cis_7_3(s))

            policy = s.computedPolicy
            security = policy.security
            nicTeaming = policy.nicTeaming
#            print(s.computedPolicy)
#            print("activeNic: "),
#            activeNic = nicTeaming.nicOrder.activeNic
#            for active in activeNic:
#                print(active .format(nicTeaming.nicOrder.activeNic)),
#            print("")
#            print("Policy: {}" .format(nicTeaming.policy))
#            print("Forged transmit: {}" .format(security.forgedTransmits))
#            print("MAC address change: {}" .format(security.macChanges))
#            print("Promiscuous mode: {}" .format(security.allowPromiscuous))
 #           key = s.key
 #           port = [p.mac for p in s.port]
            #####################################################################################
            #CIS 7.4
            #####################################################################################
            print("Native Vlan [cis 7.4]: ") ,
            print(cisClasses.cis_7_4(s))
            #####################################################################################
            #CIS 7.5 (partial: document needed)
            #####################################################################################
            #####################################################################################
            #CIS 7.6 (partial: VGT needed)
            #####################################################################################
            print("Vlan 4095 [cis 7.6 not scored]: "),
            print(cisClasses.cis_7_6(s))
#            if(s.spec.vlanId == 4095):
#                print("##################")
#                print("VGT mode - warning")
#                print("##################")
#            print("KEY: {} ->".format(key))
#            print("SWITCH: {} ->".format(switch))
#            print("MAC: {}".format(port))







if __name__ == "__main__":
    main()