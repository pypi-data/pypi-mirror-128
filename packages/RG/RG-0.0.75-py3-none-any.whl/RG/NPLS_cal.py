# Function Nway-PLS

import numpy as np
from tensorly.decomposition import parafac, tucker
import RG as rg



'''
NPLS multilinear partial least squares regression
adapted to pyhton from http://www.models.life.ku.dk/nwaytoolbox


[Xfactors, Yfactors, core, B, ypred, ssx, ssy, reg] = NPLS(X,y,nbPC)

 MULTILINEAR PLS  -  N-PLS

 INPUT
     X        Array of independent variables
     y        Array of dependent variables
     nbPC     Number of principal components to compute

 OUTPUT
     Xfactors Holds the components of the model of X in a cell array.
     Yfactors Similar to Xfactors but for Y
     Core     Core array used for calculating the model of X
     B        The regression coefficients from which the scores in
          the Y-space are estimated from the scores in the X-
          space (U = TB);
     ypred    The predicted values of Y for one to Fac components
          (array with dimension Fac in the last mode)
     ssx      Variation explained in the X-space.
          ssx(a,1) is the sum-squared residual after first a factors.
          ssx(a,2) is the percentage explained by first a factors.
     ssy      As above for the Y-space
     reg      Cell array with regression coefficients for raw (preprocessed) X
     
 AUXILIARY
If missing elements occur these must be represented by NaN.


Copyright (C) 1995-2006  Rasmus Bro & Claus Andersson
Copenhagen University, DK-1958 Frederiksberg, Denmark, rb@life.ku.dk
     
'''


#%% Function  Xtu

def fct_Xtu(X, u, dimX, ordX, Missing=0):
    
    if Missing:
        w = np.zeros((dimX[1],1))
        for i in range(len(X.T)):       
            # Only keep samples with no nan
            m = (1-np.isnan(X))[:,i] # as 0 in 1 (0 if value missing)
            m = list(map(bool,m)) # boolean version
                
            if (u[m].T@u[m] != 0):
                ww = X[m,i].T@u[m]/(u[m].T@u[m])
            else:
                ww = X[m,i].T@u[m]
                
            if len(ww)==0:
                w[i] = 0
            else:
                w[i] = ww
    else:
        w  = X.T@u
    
    if ordX>2:
        w_reshaped = np.reshape(w,(dimX[1:]), order='F')
        _, wloads = parafac(w_reshaped, 1)

    
    # If X is 2D-data
    else:
        wloads = [None]*1
        wloads[0] = w
    
    for j in range(len(wloads)):
        # Normalize
        wloads[j] = wloads[j]/np.linalg.norm(wloads[j])
            # Apply sign convention
        sq = wloads[j]**2*np.sign(wloads[j])
        wloads[j] = wloads[j]*np.sign(np.sum(sq))
    
    # Unfold solution
    if ordX>2:
        wkron = np.kron(wloads[-1],wloads[-2])
        for o in range(-3,-len(wloads)-1,-1):
            wkron = np.kron(wkron, wloads[o])    
    # If X is 2D-data
    else:
        wkron = wloads[0]
    
    return wloads, wkron


def fct_outerm(facts, lo=0, vect=0):
    
    order = len(facts)
    if lo==0:
        mwasize=np.zeros((order))
    else:
        mwasize=np.zeros((1,order-1))
    
    for i in range(order):
        mwasize[i] = len(facts[i])
        nofac = len(facts[i].T)

    mwa =  np.zeros((int(np.prod(mwasize)),nofac))
    
    for j in range(nofac):
        if (lo != 1):
            mwvect = facts[0][:,j]
            mwvect = mwvect[np.newaxis].T
            for i in range(1,order):
                if (lo != i):
                    mwvect =   mwvect@(facts[i][:,j][np.newaxis])
                    mwvect = mwvect.flatten(order='F')
        elif (lo==1):
            mwvect = facts[1][:,j]
            for i in range(2, order):
                mwvect =   mwvect@(facts[i][:,j][np.newaxis])
                mwvect = mwvect.flatten(order='F')
        mwa[:,j] = mwvect  
    if (vect!=1):
        mwa = np.sum(mwa, axis=1)
        mwa = np.reshape(mwa, mwasize, order='F')
        
    return mwa







