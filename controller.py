#!/usr/bin/env python

import sys, os, json, csv


'''
#To remove any lines with missing values

#Defining program variables
HADOOP_JAR_PATH="/opt/cloudera/parcels/CDH/lib/hadoop-0.20-mapreduce/contrib/streaming/hadoop-streaming-2.5.0-mr1-cdh5.3.3.jar"
MAPPER="mapper1.py"
IP=" /data/gcbretadvn/work/ishan/DecisionTree/naps_pnl_thd201201_201301.csv"
OP=" /data/gcbretadvn/work/ishan/DecisionTree/output1"

os.system("hadoop fs -rm -r /data/gcbretadvn/work/ishan/DecisionTree/output1")

os.system("hadoop jar " + HADOOP_JAR_PATH +" -file " + MAPPER + " -mapper 'python mapper1.py' -file '/home/ic10636/DecisionTree/modelfile.txt' -file '/home/ic10636/DecisionTree/attributes.txt' -input" + IP + " -output" + OP)
  
os.system("rm /home/ic10636/DecisionTree/output/part*")

os.system("hadoop fs -getmerge /data/gcbretadvn/work/ishan/DecisionTree/output1 /home/ic10636/DecisionTree/output/naps_pnl_thd201201_201301_nonmiss")

os.system("hadoop fs -put /home/ic10636/DecisionTree/output/naps_pnl_thd201201_201301_nonmiss /data/gcbretadvn/work/ishan/DecisionTree")
'''


'''
#The mapper here finds the min and max for each numeric variable for the data chunk coming to it
#The reducer here aggregates th emin and max for the numeric variables from each mapper and finds overall min and max for each #numeric variable

HADOOP_JAR_PATH="/opt/cloudera/parcels/CDH/lib/hadoop-0.20-mapreduce/contrib/streaming/hadoop-streaming-2.5.0-mr1-cdh5.3.3.jar"
MAPPER="mapper2.py"
REDUCER="reducer2.py"
IP=" /data/gcbretadvn/work/ishan/DecisionTree/naps_pnl_thd201201_201301_nonmiss"
OP=" /data/gcbretadvn/work/ishan/DecisionTree/output1"

os.system("hadoop fs -rm -r /data/gcbretadvn/work/ishan/DecisionTree/output1")

os.system("hadoop jar " + HADOOP_JAR_PATH +" -file " + MAPPER + " -mapper 'python mapper2.py' " + " -file " + REDUCER + " -reducer 'python reducer2.py' -file '/home/ic10636/DecisionTree/modelfile.txt' -file '/home/ic10636/DecisionTree/attributes.txt' -input" + IP + " -output" + OP)
 
os.system("rm /home/ic10636/DecisionTree/output/*")

os.system("hadoop fs -getmerge /data/gcbretadvn/work/ishan/DecisionTree/output1 /home/ic10636/DecisionTree/output/parts")
'''


'''
#This piece of code takes overall min and max of each numeric variable from output of above mapreduce 
#Then it creates a file min_max.txt from that output to hold min and max of each numeric variable in JSON format

#http://stackoverflow.com/questions/23520542/issue-with-merging-multiple-json-files-in-python

#declaring a dictionary in python

min_max={}

f1 = open('/home/ic10636/DecisionTree/output/parts', 'rb')
count=0

while True:
    try:
        min_max_line=f1.readline().strip('\t').strip('\n').strip('\t')
        min_max_line_list=min_max_line.split(':')
        if '' in min_max_line_list:
            break
        count=count+1
        min_max[min_max_line_list[0]]=min_max_line_list[1]
        #print "min_max_line",min_max_line,"min_max_line_list[0]",min_max_line_list[0],"min_max_line_list[1]",min_max_line_list[1]
    except:
        #print "Unexpected error:", sys.exc_info()[0]
        break

#print min_max

with open("min_max.txt", "wb") as outfile:
     json.dump(min_max, outfile)

outfile.close()


#f2 = open('min_max.txt', 'rb').read()
#min_max=json.loads(f2)

#print min_max["COL6"]

'''


'''
HADOOP_JAR_PATH="/opt/cloudera/parcels/CDH/lib/hadoop-0.20-mapreduce/contrib/streaming/hadoop-streaming-2.5.0-mr1-cdh5.3.3.jar"
MAPPER="mapper3.py"
REDUCER="reducer3.py"
IP=" /data/gcbretadvn/work/ishan/DecisionTree/naps_pnl_thd201201_201301_nonmiss"
OP=" /data/gcbretadvn/work/ishan/DecisionTree/output1"

os.system("hadoop fs -rm -r /data/gcbretadvn/work/ishan/DecisionTree/output1")

os.system("hadoop jar " + HADOOP_JAR_PATH + " -D mapred.map.tasks=1 " + " -file " + MAPPER + " -mapper 'python mapper3.py' " + " -file " + REDUCER + " -reducer 'python reducer3.py' " + " -file '/home/ic10636/DecisionTree/min_max.txt' -file '/home/ic10636/DecisionTree/modelfile.txt' -file '/home/ic10636/DecisionTree/attributes.txt' -input" + IP + " -output" + OP)
 
#os.system("hadoop jar " + HADOOP_JAR_PATH + " -D mapred.map.tasks=1 " + " -file " + MAPPER + " -mapper 'python mapper3.py' " + " -file '/home/ic10636/DecisionTree/min_max.txt' -file '/home/ic10636/DecisionTree/modelfile.txt' -file '/home/ic10636/DecisionTree/attributes.txt' -input" + IP + " -output" + OP)
 
os.system("rm /home/ic10636/DecisionTree/output/*")

os.system("hadoop fs -getmerge /data/gcbretadvn/work/ishan/DecisionTree/output1 /home/ic10636/DecisionTree/output/parts")

'''

