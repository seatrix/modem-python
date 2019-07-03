"""
Example of using the wlmodem libarary
"""
import logging
import sys
import time
from wlmodem import WlModem, WlModemGenericError

def main():
    """ Demo code """
    logging.basicConfig(level=logging.DEBUG)
    import argparse
    parser = argparse.ArgumentParser(description="Water Linked Modem example")
    parser.add_argument('-D', '--device', action="store", required=True, type=str, help="Serial port.")
    parser.add_argument('--baudrate', action="store", type=int, default=115200, help="Serial baudrate.")
    parser.add_argument('-v' , '--verbose', action="store_true", help="Verbose.")
    args = parser.parse_args()

    modem = WlModem(args.device, debug=args.verbose)
    try:
        modem.connect()
    except WlModemGenericError as err:
        print("Error connecting to modem: {}".format(err))
        sys.exit(1)

    print("Set modem role and channel: ", end="")
    success = modem.cmd_configure("a", 4)
    if success:
        print("success")
    else:
        print("failed")
        sys.exit(1)

    success = modem.cmd_flush_queue()
    print("Flush      :", "success" if success else "failed")

    data = b"HelloSea"
    print("Sending '{}': ".format(data), end="")
    success = modem.cmd_queue_packet(data)
    print("success" if success else "failed")

    import struct
    data = struct.pack(">bbbbbbbb", 8, 7, 6, 5, 4, 3, 2, 1)
    print("Sending encoded numbers {}: ".format(data), end="")
    success = modem.cmd_queue_packet(data)
    print("success" if success else "failed")

    print("Queue length: ", modem.cmd_get_queue_length())
    print("Diagnostic  : ", modem.cmd_get_diagnostic())

    print("Wait for packet from other modem:")
    get = 2
    while get > 0:
        pkt = modem.get_data_packet()
        if pkt:
            print("Got:", pkt)
        get -= 1
        time.sleep(0.1)

    print("Diagnostic  : ", modem.cmd_get_diagnostic())


if __name__ == "__main__":
    main()