import numpy as np
from scipy.linalg import sqrtm

from .utils import diagprod
from .exc import lda_slater_x, lda_vwn_c
from .operators import PWBasis
from .energies import get_Ecoul, get_Eewald, get_Een, get_Exc, get_T


def coulomb_pot(atoms, op):
    '''
        Simple ionic Coulomb potential.
        Latex: Eq. 3.15 ff.
               List. 3.17
    '''
    Vcoul = np.zeros_like(atoms.G2)
    Vcoul[1:] = -4 * np.pi * atoms.Z[0] / atoms.G2[1:]
    return op.J(Vcoul * atoms.Sf)


class Hamiltonian:
    '''Hamiltonian class.'''
    def __init__(self, atoms, basis=PWBasis, potential=coulomb_pot):
        self.atoms = atoms
        self.op = basis(atoms)
        self.Vreciproc = potential(self.atoms, self.op)
        self._init_W(seed=1234)

    def scf(self, Nit=300, beta=1e-5, etol=1e-6):
        '''Self-consistent field (SCF) using a steepest descent algorithm.'''
        self.Eewald = get_Eewald(self.atoms)
        self.Etot = sd(W=self.W, scf=self._scf_step, Nit=Nit, beta=beta, etol=etol)
        return self.Etot

    def _scf_step(self, W):
        '''Perform one SCF step.'''
        self.W = W
        self.Y = orth(self.atoms, self.op, self.W)
        self.n = get_n(self.atoms, self.op, self.Y)
        self.phi = solve_poisson(self.atoms, self.op, self.n)
        self.Eel = get_Eel(self.atoms, self.op, self.W, self.Vreciproc, self.Y, self.n, self.phi)
        self.Ham = H(self.atoms, self.op, self.W, self.Vreciproc, self.Y, self.n, self.phi)
        self.Grad = get_grad(self.atoms, self.op, self.W, self.Ham)
        return self.Eel + self.Eewald, self.Ham, self.Grad

    def _init_W(self, seed=None):
        '''
            Initialize wave functions W using random numbers.
            Latex: List. 3.18
        '''
        np.random.seed(seed)
        W = np.random.randn(len(self.atoms.active[0]), self.atoms.Ns)
        self.W = orth(self.atoms, self.op, W)


def orth(atoms, op, W):
    '''
        Perform orthogonalization of wave functions.
        Latex: Eq. 2.34 ff.
    '''
    U = sqrtm(W.conj().T @ op.O(W))
    return W @ np.linalg.inv(U)


def sd(W, scf, Nit, beta=1e-5, etol=1e-6):
    '''
        Steepest descent method as SCF algorithm.
        An SCF algorithm.
        Latex: List. 3.21
               Fig. 3.2
    '''
    Elist = np.zeros(Nit)
    for i in range(Nit):
        E, H, grad = scf(W)
        W = W - beta * grad
        Elist[i] = E
        print('Nit: {}  \tEtot: {:.6f} Eh'.format(i + 1, E), end='\r')
        if i > 1:
            if abs(Elist[i - 1] - Elist[i]) < etol:
                print('\nSCF converged.')
                return E
    print('\nSCF not converged!')
    return E


def get_n(atoms, op, Y):
    '''
        Calculate the electronic density n.
        Latex: Eq. 2.36
               List. 3.23
    '''
    n = np.zeros((atoms.sn, 1))
    for i in range(Y.shape[1]):
        psi = op.I(Y[:, i])
        n += atoms.f[i] * np.real(psi.conj() * psi)
    return n.T[0]


def solve_poisson(atoms, op, n):
    '''
        Solve the poisson equationto get phi.
        Latex: Eq. 2.48
    '''
    return -4 * np.pi * op.Linv(op.O(op.J(n)))


def get_Eel(atoms, op, W, Vreciproc, Y, n, phi):
    '''
        Calculate the electronic energy Eel.
        Latex: Eq. 2.49
    '''
    T = get_T(atoms, op, Y)
    Een = get_Een(Vreciproc, n)
    Exc = get_Exc(op, n)
    Ecoul = get_Ecoul(op, n, phi)
    return np.real(T + Een + Exc + Ecoul)


def get_grad(atoms, op, W, H):
    '''
        Calculate gradient.
        Latex: Eq. 2.43
               List. 3.24
    '''
    U = W.conj().T @ op.O(W)
    invU = np.linalg.inv(U)
    HW = H
    F = np.diag(atoms.f)
    U12 = sqrtm(np.linalg.inv(U))
    Ht = U12 @ (W.conj().T @ HW) @ U12
    return (HW - (op.O(W) @ invU) @ (W.conj().T @ HW)) @ (U12 @ F @ U12) + op.O(W) @ (U12 @ Q(Ht @ F - F @ Ht, U))


def Q(inp, U):
    '''
        The Q operator, needed to calculate the derivative of the Lagrangian.
        Latex: Eq. 2.47
               List. 3.25
    '''
    mu, V = np.linalg.eig(U)
    mu = np.reshape(mu, (len(mu), 1))
    denom = np.sqrt(mu) @ np.ones((1, len(mu)))
    denom = denom + denom.conj().T
    return V @ ((V.conj().T @ inp @ V) / denom) @ V.conj().T


def H(atoms, op, W, Vreciproc, Y, n, phi):
    '''
        Construct the right-hand side Hamiltonian H.
        Latex: Eq. 2.45 ff.
               List. 3.26
    '''
    vxc = lda_slater_x(n)[1] + lda_vwn_c(n)[1]
    Veff = Vreciproc + op.Jdag(op.O(op.J(vxc) + phi))
    return -0.5 * op.L(W) + op.Idag(diagprod(Veff, op.I(W)))
