import sys
sys.path.append('/extra/mccolgan/work')

from spikepy.developer.file_interpreter import FileInterpreter, Trial
import pyXdPhys as xd
import os

class ExampleText(FileInterpreter):
    def __init__(self):
        self.name = 'XDPhys' # this name must be unique
        self.extentions = ['.bf','.itd'] # Spikepy will try this FileInterpreter for files of this extention.
        self.priority = 10 # higher priority means will be used in ambiguous cases
        self.description = 'Files created with XDPhys'

    def read_data_file(self, fullpath):
        # open file and read in the data
        stim = xd.Stimulation(fullpath)
        sampling_freq = float(stim.params['adFc'])

        voltage_traces = stim.traces[:500,:] # must be a list of traces, even if only one trace

        # display_name can be anything, here we just use the filename.
        display_name = os.path.splitext(os.path.split(fullpath)[-1])[0]

        trial = Trial.from_raw_traces(sampling_freq, voltage_traces, 
                origin=fullpath, display_name=display_name)
        return [trial] # need to return a list of trials.
