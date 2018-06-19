import atexit

from pyVim import connect
from pyVim.connect import Disconnect
from pyVmomi import vim

import cisClasses
from tools import cli


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
    # Get CSC 1.1 information: search VMs
    # by network(s), for each foun
    # get informations.
    # Note: unable to find network informmation
    # on the vm, like ip address
    ###########################################
    dataStore = content.rootFolder.childEntity
    for data in dataStore:
        vm = data.vmFolder.childEntity
        for virtual in vm:
            #            print("Hosts: ", virtual.summary)
            #####################################################################################
            # CIS 8.2.1 to 8.2.5
            #####################################################################################
            print("Name: " + virtual.config.name)
            #####################################################################################
            # CIS 8.2.6 and 8.2.7- connectable.allowGuestControl
            #####################################################################################
            #            print("Vm num: ", virtual.config.hardware)
            dictionary = cisClasses.cis_8_2_2_to_8_2_7(virtual)
            print(dictionary)


#            print(dir(virtual))
# print(virtual.config.files)


if __name__ == "__main__":
    main()
