"""TEST

Usage:
    test play <file>
    test practice <chord>

"""

import docopt
import serial
import time

def main():

    arguments = docopt.docopt(__doc__, version='TEST')

    ser = serial.Serial('/dev/cu.usbserial-A603UZAB', 9600)

    if arguments['practice']:
        pass

    if arguments['play']:
        ser.write(arguments['<file>'] + '\r\n')
        
    time.sleep(1)
    ser.close()

if __name__ == '__main__':
    main()
