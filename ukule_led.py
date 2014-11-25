"""Ukule-LED.

Usage:
    ukule_led play <file> port <portname>
    ukule_led practice <chord> port <portname>

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
            print strs
            for note in strs:
                if note == '-':
                    lasti = len(file_str)
                    file_str += file_str[lasti - 3:]
                else:
                    num = chord_map[note]
                    num_str = '0' + str(num) if num < 10 else str(num)
                    file_str += num_str + '/'
        file_str = tempo + '/' + time + '/' + file_str + '-1\r\n'
        print file_str
        return file_str 

def main():
    # print chord_map['A#7']
    arguments = docopt.docopt(__doc__, version='Ukule-LED 0.2')

    serport = arguments['<portname>']
    ser = serial.Serial(serport, 9600)

    if arguments['practice']:
        ser.write(arguments['<chord>'] + '\r\n')

    if arguments['play']:
        song_str = file_to_str( arguments['<file>'] )
        ser.write(song_str)
        
    time.sleep(1)
    ser.close()

if __name__ == '__main__':
    main()
