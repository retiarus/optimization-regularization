import numpy as np

cimport numpy as np

# We now need to fix a datatype for our arrays. I've used the variable
# DTYPE for this, which is assigned to the usual NumPy runtime
# type info object.
DTYPE = np.float
# "ctypedef" assigns a corresponding compile-time type to DTYPE_t. For
# every type in the numpy module there's a corresponding compile-time
# type with a _t-suffix.
ctypedef np.float_t DTYPE_t

'''
Refularization Module
'''

cdef class TikhonovOrder0(object):
    cdef int _Nx
    cdef public str name, type
    cdef public float sum
    
    def __init__(self, Nx):
        self._Nx = Nx
        self.name = 'Tikhonov Order 0'
        self.type = 'tikhonovorder0' 
        
        # Tikhonovo of order 0 - identity matrix
            
    def __call__(self, np.ndarray[DTYPE_t, ndim=1] f):
        if len(f) != self._Nx:
            return None
        else:
            print(f)
            sum = np.sum(np.power(f, 2))
            return np.sum(f**2.0)

