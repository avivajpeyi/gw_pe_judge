from effective_spins.priors_conditional_on_xeff import p_param_and_xeff
import numpy as np
from bilby.core.prior import Uniform, PriorDict
from itertools import combinations
from deep_gw_pe_followup.restricted_prior.conversions import calc_xeff
import pandas as pd


ISOTROPIC_SPIN_PRIOR = PriorDict(dict(
    a1=Uniform(0, 1),
    a2=Uniform(0, 1),
    q=Uniform(0, 1),
    cos2=Uniform(-1, 1)
))
KWGS = dict(init_a1a2qcos2_prior=ISOTROPIC_SPIN_PRIOR, param_key='q')
REPETITIONS = 100
PTSTR = "pi(q,xeff| {} )"


def print_isotropic_spin_qxeff_prior_odds(pts):
    assert len(pts) >  1, "Incorrect q, xeff provided"

    print("Isotropic Prior odds: ")
    for combo in list(combinations(pts.keys(),r=2)):
        pt0, pt1 = pts[combo[0]], pts[combo[1]]
        o = _calc_prior_odds(pt0, pt1)
        print(f">>> {PTSTR.format(combo[0])}/{PTSTR.format(combo[1])} = {o}")



def _calc_prior_odds(pt0, pt1):
    odds = []
    for i in range(REPETITIONS):
        pi_0 = p_param_and_xeff(param=pt0['q'], xeff=pt0['xeff'], **KWGS)
        pi_1 = p_param_and_xeff(param=pt1['q'], xeff=pt1['xeff'], **KWGS)
        odds.append(pi_0/pi_1)
    return f"{np.mean(odds):.2f} +/- {np.std(odds):.2f}"



def get_isotropic_spin_prior_samples(n=10000):
    prior = ISOTROPIC_SPIN_PRIOR.copy()
    prior['cos1'] = Uniform(-1, 1)
    s = pd.DataFrame(prior.sample(n))
    xeff = calc_xeff(a1=s.a1, a2=s.a2, cos1=s.cos1, cos2=s.cos2, q=s.q)
    return pd.DataFrame(dict(q=s.q, xeff=xeff))
