# imports
import pandas as pd
import numpy as np
from copy import deepcopy


# setting a seed
np.random.seed(0)

########################
## First the two classes :
## condition and rule
########################

class condition:
    """ A condition is defined as an attribute which has a relation (i.e. =, <, >) to a value.
    """
    
    def __init__(self, first_attr, value_taken, relation):
        self.attr_name = first_attr
        self.takes_value = value_taken
        self.relation = relation

    def __str__(self):
        return("[" + self.attr_name + " " + self.relation + " " + self.takes_value+"]")


class rule:
    """ A rule is a list of conditions with some functions.
    """    
    def __init__(self, first_attr= None, first_value = None, first_relation = None, start_condition = None, start_rule = None):
        self.score = 0.0
        self.conds = []
        if start_condition != None:
            self.add(start_condition)
        elif first_attr != None and first_value!=None and first_relation!=None :
            self.add(condition(first_attr, first_value, first_relation))
        elif start_rule != None : 
            self.score = start_rule.score
            self.conds = deepcopy(start_rule.conds)
    
    
    def add(self, new_cond):
        """ Add a condition to the rule, ony if attr was not yet present
        """ 
        if new_cond.attr_name in [c.attr_name for c in self.conds]:
            return(0)
        self.conds.append(new_cond)
        return(1)
    
    def get_subset(self, Udata, Rdata):
        """ Generate the subset of ranking data from the two dataframes
        """
        attr_names = Rdata.columns
        all_data = pd.concat([Udata,Rdata],axis=1)
        for cond in self.conds:
            if cond.relation == "=":
                all_data = all_data[all_data[cond.attr_name] == cond.takes_value]
            elif cond.relation == "<":
                all_data = all_data[all_data[cond.attr_name] < cond.takes_value]
            elif cond.relation == ">":
                all_data = all_data[all_data[cond.attr_name] > cond.takes_value]
                
        return(all_data[attr_names].values)  
    
    def reorder_conds(self):
        """ For equal string representation, conds should have a fixed order when added (ex : based on attr names)
        """
        #TODO
        pass
    
    def __str__(self):
        out = [cond.__str__() for cond in self.conds]
        return(" & ".join(out))
    

########################################################################
## Then some helper functions for the beam search algorithm
########################################################################

def reorder(rules):
    """ Set in ascending order a list of rules, based on their score.
    """
    return(sorted(rules, key = lambda x : x.score))

def naive_score_function(ranks):
    """ A naive default score function for the subset discovery
        (for dev purposes)
    """
    return(np.std(ranks[:,0]))

def beam_search(Udata, Rdata, beam_width, max_iter = 50,verbose = False, score_function = naive_score_function):
    """ Run the beam search algo to find subgroups of high score
    Input :
        - Udata : a (n,p) pandas DataFrame, each line represents a subject.
            The conditions/rules are derived from thos values, which should be ordered strings of integer.
            Ex : age    0:15-19  1:20-29   2:30-39   3:40-49   4:50-59    5:60-
                    should be coded as follow :
                 age     "0"   "1"   "2"   "3"   "4"   "5"
            The relations between an attribute and a value are :
             equality (=), superiority (>) or inferiority (<).
        - Rdata : a (n,w) pandas DataFrame, each line represents the ranks given by the subject
            value (i,j) is the rank given by subject i to item j. 
            Ranks should be integer between 1 and w (= nb of items)
        - beam_width : the size of the set of condition to update
        - max_iter : iterations stop at max_iter OR before when there is no change in the beam
        - verbose : set to True to display intermediate results and beam.
        - score_function : receives a (n',w) numpy array of ranks (n'<=n) to compute the score.
    """

    # initialisation of the different conditions to combine
    L = []
    for attr in Udata.columns : 
        uniques = np.unique(Udata[attr].values)
        for index,val in enumerate(uniques) :
            L.append(condition(attr, val, "="))
            # inf and sup cond without redundancy with equality
            if index >1 and index<(len(uniques)-2):
                L.append(condition(attr, val, "<"))
                L.append(condition(attr, val, ">"))
            
    # Initialization of the beam lists
    beam = []
    new_beam = []
    for c in range(beam_width):
        beam.append(rule())
        new_beam.append(rule())
    i = 0
    while i < max_iter:
        for r in beam : 
            # shuffling the rules for better generation. 
            # Note : this is an inplace operation.
            np.random.shuffle(L)
            for l in L:
                
                new_r = rule(start_rule = r)
                
                # exit if condition was already there
                is_actually_new = new_r.add(l)              
                if not is_actually_new:
                    break 
                    
                # exit if rule was already found
                is_not_yet_in_new_beam = (new_r.__str__() not in [b.__str__() for b in new_beam])
                if not is_not_yet_in_new_beam:
                    break
                    
                # generate subset and compute score    
                Rsubset = new_r.get_subset(Udata, Rdata)
                new_score = score_function(Rsubset)
                
                if verbose:
                    print(new_r.__str__(), "->",round(new_score,2))
                
                # update new beam if new score is better than the worst of new beam
                if new_score > new_beam[0].score:
                    new_r.score = new_score
                    new_beam[0] = new_r
                    new_beam = reorder(new_beam)
                    if verbose:
                        print("new beam =", [b.__str__() for b in new_beam])
                        
        # stop the search if no difference was made in this iteration
        if [b.__str__() for b in new_beam] == [b.__str__() for b in beam]:
            print("["+str(i)+"] BEAM =", [b.__str__() for b in beam])
            break
            
        # update the beam
        beam = deepcopy(new_beam)
        
        if verbose:
            print("["+str(i)+"] BEAM =", [b.__str__() for b in beam])
            print("-----------------------------------------")
            
        i+=1
    if not verbose :
        print("["+str(i)+"] BEAM =", [b.__str__() for b in beam])
        print("-----------------------------------------")
    return(beam, [b.__str__() for b in beam])
