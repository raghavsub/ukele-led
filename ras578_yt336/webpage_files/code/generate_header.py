"""Generate Header.

Usage:
    generate_header <type> <1> <2> <3> <4>

"""

import docopt

with open('header_tmp.txt', 'a') as f:

    line = ''

    arguments = docopt.docopt(__doc__, version='-500')

    def_subarray = '{0, 0, 0}'
    subarray = ''
    bools = [False]*16

    if arguments['<type>'] == 'M':
        subarray = '{0, INTENS, 0}'

    if arguments['<type>'] == 'm':
        subarray = '{INTENS, 0, 0}'

    if arguments['<type>'] == '7':
        subarray = '{0, 0, INTENS}'

    if arguments['<1>'] == '1':
        bools[0] = True

    if arguments['<1>'] == '2':
        bools[7] = True

    if arguments['<1>'] == '3':
        bools[8] = True

    if arguments['<1>'] == '4':
        bools[15] = True

    if arguments['<2>'] == '1':
        bools[1] = True

    if arguments['<2>'] == '2':
        bools[6] = True

    if arguments['<2>'] == '3':
        bools[9] = True

    if arguments['<2>'] == '4':
        bools[14] = True

    if arguments['<3>'] == '1':
        bools[2] = True

    if arguments['<3>'] == '2':
        bools[5] = True

    if arguments['<3>'] == '3':
        bools[10] = True

    if arguments['<3>'] == '4':
        bools[13] = True

    if arguments['<4>'] == '1':
        bools[3] = True

    if arguments['<4>'] == '2':
        bools[4] = True

    if arguments['<4>'] == '3':
        bools[11] = True

    if arguments['<4>'] == '4':
        bools[12] = True

    line += '{'
    for i, b in enumerate(bools):
        if b is True:
            line += subarray
        else: 
            line += def_subarray

        if i != len(bools) - 1:
            line += ', '
        else:
            line += '},\n'

    f.write(line)
