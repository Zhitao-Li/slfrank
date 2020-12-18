import numpy as np
import matplotlib.pyplot as plt
from . import transform


def plot_rf(b1, m=1000, ptype='ex', phase='linear',
            omega_range=[-np.pi, np.pi],
            linewidth=3, fontsize='x-large', labelsize='large'):
    figs = []
    n = len(b1)
    fig, ax = plt.subplots()
    ax.plot(b1.real, label=r'$B_{1, \mathrm{x}}$', linewidth=linewidth)
    ax.plot(b1.imag, label=r'$B_{1, \mathrm{y}}$', linewidth=linewidth)
    ax.set_title(r'$B_1$ (Energy={0:.3g}, Peak={1:.3g})'.format(
        np.sum(np.abs(b1)**2), np.max(np.abs(b1))), fontsize=fontsize)
    ax.set_xlabel('Time', fontsize=fontsize)
    ax.legend(fontsize=fontsize)
    ax.yaxis.set_tick_params(labelsize=labelsize)
    ax.xaxis.set_tick_params(labelsize=labelsize)
    figs.append(fig)

    omega = np.linspace(omega_range[0], omega_range[1], m)
    psi_z = np.exp(-1j * np.outer(omega, np.arange(n)))
    a, b = transform.forward_slr(b1)
    alpha = psi_z @ a
    beta = psi_z @ b

    if ptype == 'se':
        m_xy = beta**2
        m_xy *= np.exp(1j * omega * (n - 1))
        fig, ax = plt.subplots()
        ax.set_title(r'$M_{\mathrm{xy}}$')
        ax.set_xlabel(r'$\omega$ [radian]')
        ax.plot(omega, np.real(m_xy), label=r'$M_{\mathrm{x}}$', linewidth=linewidth)
        ax.plot(omega, np.imag(m_xy), label=r'$M_{\mathrm{y}}$', linewidth=linewidth)
        ax.legend(fontsize=fontsize)
        ax.yaxis.set_tick_params(labelsize=labelsize)
        ax.xaxis.set_tick_params(labelsize=labelsize)
        figs.append(fig)
    else:
        m_xy = 2 * alpha.conjugate() * beta
        m_z = np.abs(alpha)**2 - np.abs(beta)**2
        if phase == 'linear':
            m_xy *= np.exp(1j * omega * n / 2)

        fig, ax = plt.subplots()
        ax.set_title(r'$|M_{\mathrm{xy}}|$', fontsize=fontsize)
        ax.set_xlabel(r'$\omega$ [radian]', fontsize=fontsize)
        ax.plot(omega, np.abs(m_xy), linewidth=linewidth)
        ax.yaxis.set_tick_params(labelsize=labelsize)
        ax.xaxis.set_tick_params(labelsize=labelsize)
        figs.append(fig)

        fig, ax = plt.subplots()
        ax.set_title(r'$\angle M_{\mathrm{xy}}$', fontsize=fontsize)
        ax.set_xlabel(r'$\omega$ [radian]', fontsize=fontsize)
        ax.plot(omega, np.angle(m_xy), linewidth=linewidth)
        ax.yaxis.set_tick_params(labelsize=labelsize)
        ax.xaxis.set_tick_params(labelsize=labelsize)
        figs.append(fig)

        fig, ax = plt.subplots()
        ax.set_title(r'$M_{\mathrm{z}}$', fontsize=fontsize)
        ax.set_xlabel(r'$\omega$ [radian]', fontsize=fontsize)
        ax.plot(omega, m_z, linewidth=linewidth)
        ax.yaxis.set_tick_params(labelsize=labelsize)
        ax.xaxis.set_tick_params(labelsize=labelsize)
        figs.append(fig)

    return figs
