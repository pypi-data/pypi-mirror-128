""" Utility functions and classes for SRP

Context : SRP
Module  : Stats
Version : 1.0.0
Author  : Stefano Covino
Date    : 13/08/2020
E-mail  : stefano.covino@inaf.it
URL:    : http://www.merate.mi.astro.it/utenti/covino

Usage   : Bayespvalue(model,modelsim data, edata)

Example:
        # Derive a set of models based on the posterior distribution
        S =  model([samples[:,[0]],samples[:,[1]]],dt['angle'])
        scl = np.tile(dt['err_S'],samples[:,[0]].shape[0])
        Ss = S.reshape(-1) + SS.norm.rvs(scale=scl,size=S.size,loc=0)
        Ssim = Ss.reshape(S.shape)

        model: S
	modelsim: Ssim

History : (13/08/2020) First version.
"""

from SRPSTATS.chi2 import chi2
import numpy as np


def Bayespvalue (model, modelsim, data, edata):
    #
    a = chi2(model,modelsim,edata)
    b = chi2(model,data,edata)
    c = (a > b)
    return {"Bayes-p-value": np.count_nonzero(c)/len(c)}
