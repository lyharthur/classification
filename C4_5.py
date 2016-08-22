import math
import argparse
import csv


class Node:
    """
    C45的决策树结点，每个结点需要包含以下信息：
    1. 这个结点可以使用哪些属性来分裂；
    2. 这个结点的子树包含了哪些样例；
    3. 这个结点本身是由父结点的哪个属性分裂来的，它的属性值是什么。
    """
    def __init__(self, select_row, attribute, parent_a, value):
        self.sample = select_row
        self.attribute = attribute
        self.parent_attr = parent_a
        self.value = value
        self.child = []


class Tree:
    """
    C45的决策树，有一个分裂函数，一个构造函数。
    分裂函数的参数是一个结点，这个结点要求至少有两个属性和，它计算出每一个可用属性的增益，用最高的属性进行分裂，
    构造子节点。
    构造函数，从根节点开始，除非classify出来的字典只有一个元素，或者已经没有属性
    可以用来分裂了。
    """

    def __init__(self, data):
        self.matrix = data
        self.row = len(data)
        self.col = len(data[0])
        self.root = Node(list(range(self.row)), list(range(self.col - 1)), self.col, 'root')
        self.build(self.root)

    def split(self, node):
        gain_max = 0
        gain_max_attr = 0
        gain_max_dict = {}
        res = []
        if len(node.attribute) == 0:
            return res
        for attr in node.attribute:
            t = self.entropy(node.sample)
            if t == 0:
                return res
            d = self.classify(node.sample, attr)
            c = self.conditional_entropy(node.sample, d)
            if c[1] != 0:
                c_e = (t - c[0]) / c[1]
            else:
                c_e = 0
            if c_e > gain_max:
                gain_max = c_e
                gain_max_attr = attr
                gain_max_dict = d
        used_attr = node.attribute[:]
        
        try:
            used_attr.remove(gain_max_attr)
        except ValueError:
            pass
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
            entropy_s += -(sample[k] / len(index_list)) * math.log2(sample[k] / len(index_list))
        return entropy_s

    def classify(self, select_row, column):
        res = {}
        for index in select_row:
            key = self.matrix[index][column]
            if key in res:
                res[key].append(index)
            else:
                res[key] = [index]
        return res

    def conditional_entropy(self, select_row, d):
        c_e = 0
        total = len(select_row)
        spilt_info = 0
        for k in d:
            c_e += (len(d[k]) / total) * self.entropy(d[k])
            spilt_info += -(len(d[k]) / total) * math.log2((len(d[k]) / total))
        return (c_e, spilt_info)

    def build(self, root):
        child = self.split(root)
        root.child = child
        if len(child) != 0:
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
            #print('  '*lv +self.matrix[root.sample[0]][self.col - 1])
            o.write('  '*lv +self.matrix[root.sample[0]][self.col - 1]+'\n')
            #self.matrix[root.sample[0]],
            #print(self.root.value) #, self.matrix[root.sample[0]]



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
                        #print(node.value,dataline)
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
        print('match: ' + str(match) + ' not match : ' + str(notmatch) + ' unknown : ' + str(unknown))


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
            
            if int(row['age']) < 45:#row['age']
                o.write('~40'+'\t')
            elif int(row['age'])>= 45 and int(row['age']) < 80:
                o.write('40~80'+'\t')
            else:
                o.write('80~'+'\t')
                
            if int(row['year_income']) <= 20000:#row['year_income']
                o.write('low_income'+'\t')
            elif int(row['year_income'])> 20000 and int(row['year_income']) >= 100000:
                o.write('mid_income'+'\t')
            else:
                o.write('high_income'+'\t')

            
            o.write(row['gender']+'\t')
            o.write(row['marital_status']+'\t')

##            o.write(row['total_children']+'\t')
##            o.write(row['num_children_at_home']+'\t')
            
            if int(row['total_children']) <=5 :
                o.write('total_children_low'+'\t')
            else:
                o.write('total_children_high'+'\t')
                
            if int(row['num_children_at_home']) <=2 :
                o.write('at_home_low'+'\t')
            else:
                o.write('at_home_high'+'\t')

            
            o.write(row['education']+'\t') 
            o.write(row['member_card']+'\n')#target
        
        if count > 10281*0.70:
            train_test(test)
            #train_test(train)
        else:    
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
    C45tree.output('tree.txt')
    C45tree.test(C45tree.root,"test.txt")

    print('done')
