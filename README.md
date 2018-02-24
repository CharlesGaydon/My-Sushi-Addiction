# Exceptional Preference Mining (EPM) using Preference Matrix

Author : Charles Gaydon

February 2018

Context : I wanted to discover this interesting aspect of Data Science that is EPM, and ended up building this repo, which enables you to do (simultaneously or separately) Subgroup Discovery (SD) and Exceptional Preference Mining (EPM).


## Content
- **Subgroup Discovery** using a **beam search** (see more [here](http://www.cs.cmu.edu/afs/cs/project/jair/pub/volume17/gamberger02a-html/node4.html)); 

- **Subgroup selection** using a score of "Exceptional Preference", based on a **Preference Matrix** (PM) obtained from the ranking of some items. This idea is proposed by Claudio Rebelo de Sa *et al* in their article [Exceptional Preference Mining](https://biblio.ugent.be/publication/8519644/file/8519856.pdf);

- The whole method is applied to the [**Sushi preference dataset**](http://www.kamishima.net/sushi/), set A, in which 10 sushis were ranked by 5000 subjects, about whom we possess some information.


## Structure

**Files** :
- **0_Quick_Start.ipynb** : shows how to use this repository for EPM in a few easy steps;
- **1_Exceptional_Preference_Mining.ipynb** : structured as a draft, this notebook shows, step by step, how I implemented te beam search algorithm using toy data and toy score function, then implemented an EP score function, and finally applied it to the sushi dataset.
- **beam_search.py** : functions for the beam search algorithm;
- **preference_matrix.py** : functions to compute and visualise Preference Matrix, and calculate a derived exceptionality score from them.

**Directories** :
- **sushi3-2016/** : the original sushi dataset files, as well as the ones preprocessed to comply with the format requirement of my Preference Matrix algorithms.
- **toydata/** : subject and ranking toy data used to develop the beam search algorithm

## Requirements

... are minimalistic. With up any approximately up to date numpy, pandas and matplotlib version, everything should be fine.