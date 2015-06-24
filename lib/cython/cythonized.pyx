import numpy as np
cimport numpy as np

def diagonalize(int n, float M):
        """
        For a given Q wich depends on the values of n and M, we compute
        the "diagonalized" expression of Q. This method returns three
        matrixes A, D and A^{-1} such that Q = ADA^{-1}.
        """
        Q = np.array([[-M - 1,    M,      1],
                     [M / (n-1), -M / (n-1), 0],
                     [0,    0,  0]], float, order='F')
        eigen_val, eigen_vect = np.linalg.eig(Q)
        D = np.diag(eigen_val)
        A = eigen_vect
        A_inv = np.linalg.inv(A)
        return (A, D, A_inv)
