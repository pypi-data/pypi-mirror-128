import numpy as np


class PWBasis:
    '''
        Operator class with basis set dependend operators.
        Basis set: Plane waves (PW)
    '''
    def __init__(self, atoms):
        self.atoms = atoms

    def O(self, W):
        '''The overlap operator O.'''
        return O(self.atoms, W.T).T

    def L(self, W):
        '''The Laplace operator L.'''
        return L(self.atoms, W.T).T

    def Linv(self, W):
        '''The inverse Laplace operator Linv.'''
        return Linv(self.atoms, W.T).T

    def I(self, W):
        '''The forward transformation operator I.'''
        return I(self.atoms, W.T).T

    def J(self, W):
        '''The backward transformation operator J.'''
        return J(self.atoms, W.T).T

    def Idag(self, W):
        '''The Hermitian conjugate forward transformation operator Idag.'''
        return Idag(self.atoms, W.T).T

    def Jdag(self, W):
        '''The Hermitian conjugate backward transformation operator Jdag.'''
        return Jdag(self.atoms, W.T).T


def O(atoms, W):
    '''
        The overlap operator O.
        Latex: List. 3.9
    '''
    return atoms.Omega * W


def L(atoms, W):
    '''
        The Laplace operator L.
        Latex: Eq. 3.10
               List. 3.11
    '''
    if W.shape[1] == len(atoms.G2c):
        return -atoms.Omega * atoms.G2c * W
    else:
        return -atoms.Omega * atoms.G2 * W


def Linv(atoms, W):
    '''
        The inverse Laplace operator Linv.
        Latex: List. 3.12
    '''
    out = np.zeros_like(W, dtype=complex)
    if W.ndim == 1:
        out[1:] = W[1:] / atoms.G2[1:] / (-atoms.Omega)
    else:
        for i in range(len(W)):
            out[i][1:] = W[i][1:] / atoms.G2[1:] / (-atoms.Omega)
    return out


def I(atoms, W):
    '''
        The forward transformation operator I.
        Latex: Eq. 3.11
               List. 3.13
    '''
    if W.ndim == 1:
        W = np.array([W])
    if np.size(W, 1) == atoms.sn:
        Finv = np.empty_like(W, dtype=complex)
        for i in range(W.shape[0]):
            tmp = np.reshape(W[i], atoms.s, order='F')
            Finv[i] = np.fft.ifftn(tmp).flatten(order='F')
    else:
        Finv = np.empty((W.shape[0], atoms.sn), dtype=complex)
        for i in range(W.shape[0]):
            full = np.zeros(atoms.sn, dtype=complex)
            full[atoms.active] = W[i]
            full = np.reshape(full, atoms.s, order='F')
            Finv[i] = np.fft.ifftn(full).flatten(order='F')
    return atoms.sn * Finv


def J(atoms, W):
    '''
        The backward transformation operator J.
        Latex: Eq. 3.12
               List. 3.14
    '''
    if W.ndim == 1:
        tmp = np.reshape(W, atoms.s, order='F')
        F = np.fft.fftn(tmp).flatten(order='F')
    else:
        F = np.empty_like(W, dtype=complex)
        for i in range(W.shape[0]):
            tmp = np.reshape(W[i], atoms.s, order='F')
            F[i] = np.fft.fftn(tmp).flatten(order='F')
    return 1 / atoms.sn * F


def Idag(atoms, W):
    '''
        The Hermitian conjugate forward transformation operator Idag.
        Latex: Eq. 3.13
               List. 3.15
    '''
    if W.ndim == 1:
        tmp = np.reshape(W, atoms.s, order='F')
        full = np.fft.fftn(tmp).flatten(order='F')
        F = full[atoms.active]
    else:
        F = np.empty((np.size(W, 0), len(atoms.active[0])), dtype=complex)
        for i in range(len(W)):
            tmp = np.reshape(W[i], atoms.s, order='F')
            full = np.fft.fftn(tmp).flatten(order='F')
            F[i] = full[atoms.active]
    return F


def Jdag(atoms, W):
    '''
        The Hermitian conjugate backward transformation operator Jdag.
        Latex: Eq. 3.14
               List. 3.16
    '''
    if W.ndim == 1:
        tmp = np.reshape(W, atoms.s, order='F')
        Finv = np.fft.ifftn(tmp).flatten(order='F')
    else:
        Finv = np.empty_like(W, dtype=complex)
        for i in range(len(W)):
            tmp = np.reshape(W[i], atoms.s, order='F')
            Finv[i] = np.fft.ifftn(tmp).flatten(order='F')
    return Finv
