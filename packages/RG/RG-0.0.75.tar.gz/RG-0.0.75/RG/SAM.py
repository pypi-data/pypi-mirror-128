# SAM
#Spectral Angle Mapper Algorithm for Remote Sensing Image Classification
#Rashmi S, Swapna Addamani, Venkat1and Ravikiran S
#IJISET - International Journal of Innovative Science, Engineering & Technology, Vol. 1 Issue 4, June 2014.

import numpy as np
import math

def SAM(t,r):
    
    cos1 = np.sum(t*r)
    cos2 = np.sqrt(np.sum(t*t))
    cos3 = np.sqrt(np.sum(r*r))
    ccc = cos1/(cos2*cos3)
    
    # Return the arc cosine of x, in radians.
    a = math.acos(ccc)

    return a