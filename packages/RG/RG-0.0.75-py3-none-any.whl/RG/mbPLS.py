# mbPLS: multiblock PLS

import numpy as np

def mbPLS(nbPC, Y,*args,scale=1):
    '''
    
    mbPLS: multiblock PLS
    [Tt, T_all, W, W_all, SSX, SSY, SSXi] = mbPLS(nbPC, Y, X1, X2, Xi,..., Xb, scale=1)
    
    INPUT
    nbPC <int>
        number of components in the mbPLS decomposition
    Y [n x m] <numpy.ndarray>
        responses
        n samples
        m variables     
    *args <numpy.ndarray>
        sequence of matrices to include as blocks in mbPLS
        Unlimited number of blocks b
        Each block has same number of samples but various number of variables     
            Xi [n x ki] <numpy.ndarray>
                spectra
                n samples
                ki variables
        Blocks must be centered or autoscaled before using this function
    scale <boolean> (0 or 1)
        scales blocks by diving each block by root square of the number of variables of the block
        Necessary if different number of variables in each block
        By default blocks scaled (scale=1)   

    OUTPUT
    Tt [n x nbPC] <numpy.ndarray>
        superscores
    T_all [b] <list> containing [n x nbPC] <numpy.ndarray>
        scores of each individual block
    W [k x nbPC] <numpy.ndarray>
        superloadings
    W_all [b] <list> containing [ki x nbPC] <numpy.ndarray>
        loadings of each individual block    
    
    SSX [nbPC x 1] 
        global matrix X's sum of squared variance explained by each component
    SSY [nbPC x 1] 
        Y-block sum of squared variance explained by each component  
    SSXi [nbPC x b] 
        X-block sum of squared variance explained by each component (for each block)
    
    '''
    
     
#%% Load data
    # Tuple containing n block matrices
    varargin = args
    n_block = len(varargin)
    
    varargin_temp = []
    
    # Creation matrix X containing n blocks    
    X = []
    for i in range(n_block):
        xi = varargin[i]    
        # Scaling
        if (scale==1):
            xi = xi/np.sqrt(xi.shape[1])
            varargin_temp.append(xi)
        # Create global matrix
        if (i==0):       
            X = xi
        else:
            X = np.append(X,xi,axis=1)

    n,k = X.shape
    n,l = Y.shape
    
    if (scale==1):
        varargin = varargin_temp
    # Save copy
    varargin0 = varargin
    X0 = X.copy()
    Y0 = Y.copy()
    
    #%%  Initialization
    T = np.zeros((n,n_block))
    Tt = np.zeros((n,nbPC))
    U = np.zeros((n,nbPC))
    W = np.zeros((n_block,nbPC))
    
    X_all = []
    
    # For creation of tuple containing T for each block
    T_all = []
    T_all_temp = []
    for i in range(n_block):
        Ti = np.zeros((n,nbPC))
        T_all.append(Ti)
        
    # For creation of tuple containing W for each block
    W_all = []
    W_all_temp = []
    for i in range(n_block):
        Xi = varargin[i]
        n,ki = Xi.shape
        Wi = np.zeros((ki,nbPC))
        W_all.append(Wi)
           
   # Sum of squares
    SSXi = np.zeros((nbPC,n_block))
    SSY = np.zeros((nbPC,1))

    
    # %% PLS
    for a in range(nbPC):
        u = np.ones((n,1))
        u_temp = np.ones((n,1))
        tt_temp = np.ones((n,1))
        error_u = 1
        error_tt = 1
        
        while (error_u > 1E-20) and (error_tt > 1E-20):
            
                    for i in range(n_block):
                        Xi = varargin[i]
                        wi = (Xi.T@u)/(u.T@u)
                        wi = wi / np.linalg.norm(wi)
                        ti = Xi@wi
                        
                        T[:,i] = np.squeeze(ti)
                      
                        Wi = W_all[i]
                        Wi[:,a] = np.squeeze(wi)
                        W_all_temp.append(Wi)
                    W_all = W_all_temp
                    W_all_temp = []
                    
                    wt = (T.T@u)/(u.T@u)
                    wt = wt/np.linalg.norm(wt)
                    tt = (T@wt)/(wt.T@wt)
        
                    q = (Y.T@tt) / (tt.T@tt)
                    u = (Y@q) / (q.T@q)
        
                    error_tt = sum(np.power((tt-tt_temp),2),0) 
                    tt_temp = tt
        
                    error_u = sum(np.power((u-u_temp),2),0) 
                    u_temp = u
                                       
                    
        for i in range(n_block):
            # Deflation 
            Xi = varargin[i]
            pi = (Xi.T@tt)/(tt.T@tt) 
            Xi = Xi - tt@pi.T
            X_all.append(Xi)
            
            # Sum of squares for X
            Xi_hat = tt@pi.T
            Xi_0 = varargin0[i]
            ssXi_0 = np.sum(np.sum(Xi_0*Xi_0))
            ssXi = np.sum(np.sum(Xi_hat*Xi_hat))
            ssXi = ssXi/ssXi_0
            
            SSXi[a,i] = ssXi
            
            
        # Update of deflated blocks
        varargin = X_all
        X_all = []
        
        pt = (X.T@tt)/(tt.T@tt)
    
        # Scaling based on PLS Toolbox (not necessary here)
#        tt = tt*np.linalg.norm(pt)  
#        wt = wt*np.linalg.norm(pt)
#        pt = pt/np.linalg.norm(pt)
            
        b = (u.T@tt)/(tt.T@tt)
        Y = Y - b*tt@q.T 
        
        # Sum of squares for Y
        Yhat = b*tt@q.T
        ssY0 = np.sum(np.sum(Y0*Y0))
        ssY = np.sum(np.sum(Yhat*Yhat))
        ssY = ssY / ssY0;
        SSY[a] = ssY
            
        
        # Save 
        Tt[:,a] = np.squeeze(tt)
        U[:,a] = np.squeeze(u)
        W[:,a] = np.squeeze(wt)
        
        for i in range(n_block):
            Ti = T_all[i]
            Ti[:,a] = T[:,i]
            T_all_temp.append(Ti)
        T_all = T_all_temp
        T_all_temp = []
    
                          
    SSX = np.sum(SSXi,axis=1)/n_block
    SSX = SSX[np.newaxis].T
 
    return Tt, T_all, W, W_all, SSX, SSY, SSXi
    
        