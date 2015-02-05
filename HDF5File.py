import h5py

class HDF5File:
  def __init__(self, filename):
    self.name = filename
    # Open HDF5 File
    f = h5py.File(filename)
    # Copy actual samples into a simple array
    self.emgData = f["RawData/Samples"][:].transpose()[0]

    # Open the boundaries .txt
    f = open(filename + '.txt')
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
    self.trialIndices = [map(VideoToEMG, rep) for rep in boundaries]
    self.trials = [self.emgData[l:r] for l,r in self.trialIndices]
      
