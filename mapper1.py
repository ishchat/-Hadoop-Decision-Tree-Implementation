#!/usr/bin/env python

#This mapper is used to remove any lines with missing value for any of the variables

import collections, math, sys, json, os, random, csv


def main():
    ###Code to subset data for the node starts here###
    #for line in lines: 
    counter_all=0 
    counter_nonmiss=0
    counter_cond=0
    for line in sys.stdin:
        list_from_line=line.strip('\n').split(',')
        counter_all = counter_all+1
        #print line
        if '' in list_from_line:
            #print line
            #skiping line which has any missing value
            continue
            #continue_outer_for_loop=False
            #print line
            #print "ishan"
            #obs_row = line.split(",")
            #obs_class = obs_row[0]
            #obs_row.remove(obs_class)
        else:
            print line
            counter_nonmiss=counter_nonmiss+1

main()
