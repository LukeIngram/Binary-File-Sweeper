#!/usr/bin/env python3
#   
#   binarySweep.py
#   
#   small scale unix command-line tool for removing unused C/C++ binary files 
#   in specified directory and/or subdirectories up to specified depth 
#
#    
#   MIT License
#   
#   Copyright (c) 2022 Luke Ingram
#   
#   Permission is hereby granted, free of charge, to any person obtaining a copy
#   of this software and associated documentation files (the "Software"), to deal
#   in the Software without restriction, including without limitation the rights
#   to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#   copies of the Software, and to permit persons to whom the Software is
#   furnished to do so, subject to the following conditions:
#   
#   The above copyright notice and this permission notice shall be included in all
#   copies or substantial portions of the Software.
#   
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#   SOFTWARE.   



import argparse
import sys
import os
from stat import * 
import subprocess
import logging as log 
import multiprocessing as multi




#TODO add --verbose to parser, use logging module
#       add -a flag and optional directory depth cap 
#       add -c flag to specify the collection action set 
#       add -r flag to specify the removal action set 
def init_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("PATH",type=str,help="path to target directory.")
    parser.add_argument("-a",dest="all",help="sweep all subdirectories within target",action="store_true")
    parser.add_argument("-maxdepth",dest="maxdepth",type=int,help="subdirectory depth limiter, max = 9999",default=0,action="store")
    #actionGroup = parser.add_mutually_exclusive_group()
    logGroup = parser.add_mutually_exclusive_group()
    logGroup.add_argument("--verbose",help="verbose output",action="store_true")
    return parser
    
#Currently executing a unix command to get the filetype, potentually improve 
#SLOW?????
def isbin(path): 
    file = subprocess.Popen(('file','-b', '--mime-type',path),stdout=subprocess.PIPE)
    output = subprocess.check_output(('sed','s|/.*||'),stdin=file.stdout)
    file.wait()
    return "application\n" == output.decode("utf-8")


def sweepdir(path,depth):
    log.info("searching %s"%(path)) 
    for f in os.listdir(path): 
        fpath = os.path.join(path,f)
        log.info("found \'%s\'"%(fpath))
        if os.access(fpath,os.W_OK): 
            if os.path.isdir(fpath): 
                if depth > 0: 
                    p = multi.Process(target=sweepdir,args=(fpath,depth-1))
                    p.start()
            elif os.access(fpath,os.X_OK) and isbin(fpath): 
                log.info("located binary executable \'%s\'"%(fpath))
    

def main(): 
    parser = init_parser()
    args = parser.parse_args()

    depth = args.maxdepth
    mode = os.W_OK

    if args.all:
        depth = 9999

    if args.list: 
        mode = os.R_OK

    if args.verbose: 
        log.basicConfig(format="%(levelname)s: %(message)s", level=log.DEBUG)
        log.info("Verbose output.")
    else: 
        log.basicConfig(format="%(levelname)s: %(message)s")

    if args.maxdepth > 9999 or args.maxdepth < 0: 
        parser.error("maximum depth value %d invalid. 0 < maxdepth < 10000"%(args.maxdepth))
        parser.print_help()

    if os.path.isdir(args.PATH) and os.access(args.PATH,mode): 
        sweepdir(args.PATH,depth)

    else:
        parser.error("specified target \'%s\' inaccessible. Does it exist?"%(args.PATH))
        parser.print_help()
        exit(128)

    sys.exit(0)


if __name__ == '__main__':
    main(); 