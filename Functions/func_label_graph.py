# This function labels the PPI network (G1) and differential network (G2) according to the disease genes in dg
# and non-disease genes in dgnall. 0.01% of the remaining unknown genes are randomly labeled as 1.
import numpy as np

def LabelGraph(G1, G2, dg, dgnall):
    proRandom = np.random.uniform(0,1,G1.number_of_nodes()-len(dg)-len(dgnall))
    t = 0
    t = 0
    for node in G1.nodes_iter():
        if node in dg:
            G1.node[node]['label'] = 1
            G2.node[node]['label'] = 1
        elif node in dgnall:
            G1.node[node]['label'] = 0
            G2.node[node]['label'] = 0
        else:
            if proRandom[t] >= 0.99:
                G1.node[node]['label'] = 1
                G2.node[node]['label'] = 1
            else:
                G1.node[node]['label'] = 0
                G2.node[node]['label'] = 0
            t+=1
