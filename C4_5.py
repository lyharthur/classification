import math
import argparse
import csv
import time
from collections import defaultdict


class Node:
    """
    C45 Tree node's attribute ：
    1. use which attribute
    2. subTree has which attribute
    3. parent attribute
    """
    def __init__(self, select_row, attribute, parent_a, value):
        self.sample = select_row
        self.attribute = attribute
        self.parent_attr = parent_a
        self.value = value
        self.child = []


class Tree:
    """
    C45 Tree
    built
    split info 
    entropy ,condtion entropy ,gain
    Test
    output,print Tree
    
    """

    def __init__(self, data):
        self.matrix = data
        self.row = len(data)
        self.col = len(data[0])
        self.root = Node(list(range(self.row)), list(range(self.col - 1)), self.col, 'root')
        self.build(self.root) # build tree

    def split(self, node):
        gain_max = 0
        gain_max_attr = 0
        gain_max_dict = {}
        res = []
        if len(node.attribute) == 0:
            return res
        for attr in node.attribute:
            e_s = self.entropy(node.sample)
            #print(e_s,attr)
            
            if e_s == 0:
                return res
            
            d = self.classify(node.sample, attr) #attribute classify  ;return dict
            c = self.conditional_entropy(node.sample, d)
            
            if c[1] != 0 :   ## HERE!
                gain_ratio = (e_s - c[0]) / c[1] #Gain_ratio = (Entropy - condition Entropy) / split info
                #print(attr ,(e_s ,c[0]),(e_s - c[0]) , c[1],gain_ratio,gain_max)
                if gain_ratio >= gain_max  :
                    gain_max = gain_ratio
                    gain_max_attr = attr
                    gain_max_dict = d
            else:
                #print(attr,'max')
                gain_max_attr = attr
                gain_max_dict = d
                break

        used_attr = node.attribute[:]
        #print(used_attr,gain_max_attr)
        used_attr.remove(gain_max_attr)
        
        for (k, v) in gain_max_dict.items():
            res.append(Node(v, used_attr, gain_max_attr, k))
        return res

    def entropy(self, index_list):
        """
        caculate entropy
        :param index_list: list类型，index of list。
        :return: entropy。
        """
        sample = {}
        for index in index_list:
            key = self.matrix[index][self.col - 1]
            if key in sample:
                sample[key] += 1
            else:
                sample[key] = 1
        entropy_s = 0
        for k in sample:
            #print(sample,sample[k],k,len(index_list))
            entropy_s += -(sample[k] / len(index_list)) * math.log2(sample[k] / len(index_list))
        #print(entropy_s,'in_e')
        return entropy_s
    
    def conditional_entropy(self, select_row, d):
        info = 0
        total = len(select_row)
        split_info = 0
        #print(total)
        count = 0
        for k in d:
            info += (len(d[k]) / total) * self.entropy(d[k])
            if len(d[k]) == 1:
                count += 1
            #print('rr',len(d[k]))
            if count == 10:
                return (0,100)
            split_info += -(len(d[k]) / total) * math.log2((len(d[k]) / total))
        return (info, split_info)
    
    def classify(self, select_row, column):
        res = {}
        for index in select_row:
            key = self.matrix[index][column]
            if key in res:
                res[key].append(index)
            else:
                res[key] = [index]
        return res



    def build(self, root): # build
        child = self.split(root)
        root.child = child
        #print(root.value)
        if len(child) != 0  :
            for i in child:
                self.build(i)

    def output(self ,filename):
        o = open(filename,'w')
        #print(self.root.value)
        o.write(self.root.value+'\n')
        self.printTree(self.root,1,o)

        
    def printTree(self, root,lv,o):
        #print(root.value)
        if root.child:
            for node in root.child:
                #print(node.value)  
                #print('  '*lv + node.value)
                o.write('  '*lv + node.value+'\n')
                self.printTree(node,lv+1,o)
        else:
            #print('  '*lv + )
            d = defaultdict(int)
            for i in range(len(root.sample)) :         
                #print(root.sample)
                #print(self.matrix[root.sample[i]])
                d[self.matrix[root.sample[i]][-1]] += 1
            #print(d)    
            #print(max(d.keys(), key=lambda k: d[k]))
            self.matrix[root.sample[0]][self.col - 1] = max(d.keys(), key=lambda k: d[k])
            o.write('  '*lv + max(d.keys(), key=lambda k: d[k])+'\n')
            #print(self.matrix[root.sample[0]][-1])
            #self.matrix[root.sample[0]],
            #print(self.root.value) #, self.matrix[root.sample[0]]


    def purning(self,root):
        if root.child:
            a = []
            k = ''
            for node in root.child :
                k =  self.purning(node)
                if k != None :
                    a.append(k) 
            if self.all_same(a) and len(a) > 1:
                #print(a)
                #print(root.parent_attr)
                root.child = None
                return k
            elif len(a) == 1:
                return k
        else:
            return self.matrix[root.sample[0]][self.col - 1]

    
    def all_same(self,items):
        return all(x == items[0] for x in items)
        
    

    def test(self,root,filename):
        test = open(filename,'r')
        match = 0
        notmatch = 0
        unknown = 0
        for line in test:
            line = line.replace('\n','')    
            dataline = line.split('\t')
            def check_node(root,dataline):
                if root.child:
                    for node in root.child:
                        #print(root.child)
                        if node.value in dataline:
                           return check_node(node,dataline)                    
                else:
                    if self.matrix[root.sample[0]][self.col - 1] == dataline[-1]:
                        #print(dataline[-1])
                        return 0
                    else:
                        #print('wrong', self.matrix[root.sample[0]][self.col - 1],dataline[-1])
                        return 1
            
            i = check_node(self.root,dataline)
            if i == 0:
                match += 1
            elif i == 1:
                notmatch += 1
            else :
                unknown += 1
        print('match: ' + str(match) + ', not match : ' + str(notmatch) + ' unknown : ' + str(unknown))
        print('Acc: '+str(match/(match+notmatch+unknown)))


