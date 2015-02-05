from HDF5File import HDF5File
import matplotlib.pyplot as plt
import numpy as np


path = "Data/"

filenames = [
  "florian_12kg2014.12.12.hdf5",
  "florian_12kg2014.12.12.hdf5"
  ]

files = [HDF5File(path + name) for name in filenames]


NFFT = 256

def plot_fftsum(file, indices):
  sum = np.zeros(NFFT)
  for l,r in indices:
    data = file.emgData[l:r]
    data = np.append(data, [0] * max(0, NFFT - (r-l)))
    begin = (len(data) - NFFT) / 2
    data = data[begin:begin+NFFT]
    data = data * np.hanning(NFFT)
    sum += data

  Y = np.fft.rfft(sum, n=NFFT)
  Y = abs(Y)
  plt.plot(Y)

for i in range(len(files)):
  plt.subplot(3, len(files), len(files) * 0 + i + 1)
  plot_fftsum(files[i], files[i].trialIndices[1:4])
  plt.subplot(3, len(files), len(files) * 1 + i + 1)
  middle = len(files[i].trials) / 2
  plot_fftsum(files[i], files[i].trialIndices[middle - 2: middle + 2])
  plt.subplot(3, len(files), len(files) * 2 + i + 1)
  plot_fftsum(files[i], files[i].trialIndices[-4:-1])


plt.show()
