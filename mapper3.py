#This is mapper which will take modelfile from distributed cache
#This has 2 sections - one for numeric and other for categorical

#!/usr/bin/env python

import collections, math, sys, json, os, random

#dataset = [[1,2,3,4,5,1,2,5,1,2],['a','b','c','d','a','a','a','b','e','b'],[10,9,8,7,6,5,4,3,2,1]]

#dataset is a list of lists. Subscript starts from 0 in python
#datacolumn is a column of dataset above and val is a value in it. So datacolumn is a list

def posfinder(datacolumn,val):
       pos_save = [] #declare empty list pos_save
       req_col = datacolumn[:] #req_col is copy of datacolumn
       num_instances = req_col.count(val) #num_instances will save number of times val appears in datacolumn
       for i in range(0,num_instances):
           pos_save.append(req_col.index(val)) #req_col.index(val) gives first occurance of val in req_col
           req_col[req_col.index(val)]='NULL' #value at index corresponding to above occurence is declared NULL
       #print(pos_save)
       return pos_save #pos_save is list of indices having value val in datacolumn

#pos_save1 = posfinder(dataset[1],'a')

#print(pos_save1)

#new_list1 = [dataset[1][i] for i in pos_save1] #it will simply have the same value val repeated the no. of times it occurs in datacolumn

#print(dataset[1])
#print(new_list1)

#http://stackoverflow.com/questions/19507714/python-list-comprehension-and-not-in
#new_list2 will have all elements of datacolumn except for val
#new_list2 = [dataset[1][i] for i in range(0,len(dataset[1])) if i not in pos_save1]

#print(dataset[1])
#print(new_list2)



#returns variance of a numeric list of numbers
#Variance measure used in PLANET paper with Breiman's categorical split theorem
#variance measure is used in regression tree probably not in classification
def variance(a_list):
      average = sum(a_list) / len(a_list)
      variance = sum((average - value) ** 2 for value in a_list)/(len(a_list)-1)
      return variance



#Gini measure used in Shih paper with Breiman's categorical split theorem
#Gini measure is used in classification tree
#https://www.uic.edu/classes/idsc/ids572cna/Decision%20Trees_1.pdf  --  Gini measure definition
def gini(a_list):
      gini = sum((float(a_list.count(0))/float(len(a_list)))**2 + (float(a_list.count(1))/float(len(a_list)))**2)
      return gini


#return [a_list1.count(0),len(a_list1),a_list2.count(0),len(a_list2)] as a list to main()
#need to modify for multiple occurences of same value by taking set, then converting to list 
#then for each element of list find the above 4 sufficient statistics
#note that a_list1 contains the value itself where split is to be made (as it is X<=s type split from PLANET paper)
#so need to add the number of times s occurs in the datacolumn to len(a_list1)

def FindBestSplitNum(min_max_for_column,datacolumn,Y):
        datacol_set=set(datacolumn)
        datacol_list=list(datacol_set)
        #http://stackoverflow.com/questions/7851077/how-to-return-index-of-a-sorted-list
        Indices_of_sorted_datacol_list = sorted(range(len(datacol_list)), key=lambda k: datacol_list[k])  #indices in sorted order of datacolumn
        datacol_list_values_sorted = [datacol_list[i] for i in Indices_of_sorted_datacol_list]
        #
        return_list=[]
        min_max_for_column=min_max_for_column.replace("'","")
        min=float(min_max_for_column.split(",")[0])
        max=float(min_max_for_column.split(",")[1])
        #min=float(min_max_for_column[0])
        #max=float(min_max_for_column[1])
        difference=(max-min)/(100-1)
        list_of_hundred_numbers=[min+i*difference for i in range(0,100)]
        #print list_of_hundred_numbers
        for split_point in list_of_hundred_numbers:
            datacol_list_values_sorted_subset1=[]
            datacol_list_values_sorted_subset2=[]
            for j in datacol_list_values_sorted:
                if float(j)<=split_point:
                    datacol_list_values_sorted_subset1.append(j)
                else:
                    datacol_list_values_sorted_subset2.append(j)
        #
            set_of_Ys_for_all_t1 = []
            set_of_Ys_for_all_t2 = []
            for t in datacol_list_values_sorted_subset1:
                positions_of_t_in_datacolumn1 = posfinder(datacolumn,t)
                Ys_for_given_t1 = [Y[i] for i in positions_of_t_in_datacolumn1]
                set_of_Ys_for_all_t1 = set_of_Ys_for_all_t1 + Ys_for_given_t1
            for t in datacol_list_values_sorted_subset2:
                positions_of_t_in_datacolumn2 = posfinder(datacolumn,t)
                Ys_for_given_t2 = [Y[i] for i in positions_of_t_in_datacolumn2]
                set_of_Ys_for_all_t2 = set_of_Ys_for_all_t2 + Ys_for_given_t2
        #
            return_list.append([split_point,len(set_of_Ys_for_all_t1),set_of_Ys_for_all_t1.count('0'),len(set_of_Ys_for_all_t2),set_of_Ys_for_all_t2.count('0')])
        return(return_list)



