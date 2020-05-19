# SPDX-License-Identifier: GPL-2.0+

import os, sys

os.environ["_GFORT2PY_TEST_FLAG"] = "1"

import numpy as np
import gfort2py as gf

import unittest as unittest
    
import subprocess
import numpy.testing as np_test

from contextlib import contextmanager
from io import StringIO
from io import BytesIO

#Decreases recursion depth to make debugging easier
# sys.setrecursionlimit(10)


import pymesa as pym
p=pym.mesa()
defaults = p.defaults

class TestKap(unittest.TestCase):
	def test_ion_basic(self):
		ion=pym.ion.ion(p.defaults)
		ion.getIon(5000.0,10**3,0.02,0.75)

	def test_eval_typical_charge(self):
		ion=pym.ion.ion(p.defaults)
		ion.eval_typical_charge('fe56', {'h1':0.5,'he4':0.5}, 15777.0, 10**1)