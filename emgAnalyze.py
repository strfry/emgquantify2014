#!/usr/bin/env python
# a bar plot with errorbars

# %matplotlib inline

import numpy as np
import matplotlib.pyplot as plt
import h5py

# path = 'C:\\Users\\KOM\\Desktop\\EMG_Praktikumsgruppe\\messungen\\'
path = 'data/'
filename = "florian_12kg.hdf5"
filename = "record_florian_7500g_max.hdf5"
filename = "florian_10kg_stehen2014.12.19_16.10.04.hdf5"
#filename = "tobias_5kg.hdf5"

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

  Y = np.fft.rfft(sum, n=NFFT)
  Y = abs(Y)
  plt.plot(Y)

plt.subplot(311)
plot_fftsum(repIndices[1:6])
plt.subplot(312)
plot_fftsum(repIndices[8:14])
plt.subplot(313)
plot_fftsum(repIndices[-7:-1])


plt.show()
