""" Utility functions and classes for SRP

Context : SRP
Module  : Stats.py
Version : 1.1.0
Author  : Stefano Covino
Date    : 19/05/2021
E-mail  : stefano.covino@inaf.it
URL:    : http://www.merate.mi.astro.it/utenti/covino

Usage   : emcee MCMC
        : parameter:
           nwalkers - number of walkers
           starts - starting positions of the chain
           sigmas - sigmas for the starting Gaussian ball (e.g. 0.1*starts)
           nburnt - ingterations to reach stability
           niters - total iterations
           lnprob - log of probability to sample
           lnargs - [parameters for lnprob]


        : Example of code
          def lnlike(theta, an, So, eSo):
          #
           smod = model(theta, an)
           return -0.5 * np.sum(np.log(2 * np.pi * eSo ** 2) + (So - smod) ** 2 / eSo ** 2)

          def lnprior(theta):
           prior = 0.
           #
           P = np.exp(theta[0])
           Pos = np.degrees(theta[1])
           #
           if P > 1:
            return -np.inf
           #
           if Pos < -180 or Pos > 180:
            return -np.inf
           #
           return prior

           def lnprob(theta, an, So, eSo):
            theta[1] = phaseang(theta[1])
            lp = lnprior(theta)
            if not np.isfinite(lp):
             return -np.inf
            return lp + lnlike(theta, an, So, eSo)

            def model(theta, an):
             anr = np.radians(an)
             #
             P = np.exp(theta[0])
             Pos = theta[1]
             #
             return P*np.cos(2*(Pos-anr))


History : (05/08/2020) First version.
		: (21/01/2021) Improved running.
"""

import emcee
import numpy as np


def emcee_run (nwalkers,starts,sigmas,niters,lnprob,lpargs,fjump=4,nthin=1):
    
    ndim = len(starts)

    pos = emcee.utils.sample_ball(starts,sigmas,nwalkers)

    sampler = emcee.EnsembleSampler(nwalkers, ndim, lnprob, args=lpargs)

    npos = sampler.run_mcmc(pos, niters)
    
    try:
        atime = np.mean(sampler.get_autocorr_time())
    except:
        atime = 0
        
    if np.isnan(atime):
        atime = 0
    
    samples = sampler.get_chain(discard=int(fjump*atime), thin=nthin, flat=True)

    meanaccfract = np.mean(sampler.acceptance_fraction)

    return {"sampler": sampler, "meanacceptancefraction": meanaccfract, "samples": samples, "autocorrtime":atime, "lensamples":len(samples)}

