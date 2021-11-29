import boto3, utils

class Input:
    def __init__(self, file) -> None:
        log = utils.Log()

        if file[:5] == "s3://":
            s3 = utils.S3File(file)
            self.Input = boto3.client('s3').get_object(Bucket=s3.bucket, Key=s3.s3obje)['Body']
        elif file:
            self.Input=open(file,"rb")
        else:
            log.Write(['Input file parameter missing'])

    def read(self, lrecl):
        return self.Input.read(lrecl)


