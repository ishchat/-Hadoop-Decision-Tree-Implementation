#!/usr/bin/env python


from __future__ import division
import collections, math, sys, json, os, random
from itertools import groupby
from operator import itemgetter
import re

def posfinder(datacolumn,val):
       pos_save = [] #declare empty list pos_save
       req_col = datacolumn[:] #req_col is copy of datacolumn
       num_instances = req_col.count(val) #num_instances will save number of times val appears in datacolumn
       for i in range(0,num_instances):
           pos_save.append(req_col.index(val)) #req_col.index(val) gives first occurance of val in req_col
           req_col[req_col.index(val)]='NULL' #value at index corresponding to above occurence is declared NULL
       #print(pos_save)
       return pos_save #pos_save is list of indices having value val in datacolumn


def main():
    
#lines = [ line for line in sys.stdin ]

    current_key = None
    current_count = 0
    key = None

    sum_len_a_list1=0
    sum_a_list1_count_0=0
    sum_len_a_list2=0
    sum_a_list2_count_0=0
    list_of_three_tuple = []

    list_of_split_Gini_tuple=[]

    # input comes from STDIN
    for line in sys.stdin:
        # remove leading and trailing whitespace
        line = line.strip()
        # parse the input we got from mapper.py
        #print line
        #https://www.safaribooksonline.com/library/view/python-cookbook-3rd/9781449357337/ch02s01.html
        #key, value = line.split('\s', 1)
        if line != "":
            key, value = re.split('\s*',line,1)
            #print key, value
        else:
            continue
        if key is None:
            continue
        value = value.strip('[').strip(']').split(',')
        #print key, value
        if current_key is None:
            current_key=key
            #print "NEW KEY STARTS HERE", key
        if current_key == key:
            if key.count('#') == 2:
                sum_len_a_list1=sum_len_a_list1+float(value[0])
                sum_a_list1_count_0=sum_a_list1_count_0+float(value[1])
                sum_len_a_list2=sum_len_a_list2+float(value[2])
                sum_a_list2_count_0=sum_a_list2_count_0+float(value[3])
                #current_count=current_count+1
                #print "current_key:", current_key
                #print "line :",line
                #print "key", key
                #print "value", value
                #print sum_len_a_list1,sum_a_list1_count_0,sum_len_a_list2,sum_a_list2_count_0
                #print "code block1"
            elif key.count('#') == 1:
                list_of_three_tuple.append(value)
                #print "current_key:", current_key
                #print "line :",line
                #print "key", key
                #print "value", value
                #print list_of_three_tuple 
                #print "code block1"
            else:
                pass                                              
        else:
            if current_key.count('#') == 2:
                #current_count=1
                #calculate Gini
                #push in key,Gini 
                #print (current_key,current_count)
                #Gini measure used in Shih paper with Breiman's categorical split theorem
                #Gini measure is used in classification tree
                #https://www.uic.edu/classes/idsc/ids572cna/Decision%20Trees_1.pdf  --  Gini measure definition
                try:
                    gini_a_list1 = (float(sum_a_list1_count_0)/float(sum_len_a_list1))**2 + (float(sum_len_a_list1-sum_a_list1_count_0)/float(sum_len_a_list1))**2                    
                except:
                    #Error will only occur for those values out of list_of_hundred_values which are out of range for the available values in the node
                    #As we can't split at these values as they are out of range(less than min of available node data values or greater than max), we don't need Gini for them
                    #print "sum_len_a_list1 :", sum_len_a_list1
                    #print "error gini_a_list1 ",current_key, " sum_len_a_list1 :", sum_len_a_list1
                    pass
                try:
                    gini_a_list2 = (float(sum_a_list2_count_0)/float(sum_len_a_list2))**2 + (float(sum_len_a_list2-sum_a_list2_count_0)/float(sum_len_a_list2))**2
                except:
                    #Error will only occur for those values out of list_of_hundred_values which are out of range for the available values in the node
                    #As we can't split at these values as they are out of range(less than min of available node data values or greater than max), we don't need Gini for them
                    #print "sum_len_a_list2 :", sum_len_a_list2
                    #print "error gini_a_list2 ",current_key, " sum_len_a_list2 :", sum_len_a_list2
                    pass
                if (sum_len_a_list1 != 0) & (sum_len_a_list2 != 0):
                    Gini=(sum_len_a_list1*gini_a_list1+sum_len_a_list2*gini_a_list2)/(sum_len_a_list1+sum_len_a_list2)
                    list_of_split_Gini_tuple.append([current_key,Gini])                    
                    #print current_key, sum_len_a_list1, sum_a_list1_count_0, sum_len_a_list2, sum_a_list2_count_0, " Gini ", Gini, "list_of_split_Gini_tuple", list_of_split_Gini_tuple
                #print "current_key:", current_key
                #print "code block2"
            elif current_key.count('#') == 1:
                #http://stackoverflow.com/questions/3749512/python-group-by
                sortkeyfn = key=lambda s:s[0]
                list_of_three_tuple.sort(key=sortkeyfn)
                #print "list_of_three_tuple",list_of_three_tuple                
                #http://code.activestate.com/recipes/304162-summary-reports-using-itertoolsgroupby/       
                list_of_first_and_sum_of_second_from_tuple=[]
                for k, group in groupby(list_of_three_tuple,key=itemgetter(0)):
                    list_of_first_and_sum_of_second_from_tuple.append([k,sum(int(row[1]) for row in group)])
                #print "list_of_first_and_sum_of_second_from_tuple", list_of_first_and_sum_of_second_from_tuple
                list_of_first_and_sum_of_third_from_tuple=[]
                for k, group in groupby(list_of_three_tuple,key=itemgetter(0)):
                    list_of_first_and_sum_of_third_from_tuple.append([k,sum(int(row[2]) for row in group)])
                #print "list_of_first_and_sum_of_third_from_tuple", list_of_first_and_sum_of_third_from_tuple             
                list_of_first_as_group_and_sumofsecond_sumofthird_from_tuple=[]
                for iterator_on_list in zip(list_of_first_and_sum_of_second_from_tuple,list_of_first_and_sum_of_third_from_tuple):
                    list_of_first_as_group_and_sumofsecond_sumofthird_from_tuple.append([iterator_on_list[0][0],iterator_on_list[0][1],iterator_on_list[1][1]])
                #print "list_of_first_as_group_and_sumofsecond_sumofthird_from_tuple", list_of_first_as_group_and_sumofsecond_sumofthird_from_tuple
                #Run Breiman algorithm to get order of increasing P(Y=0) (equivalent to decreasing P(Y=1))
                #https://wiki.python.org/moin/HowTo/Sorting#Sorting_Basics  <- Complex list object sorting
                sorted_list_of_first_as_group_and_sumofsecond_sumofthird_from_tuple = sorted(list_of_first_as_group_and_sumofsecond_sumofthird_from_tuple, key=lambda student:(float(student[2])/float(student[1])))
                #Find the Gini coefficient for subsequences in order
                Max_Gini_for_the_categorical_column=None
                Max_Split_for_the_categorical_column=None
                for i in range(0,len(sorted_list_of_first_as_group_and_sumofsecond_sumofthird_from_tuple)):
                    sum_a_list1_count_0=0
                    sum_len_a_list1=0
                    sum_a_list2_count_0=0
                    sum_len_a_list2=0
                    for j in range(0,i+1):
                        sum_len_a_list1=sum_len_a_list1+sorted_list_of_first_as_group_and_sumofsecond_sumofthird_from_tuple[j][1]
                        sum_a_list1_count_0=sum_a_list1_count_0+sorted_list_of_first_as_group_and_sumofsecond_sumofthird_from_tuple[j][2]
                    for j in range(i+1,len(sorted_list_of_first_as_group_and_sumofsecond_sumofthird_from_tuple)):
                        sum_len_a_list2=sum_len_a_list2+sorted_list_of_first_as_group_and_sumofsecond_sumofthird_from_tuple[j][1]
                        sum_a_list2_count_0=sum_a_list2_count_0+sorted_list_of_first_as_group_and_sumofsecond_sumofthird_from_tuple[j][2]
                    try:
                        gini_a_list1 = (float(sum_a_list1_count_0)/float(sum_len_a_list1))**2 + (float(sum_len_a_list1-sum_a_list1_count_0)/float(sum_len_a_list1))**2
                    except:
                        pass
                    try:
                        gini_a_list2 = (float(sum_a_list2_count_0)/float(sum_len_a_list2))**2 + (float(sum_len_a_list2-sum_a_list2_count_0)/float(sum_len_a_list2))**2
                    except:
                        pass
                    if (sum_len_a_list1 != 0) & (sum_len_a_list2 != 0):
                        Gini=(sum_len_a_list1*gini_a_list1+sum_len_a_list2*gini_a_list2)/(sum_len_a_list1+sum_len_a_list2)
                        if Gini>Max_Gini_for_the_categorical_column:
                            Max_Gini_for_the_categorical_column=Gini
                            Max_Split_for_the_categorical_column=sorted_list_of_first_as_group_and_sumofsecond_sumofthird_from_tuple[0:i+1]+["split point"]+sorted_list_of_first_as_group_and_sumofsecond_sumofthird_from_tuple[(i+1):len(sorted_list_of_first_as_group_and_sumofsecond_sumofthird_from_tuple)]
                            #print current_key, sum_len_a_list1, sum_a_list1_count_0, sum_len_a_list2, sum_a_list2_count_0, " Gini ", Gini
                #As the key of categorical key is just column name and does not contain split, need to concatenate full ordered sequence with key name along with "split point" keyword to signify the splitting point
                list_of_split_Gini_tuple.append([current_key+"#"+str(Max_Split_for_the_categorical_column),Max_Gini_for_the_categorical_column])
                #print current_key, "sorted_list_of_first_as_group_and_sumofsecond_sumofthird_from_tuple : ", sorted_list_of_first_as_group_and_sumofsecond_sumofthird_from_tuple, " list_of_split_Gini_tuple ", list_of_split_Gini_tuple
                #print "current_key:", current_key
                #print "code block2"                               
            else:
                pass
            #print "NEW KEY STARTS HERE", key
            if key.count('#') == 2:
                #Storing values for new key
                current_key = key
                sum_len_a_list1=float(value[0])
                sum_a_list1_count_0=float(value[1])
                sum_len_a_list2=float(value[2])
                sum_a_list2_count_0=float(value[3])
                #print "current_key:", current_key
                #print "line :",line
                #print "key", key
                #print "value", value
                #print sum_len_a_list1,sum_a_list1_count_0,sum_len_a_list2,sum_a_list2_count_0
                #print "code block3"
            elif key.count('#') == 1:
                #Storing values for new key
                current_key = key
                list_of_three_tuple=[]
                list_of_three_tuple.append(value)
                #print "current_key:", current_key
                #print "line :",line
                #print "key", key
                #print "value", value
                #print list_of_three_tuple
                #print "code block3"
            else:
                pass      
    #Processing for last key
    if current_key is not None:
        if current_key.count('#') == 2:
            #current_count=1
            #calculate Gini
            #push in key,Gini 
            #print (current_key,current_count)
            #Gini measure used in Shih paper with Breiman's categorical split theorem
            #Gini measure is used in classification tree
            #https://www.uic.edu/classes/idsc/ids572cna/Decision%20Trees_1.pdf  --  Gini measure definition
            try:
                 gini_a_list1 = (float(sum_a_list1_count_0)/float(sum_len_a_list1))**2 + (float(sum_len_a_list1-sum_a_list1_count_0)/float(sum_len_a_list1))**2
            except:
                 #Error will only occur for those values out of list_of_hundred_values which are out of range for the available values in the node
                 #As we can't split at these values as they are out of range(less than min of available node data values or greater than max), we don't need Gini for them
                 #print "error gini_a_list1 ",current_key, " sum_len_a_list1 :", sum_len_a_list1
                 pass
            try:
                 gini_a_list2 = (float(sum_a_list2_count_0)/float(sum_len_a_list2))**2 + (float(sum_len_a_list2-sum_a_list2_count_0)/float(sum_len_a_list2))**2
            except:
                 #Error will only occur for those values out of list_of_hundred_values which are out of range for the available values in the node
                 #As we can't split at these values as they are out of range(less than min of available node data values or greater than max), we don't need Gini for them
                 #print "sum_a_list1_count_0 :",sum_a_list1_count_0,"sum_len_a_list1 :", sum_len_a_list1,"sum_a_list2_count_0 :",sum_a_list2_count_0,"sum_len_a_list2 :", sum_len_a_list2,
                 #print "error gini_a_list2 ",current_key, " sum_len_a_list2 :", sum_len_a_list2
                 pass          
            if (sum_len_a_list1 != 0) & (sum_len_a_list2 != 0):
                Gini=(sum_len_a_list1*gini_a_list1+sum_len_a_list2*gini_a_list2)/(sum_len_a_list1+sum_len_a_list2)
                list_of_split_Gini_tuple.append([current_key,Gini])
                #print current_key, sum_len_a_list1, sum_a_list1_count_0, sum_len_a_list2, sum_a_list2_count_0, " Gini ", Gini, " list_of_split_Gini_tuple ", list_of_split_Gini_tuple
            #print "current_key:", current_key
            #print "code block4"
        elif current_key.count('#') == 1:
            #http://stackoverflow.com/questions/3749512/python-group-by
            sortkeyfn = key=lambda s:s[0]
            list_of_three_tuple.sort(key=sortkeyfn)
            #print "list_of_three_tuple",list_of_three_tuple            
            #http://code.activestate.com/recipes/304162-summary-reports-using-itertoolsgroupby/       
            list_of_first_and_sum_of_second_from_tuple=[]
            for k, group in groupby(list_of_three_tuple,key=itemgetter(0)):
                list_of_first_and_sum_of_second_from_tuple.append([k,sum(int(row[1]) for row in group)])
            list_of_first_and_sum_of_third_from_tuple=[]
            for k, group in groupby(list_of_three_tuple,key=itemgetter(0)):
                list_of_first_and_sum_of_third_from_tuple.append([k,sum(int(row[2]) for row in group)])
            list_of_first_as_group_and_sumofsecond_sumofthird_from_tuple=[]
            for iterator_on_list in zip(list_of_first_and_sum_of_second_from_tuple,list_of_first_and_sum_of_third_from_tuple):
                list_of_first_as_group_and_sumofsecond_sumofthird_from_tuple.append([iterator_on_list[0][0],iterator_on_list[0][1],iterator_on_list[1][1]])
            #print "list_of_first_as_group_and_sumofsecond_sumofthird_from_tuple", list_of_first_as_group_and_sumofsecond_sumofthird_from_tuple
            #Run Breiman algorithm to get order of increasing P(Y=0) (equivalent to decreasing P(Y=1))
            #https://wiki.python.org/moin/HowTo/Sorting#Sorting_Basics  <- Complex list object sorting
            sorted_list_of_first_as_group_and_sumofsecond_sumofthird_from_tuple = sorted(list_of_first_as_group_and_sumofsecond_sumofthird_from_tuple, key=lambda student:(float(student[2])/float(student[1])))
            #Find the Gini coefficient for subsequences in order
            Max_Gini_for_the_categorical_column=None
            Max_Split_for_the_categorical_column=None
            for i in range(0,len(sorted_list_of_first_as_group_and_sumofsecond_sumofthird_from_tuple)):
                sum_a_list1_count_0=0
                sum_len_a_list1=0
                sum_a_list2_count_0=0
                sum_len_a_list2=0
                for j in range(0,i+1):
                    sum_len_a_list1=sum_len_a_list1+sorted_list_of_first_as_group_and_sumofsecond_sumofthird_from_tuple[j][1]
                    sum_a_list1_count_0=sum_a_list1_count_0+sorted_list_of_first_as_group_and_sumofsecond_sumofthird_from_tuple[j][2]
                for j in range(i+1,len(sorted_list_of_first_as_group_and_sumofsecond_sumofthird_from_tuple)):
                    sum_len_a_list2=sum_len_a_list2+sorted_list_of_first_as_group_and_sumofsecond_sumofthird_from_tuple[j][1]
                    sum_a_list2_count_0=sum_a_list2_count_0+sorted_list_of_first_as_group_and_sumofsecond_sumofthird_from_tuple[j][2]
                try:
                    gini_a_list1 = (float(sum_a_list1_count_0)/float(sum_len_a_list1))**2 + (float(sum_len_a_list1-sum_a_list1_count_0)/float(sum_len_a_list1))**2
                except:
                    pass
                try:
                    gini_a_list2 = (float(sum_a_list2_count_0)/float(sum_len_a_list2))**2 + (float(sum_len_a_list2-sum_a_list2_count_0)/float(sum_len_a_list2))**2
                except:
                    pass
                if (sum_len_a_list1 != 0) & (sum_len_a_list2 != 0):
                    Gini=(sum_len_a_list1*gini_a_list1+sum_len_a_list2*gini_a_list2)/(sum_len_a_list1+sum_len_a_list2)
                    if Gini>Max_Gini_for_the_categorical_column:
                        Max_Gini_for_the_categorical_column=Gini
                        Max_Split_for_the_categorical_column=sorted_list_of_first_as_group_and_sumofsecond_sumofthird_from_tuple[0:i+1]+["split point"]+sorted_list_of_first_as_group_and_sumofsecond_sumofthird_from_tuple[(i+1):len(sorted_list_of_first_as_group_and_sumofsecond_sumofthird_from_tuple)]
                        #print current_key, sum_len_a_list1, sum_a_list1_count_0, sum_len_a_list2, sum_a_list2_count_0, " Gini ", Gini
            #As the key of categorical key is just column name and does not contain split, need to concatenate full ordered sequence with key name along with "split point" keyword to signify the splitting point
            list_of_split_Gini_tuple.append([current_key+"#"+str(Max_Split_for_the_categorical_column),Max_Gini_for_the_categorical_column])
            #print current_key, "sorted_list_of_first_as_group_and_sumofsecond_sumofthird_from_tuple :", sorted_list_of_first_as_group_and_sumofsecond_sumofthird_from_tuple, " list_of_split_Gini_tuple ", list_of_split_Gini_tuple
            #print "current_key:", current_key
            #print "code block4"
        else:
            pass
    #Printing list_of_split_Gini_tuple
    print "list_of_split_Gini_tuple :",list_of_split_Gini_tuple

main()
        
