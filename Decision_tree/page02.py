from math import log


def xiannonEnt(dataset):
    """
    计算一个数据集的香浓的熵
    :return: None
    """
    #思路：标签的个数为sum，所有种类为n,每一种类所有标签的个数为sum(n)
    #香浓的的熵 = -(sum(n0)/sum)log(sum(n0)/sum)-(sum(n1)/sum)log(sum(n1)/sum)....(sum(ni)/sum)log(sum(ni)/sum)
    xiannon = 0
    #数据集标签的总个数
    sum = len(dataset)
    #用字典将标签名和数量存放起来
    dic = {}
    for i in dataset:
        label = i[-1]
        if label not in dic.keys():
            dic[label] = 1
        else:
            dic[label] += 1
    #计算每一个标签在总的标签中的占比
    for key in dic:
        rate = float(dic[key]/sum)
        xiannon -= rate*log(rate,2)
    return xiannon

def split_dataset(dataset,axis,value):
    """
    划分数据集（根据某一个特征的某一个值进行数据集的划分）
    :return:
    """
    splited_dataset = []
    for i in dataset:
        if i[axis] == value:
            temp = i[:axis]
            temp.extend(i[axis+1:])
            splited_dataset.append(temp)
    return splited_dataset

def marjority(classlist):
    """
    多数表决方法
    :return:
    """
    temp = {}
    for i in classlist:
        if i not in temp.keys():
            temp[i] = 1
        else:
            temp[i] += 1
    return max(temp)

def choose_best_feature_tosplit(dataset):
    """
    选择最好的数据库的划分方式（也就是计算不同的特征对于香浓熵的减少程度）
    :return:None
    """
    #最优的划分特征值
    best_feature = -1
    #最大的信息增益
    best_xinxizengyi = 0.0
    #先计算数据集的香浓熵
    xianno = xiannonEnt(dataset)
    #计算特征的个数
    feature_len = len(dataset[0]) - 1
    #循环特征并计算信息增益
    for i in range(feature_len):
        #获取第i个特征的种类(未去重)
        featlist = (temp[i] for temp in dataset)
        #去重
        featlist = set(featlist)
        sub_xiannon = 0.0
        for j in featlist:
            sub_dataset = split_dataset(dataset,i,j)
            #该特征某一种类的占比
            rate = len(sub_dataset)/float(len(dataset))
            #将该特征所有种类的信息增益累加在一起
            sub_xiannon += xiannonEnt(sub_dataset)
        xinxizengyi = xianno - sub_xiannon
        if best_xinxizengyi < xinxizengyi:
            best_xinxizengyi = xinxizengyi
            best_feature = i
    return best_feature

def create_tree(dataset,labels):
    """
    创建决策树（注意：所有属性值用完的情况下 还可能没有分完就需要进行选举）
    :return:None
    """
    #如果所有的标签值一样 则不需要划分
    classlist = [i[-1] for i in dataset]
    if classlist.count(classlist[0]) == len(classlist):
        return classlist[0]
    # 所有特征已经用完
    if len(dataset[0]) == 1:
        marjority(classlist)
    #获取划分的最佳特征
    best_feature = choose_best_feature_tosplit(dataset)
    best_feature_label = labels[best_feature]
    #构建树
    tree = {labels[best_feature]:{}}
    #删除标签
    del(labels[best_feature])
    #划分结果子集 调用递归函数
    temp = set(i[best_feature] for i in dataset)
    for i in temp:
        sub_labels = labels
        sub_dataset = split_dataset(dataset,best_feature,i)
        tree[best_feature_label][i] = create_tree(sub_dataset,sub_labels)
    return tree

def classify(tree,testVec):
    """
    使用决策树进行数据的分类
    :return:
    """
    #对树进行遍历

if __name__ == '__main__':
    dataset = [[1,1,'yes'],[1,1,'yes'],[1,0,'no'],[0,1,'no'],[0,1,'no']]
    labels = ['no surfaceing', 'flippers']
    tree = create_tree(dataset,labels)
    print(tree)