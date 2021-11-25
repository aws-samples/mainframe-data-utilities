class Param:
    def __init__(self, _param):
        self.param = _param
        self.input = _param['input']
        self.lrecl = _param['lrecl']
        self.print = _param['print']
        self.skip = _param['skip']
        self.max = _param['max']
        self.keyname = _param['keyname']
        self.remlval = _param['rem-low-values']
        
        self.rules = []
        for  paramrule in _param["transf-rule"]:
            self.rules.append(TransformationRule(paramrule["offset"],paramrule["size"],paramrule["hex"],paramrule["transf"]))

    def GetLayout(self, _data):
        if len(self.rules) == 0: return self.param['transf']

        for r in self.rules:
            if _data[r.offset:r.end].hex() == r.hexv:
                return self.param[r.transf]

        return self.param['transf']

    def AddDecPlaces(self, num,dplaces):
        if dplaces == 0: return num

        return num[:len(num)-dplaces] + '.' + num[len(num)-dplaces:]

class TransformationRule:
    def __init__(self, _offset, _size, _hex, _transf):
        self.offset = _offset
        self.size = _size 
        self.end = _offset + _size 
        self.hexv = _hex
        self.transf = _transf
