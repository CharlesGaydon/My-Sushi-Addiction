import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from copy import deepcopy
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.ticker as ticker
import matplotlib.colors as mc


## Workd based on this article : 
## https://biblio.ugent.be/publication/8519644/file/8519856.pdf




def fill_PM_with_row(PM, row, l, w):
    """ Fill a preference matrix (PM) by the ranks of a row
    Input : 
        - PM : is a (w,w) (w = nb of items ranked) numpy array filled of zeros 
        - row : the rankings of a subject to take into account
        - l, w : length and w of the dataset at end. l is useless here anc could be removed.
    """
    for i in np.arange(w):
        for j in np.arange(w):
#                 print(i,j, row, PM.shape)
            PM[i,j]+=np.sign(row[i]-row[j])
    return(PM)
    
def compute_PM(ranks):
    """ Compute a preference matrix from the ranks.
    Input :
        - ranks : a (n,w) numpy array.
            Each line represents the ranks given by the subject
            Value (i,j) is the rank given by subject i (relative to this array) to item j. 
            Ranks should be integer between 1 and w (= nb of items) 
    """
    l,w = ranks.shape
#     print(l,w)
    if l==0:
        return(None)
    PM = np.zeros((w,w))
    np.apply_along_axis(lambda row : fill_PM_with_row(PM, row, l, w),1, ranks)
    PM/= float(l)
    return(PM)

# N : 
def compute_PM_score(ranks,globalPM, N, method = "Norm"):
    """ Get the exceptionality score by comparing a subgroup PM to the global PM
    Inputs :
        - ranks : a (n,w) numpy array.
            Each line represents the ranks given by the subject
            Value (i,j) is the rank given by subject i (relative to this array) to item j. 
            Ranks should be integer between 1 and w (= nb of items)
        - globalPM : the (w,w) PM of the global dataset
        - N : number of lines (subjects) of the global dataset
        - method : if we use the Frobenius norm ("Norm") or not to compute the score.
    """
    PM = compute_PM(ranks)
    
    #if subgroup is empty, return score=0
    if PM is None :
            return(0.0)
        
    if method == "Norm":
        # Frobenius norm of the difference
        criteria = np.linalg.norm(PM-globalPM,ord='fro')
    else:
        #TODO
        pass

    # weighted by sqrt(size of the subgroup)
    return(criteria*np.sqrt(ranks.shape[0]/float(N)))
    

# To visualise the preference matrix in a nice way
def display_PM(PM, items_names):
    """ Plot the PM as a heatmat and the sum over its rows in a barplot
    Inputs :
        - PM : a (w,w) numpy array of the PM
        - items_names : a list of w names of the items, in order of the dataset columns.
    """
    # PREFERENCE MATRIX
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    cax = ax.matshow(PM, cmap='seismic')
    fig.colorbar(cax)
    ax.set_xticklabels([''] + items_names, rotation=90)
    ax.set_yticklabels([''] + items_names)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(1))
    plt.show()

    # BARPLOT OF PREFERENCES
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    w = PM.sum(axis=1)
    norm01 = mc.Normalize(vmin=min(w),vmax=max(w))
    plt.barh(list(range(10)),w, tick_label = items_names,color = cm.seismic(norm01(w)))
    plt.title("Barplot of preferences")
    plt.show()
    
def display_best_PM(beam, Udata, Rdata, items_names, n=1, relative = False):
    """ Display PMs associated with the n best subgroups found.
    Input : 
        - beam : the list of best rules, in ascending order based on their score (i.e. -1 el is best)
        - Udata : a (n,p) pandas DataFrame, each line represents a subject
        - Rdata : a (n,w) pandas DataFrame, each line represents the ranks given by the subject
            value (i,j) is the rank given by subject i to item j. 
            Ranks should be integer between 1 and w (= nb of items)
        -  items_names : a list of w names of the items, in order of the dataset columns.
            Should actually be equal to Rdata.columns.tolist()
        - n=1 : number of PM to show
        - relative : if False, the PM of the subgroup are shown.
            If True, the difference between the global PM and the subgroup PM is shown.
    """
    assert n<=len(beam)
    for i in np.arange(n):
        print("PM #"+str(i)+" is obtained with rule : ")
        rule = beam[-(i+1)]
        print(rule.__str__() + " and score :" + str(rule.score))
        ranks = rule.get_subset(Udata,Rdata)
        PM = compute_PM(ranks)
        if relative:
            print("PM differences are as follow :")
            final = (1.0/2)*(compute_PM(Rdata.values)-PM)
            display_PM(final,items_names)
            #(division by 2 limits the distance to the interval [1; 1]
        else:
            print("PM is :")
            final = PM
            display_PM(final,items_names)
    

#############################################
## Some helper function for the sushi dataset
#############################################

def transform_ranks(x):
    """ Turn the sushi dataset ranks of set A (w = 10 sushis ranked) to conform
    to the format where value (i,j) is the rank given by subject i to item j.
    NOte : ranks go from 1 to 10, 1 being the best, for a normal human interpretation.
    """
    y = np.zeros_like(x)
    for rank, ID in enumerate(x):
        y[ID] = rank+1
    return(y)