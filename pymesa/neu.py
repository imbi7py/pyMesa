import pymesa.pyMesaUtils as pym
import numpy as np

from . import const
from . import math
from . import chem

class neu(object):
    def __init__(self, defaults):
        self.const = const.const(defaults)
        self.math = math.math(defaults)
        self.chem = chem.chem(defaults)
        
        self.neu_lib,self.neu_def = pym.loadMod("neu",defaults)
        
        
        self.neu_types = {'pair_neu_type':self.neu_def.pair_neu_type-1,
                    'plas_neu_type':self.neu_def.plas_neu_type-1,
                    'phot_neu_type':self.neu_def.phot_neu_type-1,
                    'brem_neu_type':self.neu_def.brem_neu_type-1,
                    'reco_neu_type':self.neu_def.reco_neu_type-1
        }
                    
        self.neu_rvs = {'ineu':self.neu_def.ineu-1,
                    'idneu_dT':self.neu_def.idneu_dT-1,
                    'idneu_dRho':self.neu_def.idneu_dRho-1,
                    'idneu_dabar':self.neu_def.idneu_dabar-1,
                    'idneu_dzbar':self.neu_def.idneu_dzbar-1
        }

    def getNeu(self,T,Rho,composition, log10_Tlim=7.5):
        log10T = np.log10(T)
        log10Rho = np.log10(Rho)
        
        
        comp = self.chem.basic_composition_info(composition)
    
        abar = comp['abar']
        zbar = comp['zbar']      
        z2bar = comp['z2bar']
        
        flags=np.zeros(self.neu_def.num_neu_types)
        flags[:]=True
        loss=np.zeros(self.neu_def.num_neu_rvs)
        sources=np.zeros((self.neu_def.num_neu_types,self.neu_def.num_neu_rvs))

        res = self.neu_lib.neu_get(T, log10T, Rho, log10Rho, abar, zbar, z2bar, log10_Tlim, flags, loss, sources, 0)
        
        l = res.args['loss']
        s = res.args['sources']
        
        return self.unpackNeuResults(l, s)


    def unpackNeuResults(self, l, s):
        
        loss = {}
        sources = {}
        for k_t, v_t in self.neu_types.items():
            loss[k_t] = l[v_t]
            sources[k_t] = {}
            for k_s, v_s in self.neu_rvs.items():
                sources[k_t][k_s] = s[v_t,v_s]
                
        return loss, sources
