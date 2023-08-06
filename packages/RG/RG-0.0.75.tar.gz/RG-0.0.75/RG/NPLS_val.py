# Function npred

import numpy as np

'''
NPRED prediction with NPLS model

See also:
'npls' 


Predict Y for a new set of samples using an N-PLS model

[ypred,T,ssx,Xres] = npred(X,Fac,Xfactors,Yfactors,Core,B,show);

INPUT
X        The array to be predicted
Fac      Number of factors to use in prediction
Xfactors Parameters of the calibration model of X (incl. scores) in a cell array
Yfactors Parameters of the calibration model of Y (incl. scores) in a cell array
Core     Core array used for calculating the model of X
B        Regression matrix of calibration model

OUTPUT
ypred    the predictions of y
T        is the scores of the new samples
ssX      sum-of-squares of x residuals
         ssX(1,1)  sum-of-squares of X
         ssX(2,1)  sum-of-squares of residuals
         ssX(1,2)  percentage variation explained after 0 component (=0)
         ssX(2,2)  percentage variation explained after Fac component

Xres     is the residuals of X

Copyright (C) 1995-2006  Rasmus Bro & Claus Andersson
Copenhagen University, DK-1958 Frederiksberg, Denmark, rb@life.ku.dk
Convert to old notation

'''

def NPLS_val(X,nbPC,Xfactors,Yfactors,core,B):

    dimX = X.shape
    X = np.reshape(X, (dimX[0], np.prod(dimX[1:])), order='F')
    
    DimY = []
    for j in range(len(Yfactors)):
        DimY.append(len(Yfactors[j]))

        
    Xres = X
    
    T = np.zeros((dimX[0],nbPC))
    
    W = []
    for f in range(nbPC):  
        w = Xfactors[-1][:,f]
        for o in range(len(Xfactors)-2,0,-1):
            w = np.kron(w,Xfactors[o][:,f])
        W.append(w)
    W = np.array(W).T
    
    Q = []
    for f in range(nbPC):  
        q = Yfactors[-1][:,f]
        for o in range(len(Yfactors)-2,0,-1):
            q = np.kron(q,Yfactors[o][:,f])
        Q.append(q)
    Q = np.array(Q).T
    
    for f in range(nbPC): 
        T[:,f] =  Xres@W[:,f]
        if f==(nbPC-1):
            Wkron = Xfactors[-1]
            for o in range(len(Xfactors)-2,0,-1):
                Wkron = np.kron(Wkron,Xfactors[o])
            Xres = Xres - T@np.reshape(core[f],(nbPC,nbPC**(len(dimX)-1)), order='F')@Wkron.T
      
    ypred = T@B@Q.T
    # Reshape y to original dimension
    ypred = np.reshape(ypred, DimY, order='F')

    
    ssx = np.sum(Xres*Xres)
    ssX = np.sum(X*X)
    SSX = np.array([[ssX, 0], [ssx, 100*(1-ssx/ssX)]])
    
    Xres = np.reshape(Xres, (dimX), order='F')

    
    return ypred, T, SSX, Xres
