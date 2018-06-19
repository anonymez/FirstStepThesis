import atexit
import ssl

from pyVim import connect
from pyVim.connect import SmartConnectNoSSL, Disconnect
from pyVmomi import vim

from tools import cli

MAX_DEPTH = 10
v_machine = {}


def setup_args():
    """
    Get standard connection arguments
    """
    parser = cli.build_arg_parser()
    my_args = parser.parse_args()

    return cli.prompt_for_password(my_args)


def printvminfo(vm):
    """
    Print information for a particular virtual machine or recurse into a folder
    with depth protection
    """

    # if this is a group it will have children. if it does, recurse into them
    # and then return
    if hasattr(vm, 'childEntity'):
        print(vm, 'prova')
        vmlist = vm.childEntity
        for i in vmlist:
            printvminfo(i)

    # ***************************************#
    # ***************************************#
    # SUMMARY - contiene tutte le informazioni necessarie!!#
    # ***************************************#
    # ***************************************#
    summary = vm.summary
    v_machine[summary.config.name] = summary.config.instanceUuid
    print(vm, ' has name: ', vm.summary.config.name, ' and UUID: ', vm.summary.config.instanceUuid)
    print(vim.AuthorizationManager.__dict__.keys())
    a = (vim.AuthorizationManager.Role())
    print(a)
    #    print(vim.AuthorizationManager.Role)
    users = vim.AuthorizationManager


#    print(users.summary)
# IMPORTANTE: CONTIENE TUTTE LE INFORMAZIONI
#    print(vm.config)
#    idle = vim.UserDirectory.findUsers('Prova')
#    print(idle)
#    print(summary.config)
#    print(summary.config.name)
#    print(summary.config.uuid)

def main():
    """
    Simple command-line program for listing the virtual machines on a host.
    """

    args = setup_args()
    si = None
    try:
        si = SmartConnectNoSSL(host=args.host,
                               user=args.user,
                               pwd=args.password,
                               port=int(args.port))
        atexit.register(Disconnect, si)
    except vim.fault.InvalidLogin:
        raise SystemExit("Unable to connect to host "
                         "with supplied credentials.")

    content = si.RetrieveContent()
    print(content.rootFolder.childEntity, ' prove')
    provando = (vim.AuthorizationManager.description)
    print(provando)

    for child in content.rootFolder.childEntity:
        if hasattr(child, 'vmFolder'):
            datacenter = child
            vmfolder = datacenter.vmFolder
            vmlist = vmfolder.childEntity
            for vm in vmlist:
                printvminfo(vm)
    # for i in vmlist:
    #    print(i)
    print(v_machine)

    args = setup_args()

    # form a connection...
    context = ssl._create_unverified_context()
    si = connect.SmartConnect(host=args.host, user=args.user, pwd=args.password,
                              port=args.port, sslContext=context)

    # Note: from daemons use a shutdown hook to do this, not the atexit
    atexit.register(connect.Disconnect, si)

    # http://pubs.vmware.com/vsphere-55/topic/com.vmware.wssdk.apiref.doc/vim.SearchIndex.html
    search_index = si.content.searchIndex

    # without exception find managed objects using durable identifiers that the
    # search index can find easily. This is much better than caching information
    # that is non-durable and potentially buggy.

    vm = None
    for i in v_machine:
        vm = search_index.FindByUuid(None, v_machine[i], True, True)
        if not vm:
            print(u"Could not a virtual machine to examine.")
            exit(1)

        print(u"Found Virtual Machine")
        print(u"=====================")
        details = {'name': vm.summary.config.name,
                   'instance UUID': vm.summary.config.instanceUuid,
                   'bios UUID': vm.summary.config.uuid,
                   'path to VM': vm.summary.config.vmPathName,
                   'guest OS id': vm.summary.config.guestId,
                   'guest OS name': vm.summary.config.guestFullName,
                   'host name': vm.runtime.host.name,
                   'last booted timestamp': vm.runtime.bootTime}

        for name, value in details.items():
            print(u"  {0:{width}{base}}: {1}".format(name, value, width=25, base='s'))

        print(u"  Devices:")
        print(u"  --------")
        for device in vm.config.hardware.device:
            # diving into each device, we pull out a few interesting bits
            dev_details = {'key': device.key,
                           'summary': device.deviceInfo.summary,
                           'device type': type(device).__name__,
                           'backing type': type(device.backing).__name__}

            print(u"  label: {0}".format(device.deviceInfo.label))
            print(u"  ------------------")
            for name, value in dev_details.items():
                print(u"    {0:{width}{base}}: {1}".format(name, value,
                                                           width=15, base='s'))

            if device.backing is None:
                continue

            # the following is a bit of a hack, but it lets us build a summary
            # without making many assumptions about the backing type, if the
            # backing type has a file name we *know* it's sitting on a datastore
            # and will have to have all of the following attributes.
            if hasattr(device.backing, 'fileName'):
                datastore = device.backing.datastore
                if datastore:
                    print(u"    datastore")
                    print(u"        name: {0}".format(datastore.name))
                    # there may be multiple hosts, the host property
                    # is a host mount info type not a host system type
                    # but we can navigate to the host system from there
                    for host_mount in datastore.host:
                        host_system = host_mount.key
                        print(u"        host: {0}".format(host_system.name))
                    print(u"        summary")
                    summary = {'capacity': datastore.summary.capacity,
                               'freeSpace': datastore.summary.freeSpace,
                               'file system': datastore.summary.type,
                               'url': datastore.summary.url}
                    for key, val in summary.items():
                        print(u"            {0}: {1}".format(key, val))
                print(u"    fileName: {0}".format(device.backing.fileName))
                print(u"    device ID: {0}".format(device.backing.backingObjectId))

            print(u"  ------------------")

        print(u"=====================")
    a = (vim.AuthorizationManager.Privilege())
    print(a, 'prova')
    exit()


# Start program
if __name__ == "__main__":
    main()
