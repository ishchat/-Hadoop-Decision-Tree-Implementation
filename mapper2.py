#This is mapper which will find min and max for each numeric variable in its data chunk

#!/usr/bin/env python

#This code will hold min and max for numeric variables for the particular mapper

import collections, math, sys, json, os, random, csv

def main():
    #declaring dictionary to hold min and max for numeric variables
    min_max=dict()
    f2 = open('attributes.txt', 'rb').read()
    attributes=json.loads(f2)
    number_of_predictors = len(attributes)
    counter_all=0 
    counter_nonmiss=0
    counter_cond=0
    for line in sys.stdin:
        #'\t' got introduced in naps_pnl_thd201201_201301_nonmiss due to running of earlier mapreduce
        line=line.strip('\n').strip('\t').split(',')
        counter_all = counter_all+1
        #print line
        if '' in line:
            #skiping line which has any missing value
            continue
        else:
            #print line
            #print "going in else"
            counter_nonmiss=counter_nonmiss+1                
            #print "number_of_predictors:  ",number_of_predictors
            for j in range(1,number_of_predictors+1):
                if attributes["COL"+str(j)] == "numeric":
                    #print attributes["COL"+str(j)]
                    #print "COL"+str(j)+"is"+"numeric"
                    if counter_nonmiss==1:
                        min_max["COL"+str(j)]=[line[j],line[j]]
                    if min_max["COL"+str(j)][0]>line[j]:
                        min_max["COL"+str(j)][0]=line[j]
                    if min_max["COL"+str(j)][1]<line[j]:
                        min_max["COL"+str(j)][1]=line[j]
            #print min_max["COL"+str(1)],min_max["COL"+str(1)][0],line[0]
    for k in min_max:
                key=k
                value=min_max[k]
                print '%s\t%s' % (key, value)
if __name__ == '__main__':
    main()
