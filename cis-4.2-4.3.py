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

        logDir = configuration.advancedOption.setting
        for d in logDir:
            #####################################################################################
            # CIS 4.2
            #####################################################################################
            if d.key == "Security.PasswordQualityControl":
                print("passQualityContr [cis 4.2]: "),
                print(cisClasses.cis_4_2(d))
        #                print(d)
        #####################################################################################
        # CIS 4.3
        #####################################################################################
        print('activeDomainContr [cis 4.3]: '),
        print(cisClasses.cis_4_3(host))


#        print(configuration.authenticationManager.info)


#        print(configuration.serviceSystem.serviceInfo)

if __name__ == "__main__":
    main()
