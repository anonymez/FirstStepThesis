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

    hostView = content.viewManager.CreateContainerView(content.rootFolder, [vim.HostSystem], True)
    viewHost = content.viewManager.viewList
    obj = [host for host in hostView.view]
    for host in obj:
        hostAnalisys = host.QueryHostConnectionInfo()
        configuration = hostAnalisys.host.host.configManager
        #####################################################################################
        # CIS 5.1
        #####################################################################################
        hostService = configuration.serviceSystem.serviceInfo.service
        #        print(hostService)
        for service in hostService:
            #####################################################################################
            # CIS 5.1
            #####################################################################################
            if service.key == "DCUI":
                print('service DCUI [cis 5.1]: '),
                print(cisClasses.cis_5_1(service))
            #####################################################################################
            # CIS 5.2
            #####################################################################################
            if service.key == "TSM":
                print('service TSM [cis 5.2]: '),
                print(cisClasses.cis_5_2(service))
            #####################################################################################
            # CIS 5.3
            #####################################################################################
            if service.key == "TSM-SSH":
                print('service TSM-SSH [cis 5.3]: '),
                print(cisClasses.cis_5_3(service))

        #####################################################################################
        # CIS 5.5 - not valid: should be ignored; supported only in Virtual Center
        #####################################################################################
        #        print(host.config)

        option = host.config.option
        for o in option:
            #####################################################################################
            # CIS 5.7
            #####################################################################################
            if o.key == "UserVars.ESXiShellInteractiveTimeOut":
                print('option ESXiShellInteractiveTimeOut [cis 5.7]: '),
                print(cisClasses.cis_5_7(o))
            #####################################################################################
            # CIS 5.8
            #####################################################################################
            if o.key == "UserVars.ESXiShellTimeOut":
                print('option ESXiShellTimeOut [cis 5.8]: '),
                print(cisClasses.cis_5_8(o))
            #####################################################################################
            # CIS 5.9
            #####################################################################################
            if o.key == "DCUI.Access":
                print('option DCUI.Acces [cis 5.9 not scored]: '),
                print(cisClasses.cis_5_9(o))


#        print(configuration.serviceSystem.serviceInfo)

if __name__ == "__main__":
    main()
