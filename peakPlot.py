#!/usr/bin/env python
# Estimate the marker peak region and show the waveform

import numpy as np
import matplotlib.pyplot as plt
import h5py
import sys

filename = sys.argv[1]

# Open HDF5 File
f = h5py.File(filename)
# Copy actual samples into a simple array
emgData = f["RawData/Samples"][:].transpose()[0]

# Open the boundaries .txt
f = open(filename + '.txt')
# Split into an array of int pairs
boundaries = [map(int, line.split('\t')) for line in f]

# Markers of begin and end in EMG sample space
#emgBegin, emgEnd = boundaries.pop(0)
# Markers in video frame space
videoBegin, videoEnd = boundaries.pop(0)


frameRate = 256. / 30

emgStart = int(videoBegin * frameRate)
emgEnd = int(videoEnd * frameRate)

emgEnd = min(len(emgData) - 600, emgEnd)


plt.subplot(211)
l,r = emgStart - 300, emgStart + 600
plt.plot(range(l,r), emgData[l:r])

plt.subplot(212)
l,r = emgEnd - 300, emgEnd + 600

print l,r, len(emgData)
print len(range(l,r)), len(emgData[l:r])

plt.plot(range(l,r), emgData[l:r])

plt.show()
