"""Ukule-LED.

Usage:
    ukule-led play <file>
    ukule-led practice <chord>

"""

import docopt
import serial
import time

def main():

    arguments = docopt.docopt(__doc__, version='Ukule-LED 0.1')

    ser = serial.Serial('/dev/cu.usbserial-A603V075', 9600)

    if arguments['practice']:
        to_write = arguments['<chord>'] + ' 20\r\n'
        print(to_write)
        ser.write(to_write)
        time.sleep(1)

    ser.close()

if __name__ == '__main__':
    main()
