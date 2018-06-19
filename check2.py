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
    except vim.fault.InvalidLogin:
        raise SystemExit("Unable to connect to host "
                         "with supplied credentials.")

    content = si.RetrieveContent()
    #    print(vim.ServiceInstance.RetrieveContent(si))

    ###############################
    # Get inf about current user session
    # privilege: readOnly
    ###############################
    print("##########################################")
    print("Get info about current user session")
    print("##########################################")
    session = content.sessionManager.currentSession
    print(session)

    ###############################
    # Get info about VMs
    ###############################


if __name__ == "__main__":
    main()
