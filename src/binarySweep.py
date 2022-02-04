#!/usr/bin/env python3
#
#   Luke Ingram Feb 2022 Philadelphia. PA, USA.
#   
#   binarySweep.py
#   
#   small scale unix command-line tool for removing unused C/C++ binary files 
#   in specified directory and/or subdirectories up to specified depth 
#   


import argparse
#import logging as log <---FOR USE WITH VERBOSE OUTPUT
import sys
import os
from stat import * 




#TODO add --verbose to parser, use logging module
#       add -a flag and optional directory depth cap 
#      
def init_parser():
    parser = argparse.ArgumentParser()
    #group1 = argparse._MutuallyExclusiveGroup()
    parser.add_argument("PATH",type=str,help="path to target directory.")
    parser.add_argument("-a",dest="all",help="sweep all subdirectories within target",action="store_true")
    parser.add_argument("-maxdepth",dest="maxdepth",type=int,help="subdirectory depth limiter, max = 9999",default=0,action="store")
    #group1.add_argument("--verbose",help="verbose output",action="store_true")
    return parser
    



#TODO sweep and remove 
def sweepdir(path,depth):
    #TODO loop through dir specified in path, check type of file. 
    
    for f in os.listdir(path): 
        fpath = os.path.join(path,fpath)
        if os.access(f,os.W_OK): 
            s = os.stat(f)
            if S_ISDIR(s.st_mode): 
                print("found dir",fpath)
                #TODO impliment recursive depth counting
            if 


        
        
    

    return 0; 


#TODO argument logic 
def main(): 
    parser = init_parser()
    args = parser.parse_args()

    if args.all:
        depth = 9999

    if args.maxdepth > 9999: 
        parser.error("maximum depth value %d too large. please specify a value less than 9999"%(args.maxdepth))
        parser.print_help()

    if os.path.isdir(args.PATH) and os.access(args.PATH,os.W_OK): 
        sweepdir(args.PATH,depth)

    else:
        parser.error("specified target \'%s\' inaccessible. Does it exist?"%(args.target))
        parser.print_help()
        exit(128)

    sys.exit(0)


if __name__ == '__main__':
    main(); 