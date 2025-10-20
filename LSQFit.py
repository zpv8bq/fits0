import numpy as np
from numpy.linalg import inv
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

xmin = 1.0
xmax = 20.0
npoints = 12
sigma = 0.2
lx = np.zeros(npoints)
ly = np.zeros(npoints)
ley = np.zeros(npoints)
pars = [0.5, 1.3, 0.5]

from math import log


def f(x, par):
    return par[0] + par[1] * log(x) + par[2] * log(x) * log(x)


from random import gauss


def getX(x):  # x = array-like
    step = (xmax - xmin) / npoints
    for i in range(npoints):
        x[i] = xmin + i * step


def getY(x, y, ey):  # x,y,ey = array-like
    for i in range(npoints):
        y[i] = f(x[i], pars) + gauss(0, sigma)
        ey[i] = sigma


# get a random sampling of the (x,y) data points, rerun to generate different data sets for the plot below
getX(lx)
getY(lx, ly, ley)

fig, ax = plt.subplots()
ax.errorbar(lx, ly, yerr=ley)
ax.set_title("Pseudoexperiment")
ax.set_xlabel("x")
ax.set_ylabel("y")
fig.show()

# *** modify and add your code here ***
nexperiments = 10000
a_param = np.zeros(nexperiments)
b_param = np.zeros(nexperiments)
c_param = np.zeros(nexperiments)
chi2 = np.zeros(nexperiments)
chi2_red = np.zeros(nexperiments)

logx = np.log(lx)
A = np.vstack((np.ones_like(logx), logx, logx ** 2)).T
W = np.diag(1.0 / (ley ** 2))
dof = len(lx) - 3

# perform many least squares fits on different pseudo experiments here
for n in range(nexperiments):
    getY(lx, ly, ley)
    cov = inv(A.T @ W @ A)
    params = cov @ (A.T @ W @ ly)
    a_param[n], b_param[n], c_param[n] = params
    y_fit = A @ params
    chi2[n] = np.sum(((ly - y_fit) / ley) ** 2)
    chi2_red[n] = chi2[n] / dof

print("Mean fitted parameters:")
print(f"a = {np.mean(a_param):.4f} ± {np.std(a_param):.4f}")
print(f"b = {np.mean(b_param):.4f} ± {np.std(b_param):.4f}")
print(f"c = {np.mean(c_param):.4f} ± {np.std(c_param):.4f}")
print(f"Mean reduced chi^2 = {np.mean(chi2_red):.3f}")
print(f"Mean  chi^2 = {np.mean(chi2):.3f}")
# fill histograms w/ required data

with PdfPages("LSQFit.pdf") as pdf:
    fig, axs = plt.subplots(2, 2, figsize=(10, 8))
    plt.tight_layout(pad=3.0)
    axs[0, 0].hist(a_param, bins=40, edgecolor='k', color='skyblue')
    axs[0, 0].set_title('Parameter a distribution')
    axs[0, 0].set_xlabel('a')
    axs[0, 0].set_ylabel('Frequency')

    axs[0, 1].hist(b_param, bins=40, edgecolor='k', color='salmon')
    axs[0, 1].set_title('Parameter b distribution')
    axs[0, 1].set_xlabel('b')
    axs[0, 1].set_ylabel('Frequency')

    axs[1, 0].hist(c_param, bins=40, edgecolor='k', color='lightgreen')
    axs[1, 0].set_title('Parameter c distribution')
    axs[1, 0].set_xlabel('c')
    axs[1, 0].set_ylabel('Frequency')

    axs[1, 1].hist(chi2, bins=40, edgecolor='k', color='violet')
    axs[1, 1].set_title('Chi^2 distribution')
    axs[1, 1].set_xlabel('Chi^2')
    axs[1, 1].set_ylabel('Frequency')
    pdf.savefig(fig)
    plt.close(fig)

    fig2, axs2 = plt.subplots(2, 2, figsize=(10, 8))
    plt.tight_layout(pad=3.0)
    h1 = axs2[0, 0].hist2d(a_param, b_param, bins=40, cmap='plasma')
    axs2[0, 0].set_xlabel('a')
    axs2[0, 0].set_ylabel('b')
    axs2[0, 0].set_title('Parameter b vs a')
    fig2.colorbar(h1[3], ax=axs2[0, 0], label='Counts')
    h2 = axs2[0, 1].hist2d(a_param, c_param, bins=40, cmap='plasma')
    axs2[0, 1].set_xlabel('a')
    axs2[0, 1].set_ylabel('c')
    axs2[0, 1].set_title('Parameter c vs a')
    fig2.colorbar(h2[3], ax=axs2[0, 1], label='Counts')
    h3 = axs2[1, 0].hist2d(b_param, c_param, bins=40, cmap='plasma')
    axs2[1, 0].set_xlabel('b')
    axs2[1, 0].set_ylabel('c')
    axs2[1, 0].set_title('Parameter c vs b')
    fig2.colorbar(h3[3], ax=axs2[1, 0], label='Counts')
    axs2[1, 1].hist(chi2_red, bins=40, color='orange', edgecolor='k')
    axs2[1, 1].set_title('Reduced Chi^2 Distribution')
    pdf.savefig(fig2)
    plt.close(fig2)

    fig3 = plt.figure(figsize=(8.5, 11))
    text = f"""Discussion and Observations

    1. The parameters fluctuate around the true value due to the random noise but as we add more points(nexperiments)  the fluctuation becomes smaller. Additionally, as uncertainty increases then the fluctuation increases as well.

    2. We expect a Chi^2 to be the same as dof and the reduced Chi^2 to be around 1. From the calculations we can see that the mean does in fact come close to dof and the reduced Chi^2 to 1. We can also see that as more data points are added and uncertainties reduced then the stdev decreases. Having a Chi^2 reduced to 1 signifies that the fit is good and the uncertainties are accurate. 
"""
    plt.text(0.01, 0.99, text, va='top', fontsize=11, wrap=True, linespacing=1.5)
    plt.axis('off')
    pdf.savefig(fig3)
    plt.close(fig3)

input("hit Enter to exit")
