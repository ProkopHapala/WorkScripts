#!/usr/bin/python

import sys
import os
from aimsUtils import *

name_in='answer.xyz'
if len(sys.argv) > 1:
	name_in=sys.argv[1]

convGeom_xyz2aims( name_in=name_in )
