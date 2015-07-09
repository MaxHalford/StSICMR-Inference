import numpy as np
import bisect
import json

class StSICMR:
    '''
    This class represents the Continuous Time Markov Chain of a Structured
    Symmetrical Island model with Changes in the Migration Rates.
    The population is splitted into "n" similar sized islands. These
    islands exchange migrants with a rate M that may change at some moments
    in the population history.
    '''

    def __init__(self, n, T, M, C):
        self.update(n, T, M, C)

    def update(self, n, T, M, C):
        '''
        Update a model with new parameters for genalg optimization, this
        saves a bit of time compared to instantiating a new class.
        '''
        self.n = n
        self.T = T
        self.M = M
        self.C = C
        # Tuples with the form (A,D,A_inv) for every migration rate
        self.diagonalizedQ = [self.diagonalize(n, mc[0], mc[1])
                              for mc in zip(M, C)]
        # We store the value of P_{T_i-T_{i-1}} for each value in T
        self.expos = [C[0]] + [self.exponential_Q(T[i]-T[i-1], i-1)
                               for i in range(1, len(T))]
        # We store the cumulative product of P_{T_i-T_{i-1}}
        self.cumprods = [C[0]]
        for expo in self.expos[1:]:
            self.cumprods.append(np.dot(self.cumprods[-1], expo))
            
    def diagonalize(self, n, m, c):
        '''
        For a given Q wich depends on the values of n and M, we compute
        the "diagonalized" expression of Q. This method returns three
        matrixes A, D and A^{-1} such that Q = ADA^{-1}.
        '''
        # Compute the infinitesimal generator
        Q = np.array([[-m - 1/c , m         , 1/c],
                      [m / (n-1), -m / (n-1), 0  ],
                      [0        , 0         , 0  ]])
        # Compute the eigenvalues and vectors for the diagonalization
        eigenVal, eigenVect = np.linalg.eig(Q)
        # Put the eigenvalues in a diagonal
        D = np.diag(eigenVal)
        A = eigenVect
        Ainv = np.linalg.inv(A)
        return (A, D, Ainv)

    def exponential_Q(self, t, i):
        '''
        Computes e^{tQ_i} for a given t.
        Note that we will use the stored values of the diagonal expression
        of Q_i. The value of i is between 0 and the index of the last
        demographic event (i.e. the last change in the migration rate).
        '''
        (A, D, Ainv) = self.diagonalizedQ[i]
        expD = np.diag(np.exp(t * np.diag(D)))
        return np.dot(np.dot(A, expD), Ainv)

    def evaluate_Pt(self, t):
        ''' Get the time interval that contains t. '''
        i = bisect.bisect_right(self.T, t) - 1
        #print ('{0} : {1} : {2}'.format(np.round(self.T, 2), t, i))
        return np.dot(self.cumprods[i],
                      self.exponential_Q(t-self.T[i], i))

    def cdf_T2s(self, t):
        '''
        Evaluates the CDF (cumulative distribution function) of the
        coalescence time of two haploid individuals
        sampled from the same island.
        '''
        return self.evaluate_Pt(t)[0][2]

    def pdf_T2s(self, t):
        '''
        Evaluates the PDF (probability density function) of the coalescence
        time of two haploid individuals sampled from the same island.
        '''
        return self.evaluate_Pt(t)[0][0]

    def cdf_T2d(self, t):
        '''
        Evaluates the CDF (cumulative distribution function) of the
        coalescence time of two haploid individuals
        sampled from different islands.
        '''
        return self.evaluate_Pt(t)[1][2]

    def pdf_T2d(self, t):
        '''
        Evaluates the PDF (probability density function) of the coalescence
        time of two haploid individuals sampled from different islands.
        '''
        return self.evaluate_Pt(t)[1][0]

    def lambda_s(self, t):
        '''
        Computes the value of lambda at time t. Here lambda(t) = N(0)/N(t)
        with N(0) the effective_population size at time 0 and N(t) the
        effective_population size at time t.
        This is for the case when both DNA are sampled from the same island.
        '''
        Pt = self.evaluate_Pt(t)
        return np.true_divide(1 - Pt[0][2],  Pt[0][0])

    def lambda_d(self, t):
        '''
        Computes the value of lambda at time t. Here lambda(t) = N(0)/N(t)
        with N(0) the effective_population size at time 0 and N(t) the
        effective_population size at time t.
        This is for the case when both DNA are sampled from different
        islands.
        '''
        Pt = self.evaluate_Pt(t)
        return np.true_divide(1 - Pt[1][2], Pt[1][0])
        
    def save(self, path):
        ''' Save the details of the model to a JSON file. '''
        # Create a dictionary
        DNA = {'n': int(self.n),
               'T': list(map(float, self.T)),
               'M': list(map(float, self.M)),
               'C': list(map(float, self.C))}
        # Save it a s a .json file
        with open(path + '.json', 'w') as outfile:
            json.dump(DNA, outfile)
        # Tell the user the inference has been saved
        print ('Model parameters saved to {0}.json.'.format(path))
