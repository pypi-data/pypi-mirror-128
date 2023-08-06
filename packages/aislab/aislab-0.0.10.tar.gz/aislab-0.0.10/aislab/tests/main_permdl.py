import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from aislab.dp_feng.decomp import *
from aislab.gnrl.bf import *
from aislab.gnrl.sf import *
from aislab.gnrl.tm import *

wpath = '/home/user/Desktop/Saso/OPEN_MAT/Project/aislab'
sys.path.append(wpath)
os.chdir(wpath)

np.set_printoptions(precision=5, linewidth=100000, threshold=100000000)
pd.options.display.precision = 5
pd.options.display.max_rows = int(1e20)
pd.options.display.max_columns = int(50)

T=7
n=5
d=3
N = n*T + d
Ne = (n - 2)*T
x = rand((N, 1))
w = ones((N, 1))
for k in range(N):
    xs = permdl(x[max(0, N - Ne + 1):], w, T, Ne)

plt.plot(np.hstack((x, w, xs)))
plt.show()
