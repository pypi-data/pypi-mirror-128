import numpy as np
from scipy.special import erfc

from .exc import lda_slater_x, lda_vwn_c


def get_T(atoms, op, W):
    '''
        Calculate the kinetic energy T.
        Latex: Eq. 2.37
    '''
    F = np.diag(atoms.f)
    T = -0.5 * np.trace(F @ (W.conj().T @ op.L(W)))
    return T


def get_Een(Vreciproc, n):
    '''
       Calculate the electron-ion interaction Een.
       Latex: Eq. 2.38
    '''
    Een = Vreciproc.conj().T @ n
    return Een


def get_Exc(op, n):
    '''
        Calculate the exchange correlation energy Exc.
        Latex: Eq. 2.39
    '''
    exc = lda_slater_x(n)[0] + lda_vwn_c(n)[0]
    Exc = n.conj().T @ op.Jdag(op.O(op.J(exc)))
    return Exc


def get_Ecoul(op, n, phi):
    '''
        Caclulate the Coloumb interaction energy Ecoul.
        Latex: Eq. 2.40 + Eq. 2.41 (as in Eq. 2.49)
    '''
    Ecoul = 0.5 * n.conj().T @ op.Jdag(op.O(phi))
    return Ecoul


def get_Eewald(atoms, gcut=2, gamma=1e-8):
    '''
        Calculate the Ewald energy.
        Latex: Eq. A.12 ff.
    '''
    Natoms = len(atoms.atom)
    tau = atoms.X
    Zvals = atoms.Z
    Omega = atoms.Omega

    LatVecs = atoms.R
    t1 = LatVecs[0]
    t2 = LatVecs[1]
    t3 = LatVecs[2]
    t1m = np.sqrt(np.dot(t1, t1))
    t2m = np.sqrt(np.dot(t2, t2))
    t3m = np.sqrt(np.dot(t3, t3))

    RecVecs = 2 * np.pi * np.linalg.inv(LatVecs.conj().T)
    g1 = RecVecs[0]
    g2 = RecVecs[1]
    g3 = RecVecs[2]
    g1m = np.sqrt(np.dot(g1, g1))
    g2m = np.sqrt(np.dot(g2, g2))
    g3m = np.sqrt(np.dot(g3, g3))

    x = np.sum(Zvals**2)
    totalcharge = np.sum(Zvals)

    gexp = -np.log(gamma)
    nu = 0.5 * np.sqrt(gcut**2 / gexp)

    tmax = np.sqrt(0.5 * gexp) / nu
    mmm1 = int(np.rint(tmax / t1m + 1.5))
    mmm2 = int(np.rint(tmax / t2m + 1.5))
    mmm3 = int(np.rint(tmax / t3m + 1.5))

    Eewald = -nu * x / np.sqrt(np.pi)
    Eewald += -np.pi * totalcharge**2 / (2 * Omega * nu**2)

    dtau = np.empty(3)
    G = np.empty(3)
    T = np.empty(3)
    for ia in range(Natoms):
        for ja in range(Natoms):
            dtau = tau[ia] - tau[ja]
            ZiZj = Zvals[ia] * Zvals[ja]
            for i in range(-mmm1, mmm1 + 1):
                for j in range(-mmm2, mmm2 + 1):
                    for k in range(-mmm3, mmm3 + 1):
                        if (ia != ja) or ((abs(i) + abs(j) + abs(k)) != 0):
                            T = i * t1 + j * t2 + k * t3
                            rmag = np.sqrt(np.sum((dtau - T)**2))
                            Eewald += 0.5 * ZiZj * erfc(rmag * nu) / rmag

    mmm1 = int(np.rint(gcut / g1m + 1.5))
    mmm2 = int(np.rint(gcut / g2m + 1.5))
    mmm3 = int(np.rint(gcut / g3m + 1.5))

    for ia in range(Natoms):
        for ja in range(Natoms):
            dtau = tau[ia] - tau[ja]
            ZiZj = Zvals[ia] * Zvals[ja]
            for i in range(-mmm1, mmm1 + 1):
                for j in range(-mmm2, mmm2 + 1):
                    for k in range(-mmm3, mmm3 + 1):
                        if (abs(i) + abs(j) + abs(k)) != 0:
                            G = i * g1 + j * g2 + k * g3
                            Gtau = np.sum(G * dtau)
                            G2 = np.sum(G**2)
                            x = 2 * np.pi / Omega * np.exp(-0.25 * G2 / nu**2) / G2
                            Eewald += x * ZiZj * np.cos(Gtau)

    return Eewald
