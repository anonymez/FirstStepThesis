import cis
import cisConnect
import cisHost
import cisSetupArgs


def main():
    args = cisSetupArgs.setup_args()
    si = cisConnect.connection(args)
    content = si.RetrieveContent()
    cisHostCount = cisHost.hostControls(si)
    controls_8_x = cis.controls_vm(si)
    print(cisHostCount)
    print(controls_8_x)

    keyCounter = cisHostCount[0].__len__()
    keyCounter = keyCounter + controls_8_x.__len__()
    secCounter = 0
    for key, value in controls_8_x.items():
        secCounter = secCounter + value
    for key, value in cisHostCount[0].items():
        secCounter = secCounter + value

    print("cis 4.2 value: "),
    print(cisHostCount[1])
    print("cis 5.7 value: "),
    print(cisHostCount[2])
    print("cis 5.8 value: "),
    print(cisHostCount[3])
    print("cis 7.4 value: "),
    print(cisHostCount[4])
    print("cis 7.6 esit [not scored]: "),
    print(cisHostCount[5])
    print('Security level: ' + str(secCounter) + '/' + str(keyCounter))


if __name__ == "__main__":
    main()
