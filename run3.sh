#Defining program variables
HADOOP_JAR_PATH="/opt/cloudera/parcels/CDH/lib/hadoop-0.20-mapreduce/contrib/streaming/hadoop-streaming-2.0.0-mr1-cdh4.5.0.jar"
MAPPER="mapper3.py"
REDUCER="reducer2.py"
IP=" /data/gcbretadvn/work/ishan/DecisionTree/naps_pnl_thd201201_201301.csv"
OP=" /data/gcbretadvn/work/ishan/DecisionTree/output1"

hadoop fs -rm -r /data/gcbretadvn/work/ishan/DecisionTree/output1

  hadoop jar $HADOOP_JAR_PATH \
  -file $MAPPER -mapper 'python mapper3.py' \
  -file '/home/ic10636/DecisionTree/modelfile.txt' \
  -file '/home/ic10636/DecisionTree/attributes.txt' \
  -input $IP -output $OP 
  
rm /home/ic10636/DecisionTree/output/part*

hadoop fs -getmerge /data/gcbretadvn/work/ishan/DecisionTree/output1 /home/ic10636/DecisionTree/output/parts

#  -file $REDUCER -reducer 'python reducer.py' \


  #-D mapred.reduce.tasks=1 \

#  -file $REDUCER -reducer 'python reducer2.py' \