if __name__ == '__main__':

    f = open('CUSTOMER.txt', 'r')
    train = open('train.txt','w')
    test = open('test.txt','w')
    n = open('format.txt','w')
    
    count = 0
    for row in csv.DictReader(f):
        count += 1
        def train_test(o):
            #o.write(row['customer_id']+'\t')
            #o.write(row['city']+'\t')
            #o.write(row['state_province']+'\t')
            #o.write(row['country']+'\t')
            #o.write(row['customer_region_id']+'\t')
            
            
            #o.write(row['age']+'\t')
            #o.write(row['year_income']+'\t')
            
            if int(row['age']) < 40:#row['age']
                o.write('age_young'+'\t')
            else:
                o.write('age_old'+'\t')
                
            if int(row['year_income']) <= 20000:#row['year_income']
                o.write('low_income'+'\t')
            else:
                o.write('high_income'+'\t')

            
            o.write('sex'+row['gender']+'\t')
            o.write(row['marital_status']+'\t')

            #o.write('t'+row['total_children']+'\t')
            #o.write('h'+row['num_children_at_home']+'\t')
            #o.write(row['education']+'\t')
            
            if int(row['total_children']) <= 4 :
                o.write('total_children_low'+'\t')
            else:
                o.write('total_children_high'+'\t')
                
            if int(row['num_children_at_home']) <=2 :
                o.write('at_home_low'+'\t')
            else:
                o.write('at_home_high'+'\t')
            
            if row['education'] == 'Partial High School' or row['education'] == 'High School Degree' or row['education'] == 'Partial College':
                o.write('non_college'+'\t')
            else:
                o.write('college'+'\t')
                
            o.write(row['member_card']+'\n')#target
            
        
        if count > 10281*0.7:
            train_test(test)
            #train_test(train)
        else:
            #train_test(test)
            train_test(train)
            
            
        n.write(row["customer_id"]+'\t'+row["account_num"]+'\t'+
                row["lname"]+'\t'+row["fname"]+'\t'+row["address"]+'\t'+row["city"]+'\t'+row["state_province"]+'\t'+
                row["postal_code"]+'\t'+row["country"]+'\t'+row["customer_region_id"]+'\t'+row["phone"]+'\t'+
                row["marital_status"]+'\t'+row["gender"]+'\t'+row["total_children"]+'\t'+row["num_children_at_home"]+'\t'+
                row["education"]+'\t'+row["member_card"]+'\t'+row["age"]+'\t'+row["year_income"]+'\n')
    
    train.close()
    test.close()
    f.close()
    n.close()
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', dest='data', type=argparse.FileType('r'), default="train.txt")
    args = parser.parse_args()
    matrix = []
    lines = args.data.readlines()
    for line in lines:
        line = line.replace('\n','')
        matrix.append(line.split('\t'))
    
    C45tree = Tree(matrix) #build tree
    C45tree.output('tree_nonPurn.txt')
    #C45tree.test(C45tree.root,"test.txt")
    C45tree.purning(C45tree.root)
    C45tree.test(C45tree.root,"test.txt")
    C45tree.output('tree_Purn.txt')
    
    print('done')
