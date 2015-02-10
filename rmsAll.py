# %matplotlib inline

import numpy as np
import matplotlib.pyplot as plt
import sys
import os

from mpltools import style
style.use('mystyle')

from HDF5File import HDF5File

path = './Data/'

#plot_basename = "plots/" + os.path.basename(filename).replace(".hdf5", "")

import glob

filenames = glob.glob(path + '*.hdf5')

def rms(x): return np.sqrt(np.mean(np.square(x)))

i = 0
for filename in filenames:
  i = i + 1
  f = HDF5File(filename)

  def transform(trial):
    trial = np.hanning(len(trial)) * trial
    F = np.fft.rfft(trial)
    F = F[5:]
    
    sum = rms(abs(F)) / np.sqrt(len(F))
    
    return sum, len(trial), sum * len(trial)
  
  P, T, A = zip(*map(transform, f.trials))
  

  fig, ax1 = plt.subplots()

  ax1.plot(P)

  ax2 = ax1.twinx()
  ax1.plot(T)
  ax2.plot(A, color='b')

  plt.show()

