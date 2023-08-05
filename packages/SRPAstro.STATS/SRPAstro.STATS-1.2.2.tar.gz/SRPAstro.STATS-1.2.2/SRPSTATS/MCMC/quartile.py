""" Utility functions and classes for SRP

Context : SRP
Module  : Stats.py
Version : 1.0.0
Author  : Stefano Covino
Date    : 10/08/2020
E-mail  : stefano.covino@brera.inaf.it
URL:    : http://www.merate.mi.astro.it/utenti/covino

Usage   : quartile (samples)
        : sampples: outpout of a MCMC chain
        : samples = sampler.chain[:, nburnt:, :].reshape((-1,ndim))

History : (10/08/2020) First version.

"""

import numpy as np


def quartile (samples, perc=[15.9, 50.0, 84.1, 99.]):
    #
    res = np.percentile(samples, perc, axis=0)
    # 
    return res