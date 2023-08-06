import numpy as np


class Atoms:
    '''Atoms class holding system parameters.'''
    def __init__(self, atom, X, a, ecut, Z, s, f, Ns):
        self.atom = atom
        self.X = X
        self.a = a
        self.ecut = ecut
        self.Z = Z
        self.s = s
        self.f = f
        self.Ns = Ns
        self.initialize()

    def initialize(self):
        '''Initialize the Atoms object.'''
        M, N = self._get_index_matrices()
        self.R, self.Omega, self.sn, self.r = self._get_cell(M)
        self.G, self.G2, self.G2c, self.active = self._get_G(N)
        self.Sf = self._get_Sf()

    def _get_index_matrices(self):
        '''
            Generate index matrices M and N to build the real and reciprocal space sampling.
            Latex: List 3.4
                   List 3.5
        '''
        ms = np.arange(np.prod(self.s))
        m1 = ms % self.s[0]
        m2 = np.floor(ms / self.s[0]) % self.s[1]
        m3 = np.floor(ms / (self.s[0] * self.s[1])) % self.s[2]
        M = np.column_stack((m1, m2, m3))

        n1 = m1 - (m1 > self.s[0] / 2) * self.s[0]
        n2 = m2 - (m2 > self.s[1] / 2) * self.s[1]
        n3 = m3 - (m3 > self.s[2] / 2) * self.s[2]
        N = np.column_stack((n1, n2, n3))
        return M, N

    def _get_cell(self, M):
        '''
            Build the unit cell R and create the respective sampling r.
            Latex: Eq. 3.3
                   List. 3.3
                   Eq. 3.5
                   List. 3.3
        '''
        R = self.a * np.eye(3)
        Omega = np.linalg.det(R)
        sn = np.prod(self.s)
        r = M @ np.linalg.inv(np.diag(self.s)) @ R.T
        return R, Omega, sn, r

    def _get_G(self, N):
        '''
            Sample the G-vectors, build squared magnitudes G2, and calculate the active space.
            Latex: Eq. 3.8
                   List. 3.5
                   List. 3.6
                   List. 3.7
        '''
        G = 2 * np.pi * N @ np.linalg.inv(self.R)
        G2 = np.sum(G**2, axis=1)
        active = np.nonzero(G2 <= 2 * self.ecut)
        G2c = G2[active]
        return G, G2, G2c, active

    def _get_Sf(self):
        '''
            Calculate the structure factor Sf.
            Latex: Eq. 3.9
                   List. 3.8
        '''
        Sf = np.sum(np.exp(-1j * self.G @ self.X.T), axis=1)
        return Sf