def NPLS_cal(X,y,nbPC):

    #%% Determine dimensions
    
    ordX = X.ndim
    ordy = y.ndim
    
    dimX = X.shape
    dimy = y.shape
    
    #%% Re-shape X and y in 2D
    
    X = np.reshape(X, (dimX[0], np.prod(dimX[1:])), order='F')
    y = np.reshape(y, (dimy[0], np.prod(dimy[1:])), order='F')
    
    #%% Declare variables
    
    Yres = y
    
    T = np.zeros((dimX[0],nbPC))
    W = [None]*(ordX-1)
    U = np.zeros((dimX[0],nbPC))
    Q = [None]*(ordy-1)
    Qkron = np.zeros((np.prod(dimy[1:]),nbPC))
    B = np.zeros((nbPC,nbPC))
    Xfac= [None]*ordX
    Ypred = np.zeros((np.prod(dimy[:]),nbPC))
    
    ssx = np.zeros((nbPC,1))
    ssy = np.zeros((nbPC,1))
    
    
    reg = [None]*dimy[1]
    core = [None]*nbPC
    
    # Initialize for missing values
    MissingX = 0
    MissingY = 0
    
    # Check if missing values X and y
    if np.any(np.isnan(X)): 
        print('Missing values in X are taken care of ')
        MissingX = 1
    if np.any(np.isnan(y)): 
        print('Missing values in Y are taken care of ')
        MissingY = 1
    
    SSX = np.zeros((1,1))
    SSY = np.zeros((1,1))
    
    if MissingX:
        SSX[0] = np.sum(X[(1-np.isnan(X))]*X[(1-np.isnan(X))])
    else:
        SSX[0] = np.sum(X*X)
    
    if MissingY:
        SSY[0] = np.sum(y[(1-np.isnan(y))]*y[(1-np.isnan(y))])
    else:
        SSY[0] = np.sum(y*y)
    
    #%% For each component
    
    for A in range(nbPC):
    
        # Initialize u
        if ((ordy==2) & (dimy[1]==1)):
            u = Yres 
        else:
            u = Yres.copy()
            u, _, _ = rg.PCA(Yres,1) #for PLS2
        
        # # Initialization
        t_temp = np.random.randn(dimX[0], 1)
        
        error = 1
        while error > 1E-10:
            wloads, wkron = fct_Xtu(X, u, dimX, ordX, MissingX)
            
            # Calculate t
            if MissingX:
                t = np.zeros((len(X),1))
                for i in range(len(X)):
                    m = (1-np.isnan(X))[i,:]   
                    m = list(map(bool,m)) 
                    t[i] = X[i,m]@wkron[m]/(wkron[m].T@wkron)
            else:
                t = X@wkron
            
            qloads, qkron = fct_Xtu(Yres, t, dimy, ordy, MissingY)
            
            # Calculate u 
            if MissingY:
                u = np.zeros((len(y),1))
                for i in range(len(y)):
                    m = (1-np.isnan(y))[i,:]   
                    m = list(map(bool,m)) 
                    u[i] = Yres[i,m]@qkron[m]/(qkron[m].T@qkron)
            else:
                u = Yres@qkron
            
            error = np.linalg.norm(t-t_temp)/np.linalg.norm(t)
            t_temp = t
        
        #%%
        # Arrange t scores so they positevely correlated with u 
        cc = np.corrcoef(t.T,u.T)
        if (cc[0,1]<1 ):
            t = -t;
            wloads[0] = -wloads[0]
            
        T[:,A] = np.squeeze(t)
        U[:,A] = np.squeeze(u)
        Qkron[:,A] = np.squeeze(qkron)
        
        for i in range(ordX-1):
            if A==0:
                W[i] = wloads[i]
            else:
                W[i] = np.concatenate([W[i], wloads[i]], axis=1)
                
        for i in range(ordy-1):
            if A==0:
                Q[i] = qloads[i]
            else:
                Q[i] = np.concatenate([Q[i], qloads[i]], axis=1)
                
        
        # #%% Make core arrays
        if ordX>1:
            Xfac[0] = T[:,:A+1]
            Xfac[1:] = W
            core[A] = calcore(np.reshape(X, dimX, order='F'),Xfac)
        else:
            core[A] = 1
            
        B[:A+1,A] = np.linalg.inv(T[:,:A+1].T@T[:,:A+1])@T[:,:A+1].T@U[:,A]
        
        # %% Make X model
        
        if ordX>2:
            Wkron = np.kron(W[-1],  W[-2])
        else:
            Wkron = W[-1]
            
        for i in range(-3,-ordX,-1):
            Wkron = np.kron(Wkron@W[i])
               
        if nbPC>1:
            xmodel =  T[:,:A+1]@np.reshape(core[A], (A+1,(A+1)**(ordX-1)), order='F')@Wkron.T
        else:
            xmodel =  T[:,:A+1]@core[A]@Wkron.T
        
        
        ypred = T[:,:A+1]@B[:A+1,:A+1]@Qkron[:,:A+1].T
        Ypred[:,A] = ypred.flatten(order='F')      
        
        # Deflation
        Xres = X - xmodel
        Yres = y - ypred
        
        if MissingX:
            ssx[A] =  np.sum(X[(1-np.isnan(X))]*X[(1-np.isnan(X))])
        else:       
            ssx[A] = np.sum(Xres*Xres)
            
        if MissingY:
            ssy[A] = np.sum(y[(1-np.isnan(y))]*y[(1-np.isnan(y))])  
        else:
            ssy[A] = np.sum(Yres*Yres)
    # Reshape y to original dimension
    ypred = np.reshape(ypred,dimy, order='F')

    ssx = np.concatenate([np.concatenate([SSX, ssx], axis=0),np.concatenate([np.zeros((1,1)),100*(1-ssx/SSX)], axis=0)], axis=1)
    ssy = np.concatenate([np.concatenate([SSY, ssy], axis=0),np.concatenate([np.zeros((1,1)),100*(1-ssy/SSY)], axis=0)], axis=1)
    
    # Save 
    Xfactors = W.copy()
    Xfactors.insert(0,T)
    
    Yfactors = Q.copy()
    Yfactors.insert(0,U)
    
    #%% Calculate regression coefficients
    if (ordy>2):
        print('Regression coefficient are only calculated for models with a vector-Y or multivariate Y (not multi-way Y)')
    else:
        R = fct_outerm(W,0,1)
        regi = []
        for iy in range(len(y.T)):
            if (ordX==2):
                dd = [dimX[1], 1]
            else:
                dd = dimX[1:]
            for A in range(nbPC):
                sR = R[:,:A+1]@B[:A+1,:A+1]@np.diagflat(Q[0][iy,:A+1])
                ssR =  np.sum(sR, axis=1)
                regi.append(np.reshape(ssR, dd, order='F'))
                
            reg[iy] = regi
        
    
    return Xfactors, Yfactors, core, B, ypred, ssx, ssy, reg
        
     
        
