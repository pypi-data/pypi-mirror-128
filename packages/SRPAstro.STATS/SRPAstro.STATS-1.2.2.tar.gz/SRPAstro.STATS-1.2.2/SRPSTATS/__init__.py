""" 

Context : SRP
Module  : Statistics
Author  : Stefano Covino
Date    : 18/11/2021
E-mail  : stefano.covino@brera.inaf.it
URL     : http://www.me.oa-brera.inaf.it/utenti/covino


Usage   : to be imported

Remarks :

History : (28/10/2010) First version.
        : (30/04/2011) ChiSqIncrement.
        : (19/02/2012) ScoreatPercentile.
        : (27/08/2012) Faster sigma clipping for frames.
        : (04/03/2013) MAD.
        : (04/04/2013) XCorr_1D.
        : (07/06/2013) FTest.
        : (22/12/2014) RebinData.
        : (08/11/2015) StDev.
        : (02/11/2016) FourierPeriodogram.
        : (04/10/2019) Bayes factor.
        : (29/01/2020) GP and FT library.
        : (08/04/2020) Stand-alone package and MCMC library.
        : (31/07/2020) chi2 and SSE.
        : (13/08/2020) p-value and Bayes p-value
        : (21/08/2020) ptmcee_run
        : (19/11/2020) pandas based CCF.
        : (11/12/2020) Minor correction.
        : (21/01/2021) Minor correction in emcee_run and ptemcee_run.
        : (12/05/2021) Correction for pypi effective download.
        : (18/05/2021) Improved ptemcee_run.
        : (19/05/2021) Improved emcee_run
        : (03/06/2021) Bug corrections in porting to SRPSTATS.
        : (12/11/2021) Error condition intercepted in MCMC.
        : (18/11/2021) Minor correction to Gaussian sample generation.
"""


__version__ = '1.2.2'


__all__ = ['AsymmetricGaussianDistrib', 'AverIterSigmaClipp', 
		'AverSigmaClippFrame',  'AverSigmaClippFrameFast', 
		'BayesFactor', 'Bayespvalue', 'chi2', 'Pandas_CCF', 
		'ChSqIncrement', 'CoordDistanceMinimization', 'FT', 'FTest', 
		'GenFitPars', 'GenGaussSet', 'GP', 'MAD', 'MCMC', 'pvalue', 
		'RebinData', 'ScoreatPercentile', 'SSE', 'StDev', 'XCorr_1D', 
		'WeightedMean', 'WeightedMeanFrame']

