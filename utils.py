import datetime, json, boto3

class ParamReader:
    def __init__(self, sysargv):
        l = Log()
        l.Write()

        desc = {
            'unknown'     : 'Unknown argument ',
            '-local-json' : 'Local Json file  ',
            '-s3url-json' : 'S3 Json file     ' 
            }

        for a in (arg := dict(zip(sysargv[1::2], sysargv[2::2]))):
            if a in desc:
                l.Write([desc[a],a,arg[a]])
            else:
                l.Write([desc['unknown'],a,arg[a]])

        if '-s3-json' in arg:
            bucket = arg['-s3-json'][5:(slash := arg['-s3-json'].find('/',5))]
            s3obje = arg['-s3-json'][slash+1:]
            self.general = json.load(boto3.client('s3').get_object(Bucket=bucket, Key=s3obje)['Body'])            
        elif '-local-json' in arg: 
            with open(arg['-local-json']) as json_file: self.general = json.load(json_file)
        else:
            l.Write(['Error! Sintax must be: python3 ' + sysargv[0] + ' -local-json (path/to/layout.json | -s3-json s3://buketname/filename)'])
            l.Write()
            quit()
        
        self.rules = []
        for  paramrule in self.general["transf-rule"]:
            self.rules.append(TransformationRule(paramrule["offset"],paramrule["size"],paramrule["hex"],paramrule["transf"]))

    def GetLayout(self, _data):
        if len(self.rules) == 0: return self.general['transf']

        for r in self.rules:
            if _data[r.offset:r.end].hex() == r.hexv:
                return self.general[r.transf]

        return self.general['transf']

    def AddDecPlaces(self, value, dplaces):
        if dplaces == 0: return value

        return value[:len(value)-dplaces] + '.' + value[len(value)-dplaces:]

class TransformationRule:
    def __init__(self, _offset, _size, _hex, _transf):
        self.offset = _offset
        self.size = _size 
        self.end = _offset + _size 
        self.hexv = _hex
        self.transf = _transf

class S3File:
    def __init__(self, url) -> None:
        self.bucket = url[5:(slash := url.find('/',5))]
        self.s3obje = url[slash+1:]

class Log:
    def __init__(self) -> None:
        self.start = datetime.datetime.now()
    def Finish(self):
        sec = str(datetime.datetime.now() - self.start)
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f") ,'Seconds', sec)
    def Write (self, content=[]):
        if len(content) > 0:
            print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f") ,'|',' | '.join(content))
        else:
            print("------------------------------------------------------------------")