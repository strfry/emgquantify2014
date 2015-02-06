#!/usr/bin/env python
# a bar plot with errorbars

# %matplotlib inline

import numpy as np
import matplotlib.pyplot as plt
import h5py
import sys
import os

# path = 'C:\\Users\\KOM\\Desktop\\EMG_Praktikumsgruppe\\messungen\\'
path = './'
#filename = "florian_12kg_2014.12.15.hdf5"
#filename = "record_florian_7500g_max.hdf5"
#filename = "florian_10kg_stehen_2014.12.19.hdf5"
#filename = "tobias_5kg.hdf5"
filename = sys.argv[1]

plot_basename = "plots/" + os.path.basename(filename).replace(".hdf5", "")

# Open HDF5 File
f = h5py.File(path + filename)
# Copy actual samples into a simple array
emgData = f["RawData/Samples"][:].transpose()[0]

# Open the boundaries .txt
f = open(path + filename + '.txt')
# Split into an array of int pairs
boundaries = [map(int, line.split('\t')) for line in f]

# Markers of begin and end in EMG sample space
emgBegin, emgEnd = boundaries.pop(0)
# Markers in video frame space
videoBegin, videoEnd = boundaries.pop(0)

if emgEnd < videoEnd:
  print "Warning: emgEnd < videoEnd: EMG boundaries in .txt are probably missing"

# Calculate conversion factor from video frame to EMG sample
convert=float(emgEnd - emgBegin)/(videoEnd - videoBegin);

# Convert indices of each repetition to EMG sample space
def VideoToEMG(frame): return int((frame - videoBegin) * convert + emgBegin)
repIndices = [map(VideoToEMG, rep) for rep in boundaries]




NFFT = 256

def plot_fftsum(indices):
  sum = np.zeros(NFFT)
  for l,r in indices:
    data = emgData[l:r]
    data = np.append(data, [0] * max(0, NFFT - (r-l)))
    begin = (len(data) - NFFT) / 2
    data = data[begin:begin+NFFT]
    data = data * np.hanning(NFFT)
    sum += data

  # Normalize
  sum = sum / len(indices) / NFFT

  Y = np.fft.rfft(sum, n=NFFT)
  Y = abs(Y)
  plt.plot(Y)

from mpltools import style
print style.available
style.use('mystyle')

plt.subplot(311)
plot_fftsum(repIndices[1:4])
plt.subplot(312)
middle = len(repIndices) / 2
plot_fftsum(repIndices[middle-2 : middle+2])
plt.ylabel("Intensity (mV)")
plt.subplot(313)
plot_fftsum(repIndices[-4:-1])

plt.xlabel("Frequency (Hz)")

plt.savefig(plot_basename + "-3-freq.pdf", format='pdf')

plt.show()

plot_fftsum(repIndices[1:4])
middle = len(repIndices) / 2
plot_fftsum(repIndices[middle-2 : middle+2])
plot_fftsum(repIndices[-4:-1])

plt.legend( ('First 3 trials', 'Middle 3 trials', 'Last 3 trials') )
plt.xlabel("Frequency (Hz)")
plt.ylabel("Intensity (mV)")

plt.savefig(plot_basename + "-3-ampl.pdf", format='pdf')

plt.show()
