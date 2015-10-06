#reducer to find min and max across all mapper outputs for each numeric column

#!/usr/bin/env python

import collections, math, sys, json, os, random, csv


def main():

    current_key = None
    current_count = 0
    key = None

    #declaring dictionary to hold min and max for numeric variables
    min_max=dict()

    counter_all=0 
    counter_nonmiss=0
    counter_cond=0
    for line in sys.stdin:
        line=line.strip('\n').strip('\t').strip(']').split('\t')
        line[1]=line[1].strip('[')
        counter_all = counter_all+1
        #print line
        if '' in line:
            #skiping line which has any missing value
            continue
        else:
            counter_nonmiss=counter_nonmiss+1      
            key=line[0]
            value=line[1].strip('"').strip('"').split(',')
            min=value[0].strip('"').strip('"')
            max=value[1].strip('"').strip('"')
            #print key, value, min, max
            if current_key is None:
                #print "NEW KEY STARTS HERE", key
                current_key=key
                min_max[key]=[min,max]
            if current_key == key:
                if min_max[key][0]>min:
                    min_max[key][0]=min
                if min_max[key][1]<max:
                    min_max[key][1]=max
            else:
                #print "NEW KEY STARTS HERE", key
                current_key=key
                min_max[key]=[min,max]

    for k in min_max:
                dict_key=k
                dict_value=min_max[k]
                print dict_key+':'+dict_value[0]+','+dict_value[1]
                #print '%s\t%s' % (dict_key, dict_value)
                #print json.dumps(min_max)

if __name__ == '__main__':
    main()
