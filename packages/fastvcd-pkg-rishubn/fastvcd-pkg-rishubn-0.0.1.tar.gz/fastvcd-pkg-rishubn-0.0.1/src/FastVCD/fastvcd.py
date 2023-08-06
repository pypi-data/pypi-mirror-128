import re
from bisect import bisect_right
class Signal:
    def __init__(self) -> None:
        self.indices = []
        self.data = []

    def add(self, i, d):
        self.indices.append(i)
        self.data.append(d)
    
    def __getitem__(self, i):
        x = bisect_right(self.indices, i)
        return self.data[x-1]


class FastVCD:
    def __init__(self, vcd):
        self.signals = self.parse_vcd(vcd)

    def parse_vcd(self, f):
        signals = {"id": {}, "name":{}}
        hier = []
        t = 0
        with open(f, 'r') as vcd:
            for line in vcd:
                if "$var" in line:
                    l = line.split(" ")
                    s = Signal()
                    sc = '.'.join(hier)
                    if len(l) == 7:
                        name = f'{sc}.{l[4]}{l[5]}'
                    else:
                        name = f'{sc}.{l[4]}'
                    if l[3] in signals["id"]:
                        signals["name"][name] = signals["id"][l[3]]
                    else:
                        signals["id"][l[3]] = s
                        signals["name"][name] = s
                elif "$scope" in line:
                    l = line.split(" ")
                    hier.append(l[2])
                elif "$upscope" in line:
                    hier.pop()
                elif '$date' in line or '$version' in line:
                    while '$end' not in next(vcd):
                        pass
                elif '$timescale' in line:
                    l = next(vcd)
                    self.timescale = l.strip()
                    while '$end' not in next(vcd):
                        pass
                elif line[0] == '#':
                    t = int(line[1:].strip())
                elif line.isspace() or line[0] == '$':
                    pass
                else:
                    l = line.strip()
                    id = l[1:]
                    x = l[0] if l[0] == 'x' else int(l[0])
                    signals['id'][id].add(t, x)
        return signals


signals = FastVCD('trace_0.vcd')
