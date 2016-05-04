"""Ukule-LED.

Usage:
    ukule_led practice <chord> port <portname>
    ukule_led play <file> port <portname>
    
"""

import docopt
import serial
import time
from chord_map import *

def file_to_str( filename ):
    with open(filename, "r") as f:
        metadata = f.readline()
        metastrs = metadata.replace('|', ' ').split()
        tempo = metastrs[0]
        if len(tempo) == 2:
            tempo = '0' + tempo
        time = metastrs[1]
        file_str = ""
        for line in f:
            strs = line.replace('|', ' ').split()
            for note in strs:
                if note == '-':
                    lasti = len(file_str)
                    file_str += file_str[lasti - 3:]
                else:
                    num = chord_map[note]
                    num_str = '0' + str(num) if num < 10 else str(num)
                    file_str += num_str + '/'
        file_str = tempo + '/' + time + '/' + file_str + '-1/\n'
        print file_str
        return file_str 

def main():

    arguments = docopt.docopt(__doc__, version='Ukule-LED 0.3')

    serport = arguments['<portname>']
    ser = serial.Serial(serport, 9600)

    if arguments['practice']:
        num = chord_map[ arguments['<chord>'] ]
        num_str = '0' + str(num) if num < 10 else str(num)
        ser.write( '1/' + num_str + '/\n' )
        print '1/' + num_str + '/\n'

    if arguments['play']:
        song_str = file_to_str( arguments['<file>'] )
        ser.write( '2/' + song_str )
        
    time.sleep(1)
    ser.close()

if __name__ == '__main__':
    main()