def FindBestSplitNum1(min_max_for_column,datacolumn,Y):
        datacol_set=set(datacolumn)
        datacol_list=list(datacol_set)
        #http://stackoverflow.com/questions/7851077/how-to-return-index-of-a-sorted-list
        Indices_of_sorted_datacol_list = sorted(range(len(datacol_list)), key=lambda k: datacol_list[k])  #indices in sorted order of datacolumn
        datacol_list_values_sorted = [datacol_list[i] for i in Indices_of_sorted_datacol_list]
        #
        return_list=[]
        #min_max_for_column=min_max_for_column.replace("'","")
        #min=float(min_max_for_column.split(",")[0])
        #max=float(min_max_for_column.split(",")[1])
        min=float(min_max_for_column[0])
        max=float(min_max_for_column[1])
        difference=(max-min)/(100-1)
        list_of_hundred_numbers=[min+i*difference for i in range(0,100)]
        datacol_list_values_sorted_subset1=[]
        datacol_list_values_sorted_subset2=[]
        set_of_Ys_for_all_t1 = []
        set_of_Ys_for_all_t2 = []
        rangestart1=0
        rangestart2=0
        for split_point in list_of_hundred_numbers:
            #datacol_list_values_sorted_subset1=[]
            #datacol_list_values_sorted_subset2=[]
            for j in range(rangestart1,len(datacol_list_values_sorted)):
                if datacol_list_values_sorted[j]<=split_point:
                    datacol_list_values_sorted_subset1.append(j)
                else:
                    datacol_list_values_sorted_subset2=datacol_list_values_sorted[j:len(datacol_list_values_sorted)]
                    rangestart1=j
                    break
        #
            #set_of_Ys_for_all_t1 = []
            #set_of_Ys_for_all_t2 = []
            for t in range(rangestart2,len(datacol_list_values_sorted_subset1)):
                positions_of_t_in_datacolumn1 = posfinder(datacolumn,datacol_list_values_sorted_subset1[t])
                Ys_for_given_t1 = [Y[i] for i in positions_of_t_in_datacolumn1]
                set_of_Ys_for_all_t1 = set_of_Ys_for_all_t1 + Ys_for_given_t1
            for t in datacol_list_values_sorted_subset2:
                positions_of_t_in_datacolumn2 = posfinder(datacolumn,t)
                Ys_for_given_t2 = [Y[i] for i in positions_of_t_in_datacolumn2]
                set_of_Ys_for_all_t2 = set_of_Ys_for_all_t2 + Ys_for_given_t2
        #
            return_list.append([split_point,len(set_of_Ys_for_all_t1),set_of_Ys_for_all_t1.count('0'),len(set_of_Ys_for_all_t2),set_of_Ys_for_all_t2.count('0')])
        return(return_list)


#PLANET paper talks about Breiman split theorem for categorical predictor in continuous dependent variable(regression tree)#
#http://www.math.ccu.edu.tw/~yshih/papers/spl.pdf Shih paper talks about Breiman split theorem for categorical predictor in categorical dependent variable(classification tree)#
#Breiman split theorem same for regression or classification tree#

def FindBestSplitCat(datacolumn,Y):
       datacol_set=set(datacolumn)
       datacol_list=list(datacol_set)
       return_list=[]
       for t in datacol_list:
           positions_of_t_in_datacolumn = posfinder(datacolumn,t)
           Ys_for_given_t = [Y[i] for i in positions_of_t_in_datacolumn]
           return_list.append([t,len(Ys_for_given_t),Ys_for_given_t.count('0')])
       return(return_list)


import collections, math, sys, json, os, random, csv

#main() reads the full data as streaming input. It also takes as input the curent node name (environment variable) which has to be split#
#It uses modelfile.txt to read the split rules for the current node which are starting from Root node itself and hence can be used on full data#
#It takes a single line (row) of data and goes over each variable one-by-one. For each variable, tt uses attributes.txt to determine if a variable#
#is numeric or character and depending upon it, it accesses modelfile.txt with variable column name as key, to get the rule and determine if the value#
#of the variable in the current line would imply that the line can stay in the node or not. Note that same variable could have been used multiple times#
#in the tree for splitting, so for each value of the variable, the check is done. The reason to check separately for numeric and character variables is that they#
#are stored differently in the modelfile.txt. Numeric variable's rules are stored as a list with all the inequalities leading up to current node.#
#Character variable's rules are stored as list of list of all sets of categories for splits(only of that particular variable) leading up to present node#
#if for any element of the numeric or character variables list from modelfile, the present line does not satisfy the condition, then it means that line#
#not part of data going into the present node. So we break the for loop and take next line as input. if all conditions for all variables are satisfied#
#then we add that line to node_data which is going to hold the data for that node out of total data streamed#. We transpose this data as subsequent functions have been written#
#to deal with column-wise data and then use it to generate sufficient statistics from this mapper#

