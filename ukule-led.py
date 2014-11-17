"""Ukule-LED.

Usage:
    ukule-led play <file>
    ukule-led practice <chord> [-b <brightness>]

"""

import docopt
import serial
import time

def main():

    arguments = docopt.docopt(__doc__, version='Ukule-LED 0.1')

    ser = serial.Serial('/dev/cu.usbserial-A603V075', 9600)

    if arguments['practice']:
        brightness = '20'
        if arguments['-b']:
            brightness = arguments['<brightness>']

        to_write = arguments['<chord>'] + ' ' + brightness + '\r\n'
        ser.write(to_write)
        
    time.sleep(1)
    ser.close()

if __name__ == '__main__':
    main()
