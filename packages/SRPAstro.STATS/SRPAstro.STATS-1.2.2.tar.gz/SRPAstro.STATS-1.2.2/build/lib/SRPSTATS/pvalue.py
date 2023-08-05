""" Utility functions and classes for SRP

Context : SRP
Module  : Stats
Version : 1.0.0
Author  : Stefano Covino
Date    : 13/08/2020
E-mail  : stefano.covino@inaf.it
URL:    : http://www.merate.mi.astro.it/utenti/covino

Usage   : pvalue(model, data, edata, nfitpars)


History : (13/08/2020) First version.
"""

from SRPSTATS.chi2 import chi2
import scipy.stats as SS


def pvalue (model, data, edata, npars):
    #
    chiquadro = chi2(model,data,edata)
    chi2red = chiquadro/(len(data)-npars)
    #
    return {'chi2':chiquadro, 'chi2red':chi2red, "p-value":1-SS.chi2.cdf(float(chiquadro),len(data)-npars), "dof":len(data)-npars}
#