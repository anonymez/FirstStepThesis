import atexit

from pyVim import connect
from pyVim.connect import Disconnect
from pyVmomi import vim

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
            # CIS 8.6.1 - look for backing-diskMode
            #####################################################################################
            device = virtual.config.hardware.device
            #            print(device)
            for devices in device:
                if ("Hard disk" in devices.deviceInfo.label):
                    print(devices)


#            print(dir(virtual))
# print(virtual.config.files)


if __name__ == "__main__":
    main()
