import numpy as np

from aislab.gnrl import tm
from aislab.gnrl import bf

from aislab.gnrl import *
N = 1e7
tic('--TIC')
for i in np.arange(1,N): pass
toc('--TOC')

tic('--TIC')
tic1('--|--TIC1')
for i in np.arange(1,N): pass
toc1('--|--TOC1')

tic1('--|--TIC1')
tic2('--|--|--TIC2')
for i in np.arange(1,N): pass
toc2('--|--|--TOC2')

tic2('--|--|--TIC2')
tic3('--|--|--|--TIC3')
for i in np.arange(1,N): pass
toc3('--|--|--|--TOC3')

tic3('--|--|--|--TIC3')
tic4('--|--|--|--|--TIC4')
for i in np.arange(1,N): pass
toc4('--|--|--|--|--TOC4')

tic4('--|--|--|--|--TIC4')
tic5('--|--|--|--|--TIC5')
for i in np.arange(1,N): pass
toc5('--|--|--|--|--TOC5')

tic5('--|--|--|--|--TIC5')
for i in np.arange(1,N): pass
toc5('--|--|--|--|--TOC5')
toc4('--|--|--|--|--TOC4')
toc3('--|--|--|--TOC3')
toc2('--|--|--TOC2')

toc1('---TOC1')

toc('---TOC')


tic2('---TIC 3')
tic('------TIC2 31')
for i in np.arange(1,N): pass
toc('------TOC2 31')

tic('------TIC2 32')
for i in np.arange(1,N): pass
toc('------TOC2 32')

toc2('---TOC 3')