# Function calcore


'''
CALCORE Calculate the Tucker core

	
 [G]=calcore(X,Factors,Options);
 [G]=calcore(X,Factors);

 This algorithm applies to the general N-way case, so
 the unfolded X can have any number of dimensions. The principles of
 'projections' and 'systematic unfolding methodology (SUM)' are used
 in this algorithm so orthogonality is required.
 This algorithm can handle missing values in X and
 also allows for TUCKER2 models using the an empty matrix in the
 corresponding cell of Factors.
 The variable 'Factors' must contain the stringed-out factors.

 Copyright (C) 1995-2006  Rasmus Bro & Claus Andersson
 Copenhagen University, DK-1958 Frederiksberg, Denmark, rb@life.ku.dk
'''

def calcore(X, Factors, O=0, MissingExist=1):

    # Function calcore
    dimX = np.array(X.shape)
    X = np.reshape(X, (dimX[0], np.prod(dimX[1:])), order='F')
    Fac = np.zeros(len(Factors))
     
    ff = []
    for f in range(len(Factors)):
        ff= np.concatenate([ff, Factors[f].flatten()], axis=0)
        Fac[f] = len(Factors[f].T)     
        # Tucker 2  ie no compression in that mode
        if (Factors[f].all==None):
            Fac[f] = -1
    Factors = ff[np.newaxis].T
    
    # Initialize system variables
    if len(Fac)==1:
        Fac = Fac*np.ones(len(dimX))
    
    Fac_orig = Fac
    i = np.where(Fac==-1)
    Fac[i] = np.zeros((1,len(i)))
    N = len(Fac)
    
    Fac = np.array(Fac, dtype=int)    

    if 'MissingExist' in locals():
        if np.sum(np.isnan(X)) > 0:
            MissingExist=1
        else:
            MissingExist=0
            
    FIdx0 = np.cumsum(np.concatenate([np.zeros(1), dimX[:N-1]*Fac[:N-1]]))
    FIdx0 = np.array(FIdx0, dtype=int)
    FIdx1 = np.cumsum(dimX*Fac)
    FIdx1 = np.array(FIdx1, dtype=int)

    if (('O' in locals()) and (O==None)) :
        O=1
        
    if O: # means orthogonality
        CurDimX = list(dimX)
        RedData = X
        for c in range(N):
            if Fac_orig[c]==-1:
                kthFactor = np.eye(dimX[c])
                CurDimX[c] = dimX[c]
            else:
                kthFactor = Factors[FIdx0[c]:FIdx1[c]]
                CurDimX[c] = Fac[c]
                
            if MissingExist:
                RedData = missmult(kthFactor.T, RedData)
            else: 
                RedData = kthFactor.T@RedData
                
            if (c!=N-1):
                newi = CurDimX[c+1]
                newj = np.prod(CurDimX)/CurDimX[1]
            else:
                newi = CurDimX[0]
                newj = np.prod(CurDimX)/CurDimX[0]
            RedData = np.reshape(RedData.T, newi, newj)
        G = RedData
        
    else: # oblique factors
        if Fac_orig[0] ==-1:
            LMatTmp = np.eye(dimX[0])
        else:
            LMatTmp = np.reshape(Factors[FIdx0[0]:FIdx1[0]], (dimX[0], Fac[0]))
            
        RMatTmp=1
        for c in range(1,N):
            if Fac_orig[c]==-1:
                kthFactor = np.eye(dimX[c])
            else:
                kthFactor = np.reshape(Factors[FIdx0[c]:FIdx1[c]], (dimX[c], Fac[c]))
            RMatTmp = np.kron(kthFactor.T, RMatTmp)
            
        if MissingExist:
            RedData = missmult(np.linalg.pinv(LMatTmp), X)
            RedData = missmult(RedData, np.linalg.pinv(RMatTmp))
        else:
            RedData, _, _, _  = np.linalg.lstsq(LMatTmp,X, rcond=None)
            RedData = RedData@np.linalg.pinv(RMatTmp)
        G = RedData
    
    filtre = Fac==0
    Fac[filtre] = dimX[filtre]
    Fac = np.array(Fac, dtype=int)
    G = np.reshape(G, Fac, order='F')
    
    return G
     


