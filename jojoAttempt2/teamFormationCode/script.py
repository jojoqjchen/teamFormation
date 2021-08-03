import pandas as pd
import numpy as np
import random

def team_formation_tool(data, columns, answers, team_size, isCsv = False):
    # Initialization

    if isCsv: ## Needed for the jupyter notebook
        pp = pd.read_csv(data)# people, pp-mg-sum21.csv
        ppcol = list(pp.columns)
    else:
        pp = pd.DataFrame(data = data, columns = columns)
        ppcol = columns
        #print(pp.info())

    # Set up for matching and build ppreport, a report table

    p = range(len(pp))
    pc = list(p)

    #useful_indexes = [i for i in range(len(answers)) if answers[i]!='3']
    similar_indexes = [i for i in range(len(answers)) if answers[i]=='1']
    different_indexes = [i for i in range(len(answers)) if answers[i]=='2']


    ### NOTE: ppc would take into account only the columns that are not "ignored" by the user!
    ppc_different = pp[[ppcol[i] for i in different_indexes]].copy(deep=True)
    ppc_different = ppc_different.astype(int) # IMPORTANT - BY DEFAULT, ALL COLUMNS ARE 'OBJECTS' (AT LEAST IF READ FROM CSV/EXCEL)
    ppc_similar = pp[[ppcol[i] for i in similar_indexes]].copy(deep=True)
    ppc_similar = ppc_similar.astype(int) # IMPORTANT - BY DEFAULT, ALL COLUMNS ARE 'OBJECTS' (AT LEAST IF READ FROM CSV/EXCEL)

    
    N = len(pp)
    S = int(np.ceil(N/team_size)) # S is number of teams to be created, approx N/m

    ppreport = pp.copy(deep=True) #deep copy,pp is unchanged
    ppreport['Team']='TBA'

    #prjmat is the intended list of project team
    prjmat = [[] for i in range(S)]
    
    sample = random.sample(range(1,N),S) # Drawing S random students without replacement
    
    # Adding students to team iteratively
    for idx, student in enumerate(sample):
    #for student in range(S):
        prjmat[idx].append(student)
        pc.remove(student)

    ## Add element to team i starting with 0 to S-1, and repeat
    i=0

    while len(pc)!=0:

        mcor = 1000000.0 # a large number
        minj = -1

        for j in pc:
            prjcopy = prjmat[i].copy()
            prjcopy.append(j)
            # Different score
            tmp_different = ppc_different.iloc[prjcopy]
            ccor_different = tmp_different.transpose().corr().sum().sum() #current correlation mattrix sum
            
            # Similar score
            tmp_similar = ppc_similar.iloc[prjcopy]
            ccor_similar = tmp_similar.transpose().corr().sum().sum()
            
            score = ccor_different - ccor_similar
            
            if score < mcor:
                mcor = score
                minj = j

        # After loop of all pc
        if minj != -1:
            pc.remove(minj)   # then add to prjmat[i]
            prjmat[i].append(minj)

        i=i+1
        if i==S: i=0

    # Add team number to ppreport

    k=0
    for i in range(S):
        for j in range(len(prjmat[i])):
            ppreport.at[prjmat[i][j], 'Team'] = i #prjmat[i][j]
            k=k+1
    ppreport = ppreport.sort_values('Team',ascending=True)

    return ppreport
