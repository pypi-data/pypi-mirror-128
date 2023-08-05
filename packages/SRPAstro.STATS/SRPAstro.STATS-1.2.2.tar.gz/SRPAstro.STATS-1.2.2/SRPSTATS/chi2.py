""" Utility functions and classes for SRP

Context : SRP
Module  : Stats
Version : 1.0.0
Author  : Stefano Covino
Date    : 31/07/2020
E-mail  : stefano.covino@inaf.it
URL:    : http://www.merate.mi.astro.it/utenti/covino

Usage   : chi2(m,o,eo)
            m are the model data
            o are the observations
            eo are the 1sigma errors for the observations

History : (31/07/2020) First version.
"""



def chi2 (m,o,eo):
    c2 = ((m-o)/eo)**2
    if len(c2.shape) == 2:
        return c2.sum(axis=1)
    else:
        return c2.sum()
