
import numpy as np

def interactions(X):
    '''
    
    Interactions: include 2nd order interactions
    Multiply all columns pairwise to get each and every possible interaction
    [Z] = interactions(X)
    
    INPUT
    X [n x k] <numpy.ndarray>
        spectra
        n samples
        k variables
    
    # Test matrix
    #X = np.arange(1,5,1)[np.newaxis]
    #X = np.concatenate((X,X),axis=0)
    
    OUTPUT
    Z [n x ?] 
        preprocessed spectra
         
    
    '''
    
    
    Z = X
    for i in range(X.shape[1]):
        for j in range(X.shape[1]):
            if j>i:
                z = X[:,i]*X[:,j]
                z = z[np.newaxis].T
                Z = np.concatenate((Z,z),axis=1)
        

    return Z