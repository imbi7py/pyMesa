import pyMesaUtils as pym
import numpy as np

eos_lib, eos_def = pym.loadMod("eos")
const_lib, const_def = pym.loadMod("const")
crlibm_lib, _ = pym.loadMod("crlibm")
chem_lib, chem_def = pym.loadMod("chem")
net_lib, net_def = pym.loadMod("net")
rates_lib, rates_def = pym.loadMod("rates")

ierr=0

crlibm_lib.crlibm_init()
const_lib.const_init(pym.MESA_DIR,ierr)
chem_lib.chem_init('isotopes.data',ierr)
rates_lib.rates_init('reactions.list','jina_reaclib_results_20130213default2',
                    'rate_tables',False,'','','',ierr)


net_lib.net_init(ierr)
eos_lib.eos_init('mesa','','','',False,ierr)
                
                

eos_handle = eos_lib.alloc_eos_handle(ierr)

net_handle = net_lib.alloc_net_handle(ierr)

chem_h1 = chem_def.ih1.get()

net_h1 = net_lib.ih1.get()

Z = 0.00
X = 1.00
abar = 1.0
zbar = 1.0
species = 1
chem_id = np.array([chem_h1])
net_iso = np.array([net_h1])
xa = np.array([1.0])
Rho = 10**8.0
log10Rho = 8.0
T = 10**9
log10T = 9.0
res = np.zeros(eos_def.num_eos_basic_results.get())
d_dlnRho_const_T = np.zeros(eos_def.num_eos_basic_results.get())
d_dlnT_const_Rho = np.zeros(eos_def.num_eos_basic_results.get())
d_dabar_const_TRho = np.zeros(eos_def.num_eos_basic_results.get())
d_dzbar_const_TRho = np.zeros(eos_def.num_eos_basic_results.get())
ierr = 0

eos_res = eos_lib.eosdt_get(
               eos_handle, Z, X, abar, zbar, 
               species, chem_id, net_iso, xa, 
               Rho, log10Rho, T, log10T, 
               res, d_dlnRho_const_T, d_dlnT_const_Rho, 
               d_dabar_const_TRho, d_dzbar_const_TRho, ierr)