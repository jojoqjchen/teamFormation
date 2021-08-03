import pandas as pd
import numpy as np
import scipy as sc
from scipy import optimize
import cvxpy as cp

def project_first_teams(data, columns, numberOfProjects, maxTeamSize, numberOfChoices = 3, isCsv = False):
    # Initialization, Reading the survey information

    if isCsv: ## Needed for the jupyter notebook
        df = pd.read_csv(data)# people, pp-mg-sum21.csv
    else:
        df = pd.DataFrame(data = data, columns = columns)

    try:
        colNames = []
        for i in range(1,int(numberOfChoices)+1):
            col = 'Choice '+str(i)
            c = df[col]
            colNames.append(col)
    except KeyError:     # NOTE: Columns must include 'Choice 1', 'Choice 2', 'Choice 3'
        raise KeyError

    # NOTE: Projects must be numbered between 1 and numberOfProjects.

    n = df.shape[0] # Number of students
    m = int(numberOfProjects) # Number of teams
    t = int(maxTeamSize) # Maximal Team size

    choices = df.loc[:,colNames].to_numpy()

    # OPTIMIZATION
    ## By default, each project for each student has a value of 100.
    ## Each of the 3 student’s favorites projects’ values will be set to 1, 2, and 3.
    ## The decision variables, Xij, are equal to 1 if the student i is assigned to the project j, 0 otherwise.
    ## CONVENTION: the vectors X (decision variable) & c (weights) dimension is n*m, i.e. numberOfStudents*numberOfProjects
    ## CONVENTION (2): c = (C11, C12,…C1m, C21,…C2m,…Cnm).
    ## CONVENTION (3) I.e., the weight of the project j for the student i will be in position m*i+j-1 (starting at 0) in c.

    ## WEIGHTS
    c_choices = np.full((n*m,1),100) # Setting all the weights to 100.

    for i in range(choices.shape[0]): # For each student: i = student number from 0 to n-1

        for k in range(choices.shape[1]): # For all the possible projects: k = choice number for the student i

            c_choices[i*m+int(choices[i,k])-1]=k+1 #

    ## CONSTRAINTS
    b_eq = np.ones((n,1)) # -> Equality constraints: each student must be assigned to 1 project
    b_ub = t*np.ones((m,1)) # -> Inequality constraints: each team must have at most t number of students assigned to it

    A_eq = np.zeros((n,n*m)) # -> Initialization
    A_ub = np.zeros((m,n*m)) # -> Initialization

    for row_eq in range(n):
        for i in range(m):
            A_eq[row_eq,row_eq*m+i]=1

    for row_ub in range(m):
        for i in range(n):
            A_ub[row_ub,row_ub+i*m]=1

    ## BOUNDS FOR THE ANSWERS
    lb, ub = 0, 1 # Lower and upper bound for the decision variables

    ## MILP Programming - Using CVXPY
    ### Documentation: https://www.cvxpy.org/index.html
    ### Inspiration: https://towardsdatascience.com/integer-programming-in-python-1cbdfa240df2
    
    x = cp.Variable((n*m,1), integer=True) # Defining variables x - integer
    
    ### OPTIMIZATION PROBLEM
    
    objective = cp.Minimize(x.T @ c_choices) # Minimize the weights of the allocations. 
    
    ### CONSTRAINTS
    
    team_size_constraint = A_ub @ x <= b_ub # Each team must have at most t participants
    assignments_constraint = A_eq @ x == b_eq # Each participant must be assigned to 1 project
    x_lb = 0<=x # Binary var
    x_ub = 1>=x # Binary var
    constraints = [team_size_constraint, assignments_constraint, x_lb, x_ub] # All constraints
    
    ### SOLVER
    
    opti_problem = cp.Problem(objective,constraints)
    opti_problem.solve(solver=cp.GLPK_MI)
    
    df['Team'] = 'TBA'
    for i in range(n): # for each student
        sub_list = x.value[i*m:(i+1)*m]
        for j in range(m): # we will search its project
            if sub_list[j]>=1:
                df.at[i, 'Team'] = j+1

    df = df.sort_values('Team',ascending=True)

    
    ### LEGACY - IN CASE CVXPY DOES NOT WORK
    
    ## OPTIMIZATION - Objective: min cTx. Cf doc: https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.linprog.html#scipy.optimize.linprog
    #res = sc.optimize.linprog(c = c_choices, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=(lb,ub), method='simplex', callback=None, options=None, x0=None)

    #x_res = res['x']
    #x_res = np.floor(x_res+0.5) # In case results are not integers
    #x_res_team = [[] for i in range(m)] # Final result to return: teammates for each project

    return df
