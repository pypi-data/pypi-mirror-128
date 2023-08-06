import numpy as np
import scipy.linalg
from numba import jit

def compute_X(P0, P1, discount, X, pi):
    """
    Compute Delta*A_inv as defined in Algorithm 3 of the paper
    and store the product in matrix X
    """
    dim = P0.shape[0]
    i0 = 0 # state having null bias in non-discounted case
    mat_pol = np.copy(P1)
    for i, a in enumerate(pi):
        if a: continue
        else: mat_pol[i, :] = P0[i, :]
    Delta = P1 - P0
    if discount < 1.0:
        mat_pol *= discount
    else:
        mat_pol[:, i0] = -1.0
        mat_pol[i0, i0] = 0.0
        Delta[:, i0] = 0.0
    A = np.eye(dim, dtype=np.double) - mat_pol
    X[:,:] = scipy.linalg.solve(A.transpose(), Delta.transpose(), overwrite_a=True, overwrite_b=True, check_finite=False).transpose()

@jit
def substract_outer_product(X, col, row, visited, check_indexability):
    """
    Substract the outerproduuct col * row from X:
    
    X[i,j] = X[i,j] - col[i]*row[j]

    Assume that all arrays are of the right dimensions.
    """
    n = col.shape[0]
    for i in range(n):
        if check_indexability or not(visited[i]):
            for j in range(n):
                X[i,j] -= col[i]*row[j]

def update_X(sigma, discount, visited, X, check_indexability):
    """
    Update the matrix according to Algorithm 3 of the paper. 

    It updates all states as updating only a part of them makes the performance worst

    TODO: one could try to improve computation time when we do not need to check indexability
    """
    col_X_sigma = discount*np.copy(X[:, sigma])/(1.0+discount*X[sigma, sigma])
    row_X_sigma = np.copy(X[sigma,:])
    substract_outer_product(X, col_X_sigma, row_X_sigma, visited, check_indexability)

def find_mu_star(visited, y, z, current_mu, delta, discount, atol):
    """
    Find the smallest 
    """
    mu_star_k = current_mu
    next_sigma = -1
    mu_i_k = (delta + discount*(z - y*current_mu))/(1.0-discount*y)
    valid_idx = np.where( (mu_i_k > current_mu + atol) * np.logical_not(visited) ) [0]
    if len(valid_idx)>0:
        argmin = mu_i_k[valid_idx].argmin()
        return valid_idx[argmin], mu_i_k[valid_idx[argmin]]
    else:
        return -1, current_mu 

@jit
def compute_V_and_update_W(V, W, discount, V0, sigma_k, k, k0=0):
    sigma = sigma_k[k-1]
    V[k0] = V0
    for l in range(k0+1, k+1):
        if l==k:
            W[k-1] = discount*V[k-1] / (1+discount*V[k-1,sigma])
        V[l] = V[l-1] - W[l-1] * V[l-1, sigma_k[l-1]]

#@profile
def compute_whittle_indices(P0, P1, R0, R1, discount=1, check_indexability=True, verbose=False, atol=1e-12, number_of_updates=0):
    """
    Implementation of Algorithm 3 of the paper
    Test whether the problem is indexable
    and compute Whittle indices when the problem is indexable
    The indices are computed in increasing order

    Args:
    - P0, P1: transition matrix for rest and activate actions respectively
    - R0, R1: reward vector for rest and activate actions respectively
    - discount: discount factor
    - check_indexability: if True check whether the problem is indexable or not
    """
    dim = P0.shape[0]
    assert P0.shape == P1.shape
    assert R0.shape == R1.shape
    assert R0.shape[0] == dim

    is_indexable = True
    visited = np.zeros(dim, dtype=bool)
    pi = np.ones(dim, dtype=np.double)

    whittle_idx = np.empty(dim, dtype=np.double)
    X = np.empty((dim, dim), dtype=np.double)
    compute_X(P0, P1, discount, X, pi)
    y = -X.dot(pi)
    z = X.dot(R1)
    delta = R1 - R0
    whittle_idx = (delta + discount*z)/(1.0 - discount*y)
    sigma = np.argmin(whittle_idx)
    z -= whittle_idx[sigma]*y

    if number_of_updates>0:
        # We initialize the first V:
        V = np.zeros((dim,dim), dtype=np.double)
        W = np.zeros((dim,dim), dtype=np.double)
        sigma_k = np.zeros(dim, dtype=int)
        k0 = 0
        frequency_of_update = dim / number_of_updates

    if verbose: print('       ', end='')
    for k in range(1, dim):
        if verbose: print('\b\b\b\b\b\b\b{:7}'.format(k), end='', flush=True)
        if number_of_updates>0:
            # We define W and create a new V:
            sigma_k[k-1] = sigma
            if k > k0 + frequency_of_update:
                pi = np.logical_not(visited)
                compute_X(P0, P1, discount, X, pi)
                k0 = k-1
            compute_V_and_update_W(V, W, discount, X[:,sigma], sigma_k, k, k0)
            X[:,sigma] = V[k,:]
        else:
            update_X(sigma, discount, visited, X, check_indexability)
        visited[sigma] = True
        y += (1.0 - discount*y[sigma])*X[:, sigma]
        next_sigma, mu_star_k = find_mu_star(visited, y, z, whittle_idx[sigma], delta, discount, atol)
        whittle_idx[next_sigma] = mu_star_k
        z += (mu_star_k-whittle_idx[sigma])*y
        if check_indexability and is_indexable:
            if ((delta + discount*z > mu_star_k + atol)*visited).any():
                is_indexable = False
        sigma = next_sigma
    if verbose: print('\b\b\b\b\b\b\b', end='')
    return is_indexable, whittle_idx
