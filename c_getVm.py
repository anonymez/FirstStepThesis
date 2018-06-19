from __future__ import print_function
import atexit
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
    print(summary)
    print(summary.runtime.host.vm)
    v_machine[summary.config.name] = summary.config.instanceUuid
    print(vm, ' has name: ', vm.summary.config.name, ' and UUID: ', vm.summary.config.instanceUuid)


#    print(vim.AuthorizationManager.Role)
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

    for child in content.rootFolder.childEntity:
        if hasattr(child, 'vmFolder'):
            datacenter = child
            vmfolder = datacenter.vmFolder
            vmlist = vmfolder.childEntity
            for vm in vmlist:
                printvminfo(vm)
                ################################
                ###permessi contiente l'array###
                ######dei permessi sulle vm#####
                permessi = content.authorizationManager.RetrieveEntityPermissions(vm, True)
                ################################
                ###stampa gli id dei permessi###
                ###il contenuto e' in un array###
                ################################
                for perm in permessi:
                    print(perm)
                    print(perm.roleId)
        #                if hasattr(content.authorizationManager.Permission,'roleId'):
        #                    print('prova')
        ruoli = content.authorizationManager.RetrieveRolePermissions(-1)
        print(ruoli)
    ###########################
    # Stampa gli utenti#
    ##sulle macchine##
    ###########################
    print('=========')
    print('Elenco degli utenti sulle macchine')
    print('=========')
    utenti = (content.authorizationManager.RetrieveAllPermissions())
    print(utenti)

    ruoli2 = (content.authorizationManager.roleList)
    for p in ruoli2:
        print('ID Role = ', p.roleId, ', nome = ', p.name)

    ###########################
    # Stampa gli utenti#
    ###########################
    print('=========')
    print('Elenco degli utenti')
    print('=========')
    #    utenti2 = content.authorizationManager.privilegeList
    utenti2 = (
        content.userDirectory.RetrieveUserGroups(searchStr='', exactMatch=False, findUsers=True, findGroups=False))
    print(utenti2, 'prova')
    #    print(content.sessionManager.sessionList)
    #    print(content.datacenter.datastore)
    # .userDirectory.domainList)
    datastore = content.rootFolder.childEntity
    ###########################
    # Info sul datastore#
    ###########################
    for data in datastore:
        dataStoreEntity = data.datastoreFolder.childEntity
        for dataEntity in dataStoreEntity:
            print(dataEntity.info)
    virtual = content.virtualDiskManager
    datastoreName = content.datastoreNamespaceManager
    ###########################
    # Info network #
    ###########################
    dataStore = content.rootFolder.childEntity
    for data in dataStore:
        net = data.network
        for network in net:
            print(network.summary)
            print(network.vm)
            print(network.host)

    ###########################
    # Info IP #
    ###########################
    dataIP = content.rootFolder.childEntity
    ipPool = content.ipPoolManager
    for ipData in dataIP:
        pool = ipData.datastoreFolder.childEntity
        print("prova", ipPool, "prova")

    ##################
    # Get resource pool
    ##################

    resource = data.hostFolder.childEntity
    for i in resource:
        print(i.resourcePool.summary)

    ###########################
    # Info switch #
    ###########################


#   NOT SUPPORTED
#    dataSwitch = content.dvSwitchManager.QueryAvailableDvsSpec()
#   print(dataSwitch)

###########################
# File di log #
###########################

#    log = content.diagnosticManager.QueryDescriptions()
#    print(log)
#    for i in log:
#        print(i)
#        log2 = content.diagnosticManager.BrowseDiagnosticLog(key=i.key)
#        print(log2)

# Start program
if __name__ == "__main__":
    main()
