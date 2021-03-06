# This program compute the AUC of dgSeq on Thyroid Cancer(TC) and output the
# average AUC value and a numpy matrix which contains the probabilities of
# all cross validation genes being disease-associated.

import numpy as np
import networkx as nx
import copy
from func_exclude_gene import ExcludeGene
from func_feature_generate import GetFeature
from func_minimum import FindMin
from func_label_graph import LabelGraph
from sklearn.metrics import roc_auc_score

fdg = open("thyroid_cancer_gene_census.tsv")
fdg.readline()
dg = []
for line in fdg:
    data = line.split('\t')
    dg.append(data[0])
fdg.close()

fnode = open("GeneList_THCA.txt")
GeneList = []
for line in fnode:
    data = line.split('\t')
    GeneList.append(data[1])
fnode.close()

#none disease gene based on shortest path in normal disease-gene network
fdgnsp = open("dgn_shortest_path_norm.txt")
dgn2norm = (fdgnsp.readline()[:-1].split('\t')[1]).split(',')
dgn3norm = (fdgnsp.readline()[:-1].split('\t')[1]).split(',')
dgn4norm = (fdgnsp.readline()[:-1].split('\t')[1]).split(',')
dgn5norm = (fdgnsp.readline()[:-1].split('\t')[1]).split(',')
fdgnsp.close()

fdgnnp = open("dgn_no_path_norm.txt")
dgnnpnorm = fdgnnp.readline()[:-1].split(',')
fdgnnp.close()

#none disease gene based on shortest path in differential network
fdgndiff = open("dgn_shortest_path_diff.txt")
dgn3diff = (fdgndiff.readline()[:-1].split('\t')[1]).split(',')
dgn4diff = (fdgndiff.readline()[:-1].split('\t')[1]).split(',')
dgn5diff = (fdgndiff.readline()[:-1].split('\t')[1]).split(',')
fdgndiff.close()

dgnnorm = dgn5norm+dgnnpnorm

# Genes not in the PPI network are removed
dgnnorm = ExcludeGene(dgnnorm,GeneList)

dgndiff = dgn4diff+dgn5diff

# Benchmark non-disease genes set
dgnpotential = list(set(dgnnorm).intersection(dgndiff))

# alldgn contains genes whose prior labels are zero
alldgn = list(set(dgnnorm).union(set(dgndiff)))

Gnorm = nx.read_gml("ppi_tc.gml.gz")
Gdiff = nx.read_gml("dif_tc.gml.gz")

Round = 100
auc100 = np.zeros(Round)
dgLength = len(dg)
prob = np.zeros(2*dgLength)
probS = np.zeros((Round,2*dgLength))
dg_tmp = copy.deepcopy(dg)
y = np.concatenate((np.ones(dgLength),np.zeros(dgLength)))
AllLength = 2*dgLength

import time
start = time.clock()

for r in range(Round):
    print(r)    
    # Randomly select len(dg) non-disease genes from benchmark set
    dgn = []
    while len(dgn) < dgLength:
        temp = np.random.choice(dgnpotential)
        if temp not in dgn:
            dgn.append(temp)
    AllGene = dg+dgn
       
    # leave one out
    for i in range(AllLength):      
        LOO = AllGene[i]
        
        # Label the graph
        if i < dgLength:
            dg_tmp.remove(LOO)
            LabelGraph(Gnorm, Gdiff, dg_tmp, alldgn)
            dg_tmp.append(LOO)
        else:
            alldgn.remove(LOO)
            LabelGraph(Gnorm, Gdiff, dg_tmp, alldgn)
            alldgn.append(LOO)
            
        # Extract feature
        X = GetFeature(Gnorm, Gdiff, AllGene, AllLength)
        indices = np.arange(2*dgLength)
        train_index = indices[np.logical_not(indices==i)]
        X_train, y_train = X[train_index], y[train_index]
        X_test = X[i]
        
        # Compute parameters
        res = FindMin(X_train,y_train)
        FW = np.dot(X_test,res.x)
        prob[i] = np.exp(FW)/(1+np.exp(FW))
     
    auc100[r] = roc_auc_score(y, prob)
    probS[r] = prob

end = time.clock()
print ('run:',(end - start)/60,'min')

#save the probabilities for drawing the ROC curve
print(np.mean(auc100))
np.save("prob_TH.npy",probS)