'''
MISSMULT product of two matrices containing NaNs

[X]=missmult(A,B)
This function determines the product of two matrices containing NaNs
by finding X according to
     X = A*B
If there are columns in A or B that are pur missing values,
then there will be entries in X that are missing too.

The result is standardized, that is, corrected for the lower
number of contributing terms.

Missing elements should be denoted by 'NaN's


 Copyright (C) 1995-2006  Rasmus Bro & Claus Andersson
 Copenhagen University, DK-1958 Frederiksberg, Denmark, rb@life.ku.dk

INBOUNDS
REALONLY
'''

def missmult(A, B):
    
    ia, ja = A.shape
    ib, jb = B.shape 
    
    X = np.zeros((ia, jb))
    
    one_arry = np.ones(ia, 1)
    
    for j in range(jb):      
        p = one_arry@B[:,j][np.newaxis]
        tmpMat = A*p
        X[:,j] = missum(tmpMat.T)

    
    return X
    
            

'''
MISSSUM sum of a matrix X with NaN's

[mm]=misssum(X,def)

This function calculates the sum of a matrix X.
X may hold missing elements denoted by NaN's which
are ignored.

The result is standardized, that is, corrected for the lower
number of contributing terms.

Check that for no column of X, all values are missing

 Copyright (C) 1995-2006  Rasmus Bro & Claus Andersson
 Copenhagen University, DK-1958 Frederiksberg, Denmark, rb@life.ku.dk
Insert zeros for missing, correct afterwards
'''

def missum(X):
    
    missidx = np.isnan(X)
    i = np.where(missidx)
    
    if (i!=None):
        X[i] = 0
    
    n_real = len(X) - np.sum(missidx,axis=0)
    weight = len(X)
    
    column_nul = np.where(n_real==0)
    
    
    if ((X.ndim==1) or X.shape[1]==1):
        if (n_real==0):
            mm = np.nan
        else:
            mm = weight*np.sum(X, axis=0)/n_real    
    else:
        n_real[column_nul] = 1    
        mm = weight*np.sum(X, axis=0)/n_real
        mm[column_nul] = np.nan 
        
    return mm
    
    

        



        
     
     
        
     