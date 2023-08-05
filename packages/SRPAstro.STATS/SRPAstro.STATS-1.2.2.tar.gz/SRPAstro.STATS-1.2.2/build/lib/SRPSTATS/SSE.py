""" Utility functions and classes for SRP

Context : SRP
Module  : Stats
Version : 1.0.0
Author  : Stefano Covino
Date    : 31/07/2020
E-mail  : stefano.covino@inaf.it
URL:    : http://www.merate.mi.astro.it/utenti/covino

Usage   : SSE(model, data)


History : (31/07/2020) First version.
"""

#from scipy import stats


def SSE (model, data):
    res = ((data - model)/model)**2
    if len(res.shape) == 2:
        return res.sum(axis=1)
    else:
        return res.sum()