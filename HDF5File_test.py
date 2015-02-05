from HDF5File import HDF5File
import matplotlib.pyplot as plt

path = 'data/'
filename = "florian_12kg.hdf5"

file1 = HDF5File(path + filename)

plt.plot(file1.emgData, "grey")

for i in range(len(file1.trials)):
    l, r = file1.trialIndices[i]
    plt.plot(range(l, r), file1.trials[i])


plt.show()
