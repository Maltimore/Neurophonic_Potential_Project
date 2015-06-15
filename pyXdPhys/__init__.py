import numpy as np

class Stimulation:
    def __init__(self,fname,depvar_sort=True):
        self.load_data(fname)
        self.fname = fname
        if depvar_sort:
            self.depvar_sort()

    def load_data(self,fname):
        if fname[-3:] == '.gz':
            import gzip
            fid = gzip.open(fname,'r')
        else:
            fid = open(fname)
        lines = fid.readlines()
        data_trace = [[]]
        data_stim = [[]]
        inside_trace = False
        inside_stimulus = False
        inside_params = False
        depvar = []
        depvar_full = []
        params = dict()
        self.version = lines[0].split(' ')[-1][:-1].strip()
        for lin in lines:
            lin = lin.strip()
            if lin == 'STIMULUS':
                inside_stimulus = True
            if lin == 'END_STIMULUS':
                if inside_stimulus:
                    data_stim.append([])
                inside_stimulus = False

            if self.version in ['2.8.1-1','2.8.0-1','2.8.0-2','2.8.0-3','2.8.0-4','2.8.0-5']:
                #explicit trace delimiter style found in xdphys 2.8.1-1 files
                if lin == 'TRACE':
                    inside_trace = True
                if lin == 'END_TRACE':
                    inside_trace = False
                    data_trace.append([])
            elif self.version in ['2.47']:
                #implicit delimiter style found in xdphys 2.47 files
                if len(lin)==80 and not inside_stimulus:
                    inside_trace = True
                if lin[0:6] == 'depvar' and not inside_stimulus:
                    inside_trace = False
                    data_trace.append([])
                if lin == 'END_RASTERDATA':
                    inside_trace = False
            else:
                raise Exception('unknown xdphys version '+self.version)

            if lin == 'PARAMS':
                inside_params = True
            if lin == 'END_PARAMS':
                inside_params = False
            if inside_params and lin.find('=')>0 and lin[0]!=';':
                p = lin[lin.find('=')+1:].strip()
                try:
                    p = float(p)
                    if np.floor(p) == p:
                        p = int(p)
                except ValueError:
                    pass
                params[lin[0:lin.find('=')]] = p
            if inside_trace:
                data_trace[-1].append(lin)
            if inside_stimulus:
                data_stim[-1].append(lin)
            if lin[0:6] == 'depvar' and len(lin)>16:
                val =  int(lin[lin.find('=')+1:lin.find('<')])
                if params['depvar'] == 'gen' and not val == -6666:
                    val = int(lin.split(';')[1])
                    depvar_full.append([
                        int(lin.split(';')[0].split('<')[1]),
                        int(lin.split(';')[1]),
                        int(lin.split(';')[2]),
                        int(lin.split(';')[3]),
                        int(lin.split(';')[4])]
                        )
                if params['depvar'] == 'gen' and val == -6666:
                    depvar_full.append([-6666,-6666,-6666,-6666,-6666])
                depvar.append(val)

        self.traces = self._str_list_conv(data_trace)
        self.stim = self._str_list_conv(data_stim,channel_1_only=False)
        self.depvar = np.array(depvar)
        self.params = params
        if len(self.traces) > 0:
            self.times = np.arange(0.,float(self.traces.shape[1]))/(
                    float(self.traces.shape[1]))*self.params['Epoch']
        else: self.times = None
        self.clickfile = False
        self.longnoise = False
        if self.params['depvar'] == 'itd (us)':
            self.freqs = self.depvar.copy()
            if ('itd.stim' not in self.params.keys()):
                self.freqs.fill(0.)
                if 'prefs.page' in self.params.keys():
                    if (self.params['prefs.page'+str(self.params['prefs.page'])] == 'click'):
                        self.clickfile = True
                    if (self.params['prefs.page'+str(self.params['prefs.page'])] == 'longnoise'):
                        self.longnoise = True
            elif self.params['itd.stim']=='BB':
                #noise stimulation. TODO: figure out what the ts parameters mean
                self.freqs.fill(0.)
            else:
                self.freqs.fill(self.params['itd.stim'])
            #spontaneous stimulations get marked by -6666
            self.freqs[np.where(self.depvar < -6000)] = -6666
        if self.params['depvar'] == 'bf (Hz)':
            self.freqs = self.depvar
        if self.params['depvar'] == 'gen':
            self.genfile = True
            self.freqs = self.depvar.copy()
            self.depvar_full = np.array(depvar_full)
        else:
            self.genfile = False

        #parse the timestamp as a python datetime if present
        if 'timestamp' in self.params.keys():
            from datetime import datetime
            self.timestamp = datetime.fromtimestamp(
                    self.params['timestamp'])


    def _str_list_conv(self,str_list,channel_1_only=True):
        def parse(lines):
            nums = []
            for lin in lines:
                for n in range(int(len(lin)/4)):
                    nums.append(int(lin[4*n:4*(n+1)],16))
            return nums
        ret = []
        for tra in str_list:
            if len(tra)>0 and ((not channel_1_only) or (tra[1] == 'channel=1')):
                ret.append(parse(tra[2:]))
            if len(tra)>0 and len(tra[1])==80:
                ret.append(parse(tra))
        ret = np.array(ret)
        return ret - (ret > 32767)*65536

    def depvar_sort(self):
        ind = self.depvar.argsort()
        self.depvar = self.depvar[ind]
        #not all files contain the stimulus
        if len(self.stim) == len(self.depvar):
            self.stim = self.stim[ind,:]
        if len(self.traces) == len(self.depvar):
            self.traces = self.traces[ind,:]
        try:
            self.freqs = self.freqs[ind,:]
        except:
            pass

    def write_wav(self,fname=None):
        from scipy.io.wavfile import write
        if fname is None:
            fname = self.fname+'.wav'

        sound = self.traces
        sound = np.hstack((sound,np.zeros(sound.shape)))
        sound = sound.flatten()

        scaled = np.int16(sound/np.max(np.abs(sound)) * 32767)
        write(fname, self.params['adFc'], scaled)
        return sound


def testme():
    stim = Stimulation('/groups/kempter/owldata/170/170.07.4.itd',depvar_sort=False)

if __name__ == '__main__':
    testme()
