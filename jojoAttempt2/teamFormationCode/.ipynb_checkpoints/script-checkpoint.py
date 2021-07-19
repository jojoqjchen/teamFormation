import pandas as pd
import numpy as np

def team_formation_tool(data, columns, useful_indexes, team_size, isCsv = False):
    # Initialization
    
    if isCsv: ## Needed for the jupyter notebook
        pp = pd.read_csv(data)# people, pp-mg-sum21.csv
        ppcol = list(pp.columns)
    else: 
        pp = pd.DataFrame(data = data, columns = columns)
        ppcol = columns
    
    # Set up for matching and build ppreport, a report table

    p = range(len(pp))
    pc = list(p)
    
    ### NOTE: ppc would take into account only the columns that are not "ignored" by the user! 
    ppc = pp[[ppcol[i] for i in useful_indexes]].copy(deep=True)

    N = len(pp)

    S = int(np.ceil(N/team_size)) # S is number of teams to be created, approx N/m

    ppreport = pp.copy(deep=True) #deep copy,pp is unchanged
    ppreport['Team']='TBA'
    #ppreport['Similarity']=np.nan
    
    
    #prjmat =[] #intended list of project team
    prjmat =[]
    for s in range(int(S)): 
        prjmat.append([])
        
    # Adding students to team iteratively
    
    for s in range(S):
        prjmat[s].append(s)
        pc.remove(s)

    ## Add element to team i starting with 0 to S-1, and repeat
    i=0

    while len(pc)!=0:

        mcor = 1000000.0 # a large number
        minj = -1

        for j in pc:
            prjcopy = prjmat[i].copy()
            prjcopy.append(j)
            tmp = ppc.iloc[prjcopy]
            ccor = tmp.transpose().corr().sum().sum() #current correlation mattrix sum
            if ccor < mcor:
                mcor = ccor
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
    
    return ppreport