#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
It compresses using lossy compression the ids of all reads from a input FASTQ file (using the read index/count).
The reads ids have all the ids in alphabetically order.




Author: Daniel Nicorici, Daniel.Nicorici@gmail.com

Copyright (c) 2009-2014 Daniel Nicorici

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.


"""
import sys
import os
import optparse
import gc
import gzip
import string
import math
import itertools

def generate_id(t, no12 = False):
    digits = string.digits + string.ascii_uppercase
    l = len(digits)
    r = int(math.ceil(math.log(float(t+2)/float(2),l)))
    if no12:
        for el in itertools.product(digits,repeat = r):
            x = ''.join(el)
            yield "@%s\n" % (x,)
            yield "@%s\n" % (x,)
    else:
        for el in itertools.product(digits,repeat = r):
            x = ''.join(el)
            yield "@%s/1\n" % (x,)
            yield "@%s/2\n" % (x,)

if __name__ == '__main__':

    #command line parsing

    usage = "%prog [options]"
    description = """It compresses using lossy compression the ids of all reads from a input FASTQ file (using the read index/count). The compressed reads ids have all the ids in alphabetically order."""
    version = "%prog 0.10 beta"

    parser = optparse.OptionParser(usage=usage,description=description,version=version)

    parser.add_option("--input","-i",
                      action="store",
                      type="string",
                      dest="input_filename",
                      help="""The input file in FASTQ Solexa file (also given thru STDOUT or as gzipped file). It is assumed that the input reads are shuffled (that is read id 1 is followed by read id 2 where read 1 and read 2 form a pair). """)

    parser.add_option("--output","-o",
                      action="store",
                      type="string",
                      dest="output_filename",
                      help="""The output text file containg the changed reads ids (also given thru STDOUT or as gzipped file).""")

    parser.add_option("--count-reads","-n",
                      action = "store",
                      type = "string",
                      dest = "count",
                      help="""The total number of reads in the input file. This is used in order to generate the compress the best the reads ids.""")

    parser.add_option("--no12","-s",
                      action = "store_true",
                      dest = "no12",
                      default = False,
                      help="""If this is set than no /1 and /2 will be added to the compressed reads ids.""")

    (options,args) = parser.parse_args()

    # validate options
    if not (options.input_filename and
            options.output_filename and
            options.count
            ):
        parser.print_help()
        parser.error("Input and output files should be specified!")
        sys.exit(1)


    fin = None
    if options.input_filename == '-':
        fin = sys.stdin
    elif options.input_filename.lower().endswith('.gz'):
        fin = gzip.open(options.input_filename,'r')
    else:
        fin = open(options.input_filename,'r')

    fou = None
    if options.output_filename == '-':
        fou = sys.stdout
    elif options.output_filename.lower().endswith('.gz'):
        fou = gzip.open(options.output_filename,'w')
    else:
        fou = open(options.output_filename,'w')

    n = 0
    if os.path.isfile(options.count):
        n = sum([int(line.strip()) for line in file(options.count,'r').readlines() if line.strip()])
    else:
        n = int(options.count)
    if not n:
        print >>sys.stderr,"ERROR: Cannot read/use the '--count-reads' option!"
        sys.exit(1)
    i = 0
    ids = generate_id(n)
    while True:
        lines = fin.readlines(10**8)
        if not lines:
            break
        gc.disable()
        lines = [line if (j+i)%4 != 0 else ids.next() for (j,line) in enumerate(lines)]
        gc.enable()
        i = i + len(lines)
        fou.writelines(lines)
    fin.close()
    fou.close()

    #
