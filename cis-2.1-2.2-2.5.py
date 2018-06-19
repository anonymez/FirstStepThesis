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
        #####################################################################################
        # CIS 2.1 - need to select a  server to let it appears in the list
        #####################################################################################
        configuration = hostAnalisys.host.host.configManager
        # print(configuration.dateTimeSystem.dateTimeInfo)
        print('cis 2.1 passed: '),
        print(cisClasses.cis_2_1(host))
        #####################################################################################
        # CIS 2.2
        #####################################################################################
        #        print(hostAnalisys.host.host.configManager.firewallSystem.firewallInfo.ruleset)
        print('cis_2_2_passed: '),
        print(cisClasses.cis_2_2(host, hostAnalisys.host.host.configManager.firewallSystem.firewallInfo.ruleset))

        #####################################################################################
        # CIS 2.5
        #####################################################################################
        #        conf = configuration.snmpSystem.configuration
        #        conf.enabled = False
        #        used = configuration.snmpSystem.ReconfigureSnmpAgent(conf)
        #        print(configuration.snmpSystem.configuration)
        #        print(configuration.snmpSystem.limits)
        print('cis_2_3_passed: '),
        print(cisClasses.cis_2_3(host))


if __name__ == "__main__":
    main()
