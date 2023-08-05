""" Utility functions and classes for SRP

Context : SRP
Module  : Stats.py
Version : 1.1.0
Author  : Stefano Covino
Date    : 18/05/2021
E-mail  : stefano.covino@inaf.it
URL:    : http://www.merate.mi.astro.it/utenti/covino

Usage   : ptemcee MCMC
        : parameter:
           nwalkers - number of walkers
           ntemps - number of temperatures
           starts - starting positions of the chain
           sigmas - sigmas for the starting Gaussian ball (e.g. 0.1*starts)
           niters - total iterations
           lnprob - log of probability to sample
           args - [parameters for lnprob]


        : Example of code
          def lnlike(theta, t, Io, Do, Ro):
            alpha = np.exp(theta[0])
            beta = np.exp(theta[1])
            deltat = int(round(theta[2]))
            fact = np.exp(theta[3])
            taub = np.exp(theta[4])
            mu = np.exp(theta[5])
            t0b = theta[6]
            factr = np.exp(theta[7])
            t0m = theta[8]    
            taum = np.exp(theta[9])
            ti = t - deltat
            s,i,r,d,n = sird(alpha,beta,mu,deltat,taub,t0b,taum,t0m,0,ti[-1],1)
            ichi = -0.5 * np.sum(np.log(2 * np.pi * (fact*np.sqrt(Io)) ** 2) + (i[ti[0]-1:ti[-1]] - Io*fact) ** 2 / (fact*np.sqrt(Io)) ** 2)
            rchi = -0.5 * np.sum(np.log(2 * np.pi * (factr*fact*np.sqrt(Ro)) ** 2) + (r[ti[0]-1:ti[-1]] - Ro*factr*fact) ** 2 / (factr*fact*np.sqrt(Ro)) ** 2)
            dm = np.round(d)
            dchi = np.sum(poisson.logpmf(dm[ti[0]-1:ti[-1]],Do))
            return ichi + dchi + rchi


            def lnprior(theta):
                #
                prior = 0.
                #
                alpha = np.exp(theta[0])
                beta = np.exp(theta[1])
                deltat = theta[2]
                fact = np.exp(theta[3])
                taub = np.exp(theta[4])
                mu = np.exp(theta[5])
                t0b = theta[6]
                factr = np.exp(theta[7])
                t0m = theta[8]
                taum = np.exp(theta[9]) 
                #
                if alpha < 0.0001 or alpha > 1.:
                    return -np.inf
                #
                #lgb = np.log(gp((0.406/N_0,0.1/N_0),beta))
                #prior += lgb    
                #
                if fact < 1:
                    return -np.inf
                #
                # R0
                if beta*N_0/alpha <= 0.005 or beta*N_0/alpha > 30:
                    return -np.inf
                #
                #lgg = np.log(gp((26,0.1),deltat))
                if deltat < 1 or deltat > 50:
                    return -np.inf
                #
                lgtaub = np.log(gp((26,1),taub))
                prior += lgtaub
                #
                #lgm = np.log(gp((0.014,0.001),mu/fact))
                #prior += lgm
                #
                cfr = mu/(alpha+mu)
                lgc = np.log(gp((0.0114,0.0001),cfr))
                prior += lgc
                #if cfr < 0.001 or cfr > 0.01:
                #    return -np.inf
                lgtb = np.log(gp((60,1),t0b))
                prior += lgtb
                #
                if factr < 1:
                    return -np.inf
                #
                lgtaum = np.log(gp((19,1),taum))
                prior += lgtaum
                #
                lgtm = np.log(gp((90,0.1),t0m))
                prior += lgtm
                #
                return prior
                  

                def lnprob(theta, t, i, d, r):
                    lp = lnprior(theta)
                    if not np.isfinite(lp):
                        return -np.inf
                    return lp + lnlike(theta, t, i, d, r)


History : (21/08/2020) First version.
	    : (21/01/2021) Improved running.
	    : (18/05/2021) Further improvement.
"""

import emcee
import ptemcee
import numpy as np


def ptemcee_run (nwalkers,ntemps,starts,sigmas,niters,lnlike,lnprob,llargs,lpargs,fjump=4,nthin=1):
    
    ndim = len(starts)

    pos = np.array(starts) + np.array(sigmas)*np.random.randn(ntemps,nwalkers,ndim)

    sampler = ptemcee.Sampler(nwalkers, ndim, logl=lnlike, logp=lnprob, ntemps=ntemps, loglargs=llargs, logpargs=lpargs)

    npos = sampler.run_mcmc(pos, niters)
    
    atime = np.mean(sampler.get_autocorr_time())
    
    samples = sampler.chain[:, :, int(fjump*atime)::nthin, :].reshape((-1,ndim))
    
    logevidence = sampler.log_evidence_estimate(fburnin=fjump*atime/niters)

    meanaccfract = np.mean(sampler.acceptance_fraction)

    return {"sampler": sampler, "meanacceptancefraction": meanaccfract, "samples": samples, "logevidence":logevidence, "autocorrtime":atime, "lensamples":len(samples)}


