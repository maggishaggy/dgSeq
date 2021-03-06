# This function extract features for all the genes in AllGene
import numpy as np

def GetFeature(G1, G2, AllGene, AllLength):
    X = np.zeros((AllLength,5))
    for k in range(AllLength):
        node = AllGene[k]
        one = 0
        zero = 0
        neighbor = G1.neighbors(node)
        for nei in neighbor:
            if G1.node[nei]['label'] == 1:
                one+=1
            elif G1.node[nei]['label'] == 0:
                zero+=1
        X[k][0] = 1
        X[k][1] = zero
        X[k][2] = one
        one = 0
        zero = 0
        neighbor = G2.neighbors(node)
        for nei in neighbor:
            if G2.node[nei]['label'] == 1:
                one+=1
            elif G2.node[nei]['label'] == 0:
                zero+=1
        
        X[k][3] = zero
        X[k][4] = one

    return X