def main():
    #with open('/home/ic10636/DecisionTree/naps_pnl_thd201201_201301.csv', 'rb') as csvfile:
        #variable names are in this sequence : ['target_variable', 'AGEOLTR2_MAG', 'AGESATTR_MAG', 'BKRBALHC_MAG', 
        #'BNKNROLD_MAG', 'BNKRBAL_MAG', 'RISKSCR_MAG', 'ZIPCODE', 'SOURCECD', 'status']
        #spamreader = csv.reader(csvfile, delimiter=',')
        #lines = [line for line in spamreader] #lines is a list of list where each field can be accessed as lines[i][j] where i is row and j is column
           #print (lines[0],lines[1])
    #f1 = open('/home/ic10636/DecisionTree/modelfile.txt', 'rb').read()
    f1 = open('modelfile.txt', 'rb').read()
    modelfile=json.loads(f1)
    #f2 = open('/home/ic10636/DecisionTree/attributes.txt', 'rb').read()
    f2 = open('attributes.txt', 'rb').read()
    attributes=json.loads(f2)
    f3 = open('min_max.txt', 'rb').read()
    min_max=json.loads(f3)
    number_of_predictors = len(attributes)
    #add a line here to see node name passed as environment variable#
    node_name = "Root"
    #Get the set of rules associated with this node name#
    node_rules=modelfile[node_name]
    #print "node_rules :", modelfile[node_name]
    node_data = []
    ###Code to subset data for the node starts here###
    #for line in lines: 
    counter_all=0 
    counter_nonmiss=0
    counter_cond=0
    for line in sys.stdin:
        line=line.strip('\n').strip('\t').split(',')
        counter_all = counter_all+1
        #print line   
        if '' in line:
            #print line
            #skiping line which has any missing value
            continue
            #continue_outer_for_loop=False
            #print line
            #print "ishan"
            #obs_row = line.split(",")
            #obs_class = obs_row[0]
            #obs_row.remove(obs_class)
            #if this line is following the set of rules associated with this node name only then save it else continue the loop#
        else:
            #print line
            #print "going in else"
            counter_nonmiss=counter_nonmiss+1
            #print "number_of_predictors:  ",number_of_predictors
            for j in range(1,number_of_predictors+1):
                if attributes["COL"+str(j)] == "numeric":
                    #print attributes["COL"+str(j)]
                    #print "COL"+str(j)+"is"+"numeric"
                    node_rules_current_col = node_rules["COL"+str(j)]
                    expression_to_evaluate = "True"
                    for rule in node_rules_current_col:
                        expression_to_evaluate=expression_to_evaluate + " and " + str(line[j])+rule 
                    #print expression_to_evaluate
                    if eval(expression_to_evaluate) == False:
                        break
                elif attributes["COL"+str(j)] == "character":
                    #print attributes["COL"+str(j)]
                    #print "COL"+str(j)+"is"+"character"
                    node_rules_current_col = node_rules["COL"+str(j)]
                    expression_to_evaluate = "True"
                    for rule in node_rules_current_col:
                        expression_to_evaluate=expression_to_evaluate + " and " + "'" + str(line[j]) + "'" + " in " + str(rule)
                    #print expression_to_evaluate
                    if eval(expression_to_evaluate) == False:
                        break
            if eval(expression_to_evaluate) == True:
                #print "eval(expression_to_evaluate) :",eval(expression_to_evaluate)
                node_data.append(line)
                counter_cond=counter_cond+1
                #print "appending"
    #print "counter_all: ",counter_all," counter_nonmiss: ",counter_nonmiss, " counter_cond: ",counter_cond
    #print node_data
    #note that each element of node_data list is one row. We need  each element to be 1 column to fit in our funcions written for our local decision tree#
    column_wise_node_data=[list(b) for b in zip(*node_data)]
    ###Code to subset data for the node ends here###
    #print column_wise_node_data
    Y=column_wise_node_data[0]
    for j in range(1,number_of_predictors+1):
        if attributes["COL"+str(j)] == "numeric":
            min_max_for_column=min_max["COL"+str(j)] #min_max_for_column automatically gets converted into tuple by python
            #print "COL", str(j), "min_max_for_column", min_max_for_column
            #print "column_wise_node_data", str(j), column_wise_node_data[j]
            #print "Y", Y
            return_list_of_list_from_function=FindBestSplitNum(min_max_for_column,column_wise_node_data[j],Y)
            for k in range(0,len(return_list_of_list_from_function)):
                key=node_name+"#"+"COL"+str(j)+"#"+str(return_list_of_list_from_function[k][0])
                value=str(return_list_of_list_from_function[k][1:5])
                print '%s\t%s' % (key, value)
        if attributes["COL"+str(j)] == "character":
            return_list_of_list_from_function=FindBestSplitCat(column_wise_node_data[j],Y)
            for k in range(0,len(return_list_of_list_from_function)):
                key=node_name+"#"+"COL"+str(j)
                value=str(return_list_of_list_from_function[k])
                print '%s\t%s' % (key, value)
if __name__ == '__main__':
    main()
