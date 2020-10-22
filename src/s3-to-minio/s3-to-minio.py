import os
import logging
import sys, getopt
import boto3
import requests
import time
from botocore.client import Config
from botocore.exceptions import ClientError

logger = logging.getLogger('file processor')
s3_client = boto3.client('s3')

file_path = '~/input/'
rebuild_path = '/output/Managed/'

SRC_BUCKET = 'k8-jmeter-test-engine-data'

LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()

SHELL_ACCESS = False

class Main():

    @staticmethod
    def log_level(level):
        logging.basicConfig(level=getattr(logging, level))

    @staticmethod
    def download_from_s3_bucket(inputfile):

        try:
            s3 = boto3.resource('s3')
            #logger.debug('Check if the Bucket {} exists'.format(SRC_BUCKET))
            if (s3.Bucket(SRC_BUCKET) in s3.buckets.all()) == False:
                logger.info('Bucket {} not found.'.format(SRC_BUCKET))
                return
            logger.info('Bucket {} found.'.format(SRC_BUCKET))    
            bucket = s3.Bucket(SRC_BUCKET)

            for file in bucket.objects.all(): 
                logger.info(file)
                #path, filename = os.path.split(file.key)
                #obj_file = file_path + filename
                #logger.info('Downloading file {}.'.format(filename))
                #bucket.download_file(file.key, obj_file)
                # we only are intrested in processing the first file if it exists
                #break

            for objs in bucket.objects.all():
                print(objs.key)
                path='/tmp/'+os.sep.join(objs.key.split(os.sep)[:-1])
                try:
                    if not os.path.exists(path):
                        os.makedirs(path)
                    bucket.download_file(objs.key, '/tmp/'+objs.key)
                except FileExistsError as fe:                          
                    print(objs.key+' exists')


        except ClientError as e:
            logger.error("Cannot Connect to {}. Please Verify your credentials.".format(SRC_BUCKET))
            logger.error(e)
        except Exception as e:
            logger.error(e)

    @staticmethod
    def download_dir(prefix, local, bucket, client=s3_client):
        """
        params:
        - prefix: pattern to match in s3
        - local: local path to folder in which to place files
        - bucket: s3 bucket with target contents
        - client: initialized s3 client object
        """
        keys = []
        dirs = []
        next_token = ''
        base_kwargs = {
            'Bucket':bucket,
            'Prefix':prefix,
        }
        while next_token is not None:
            kwargs = base_kwargs.copy()
            if next_token != '':
                kwargs.update({'ContinuationToken': next_token})
            results = client.list_objects_v2(**kwargs)
            contents = results.get('Contents')
            for i in contents:
                k = i.get('Key')
                if k[-1] != '/':
                    keys.append(k)
                else:
                    dirs.append(k)
            next_token = results.get('NextContinuationToken')
        for d in dirs:
            dest_pathname = os.path.join(local, d)
            if not os.path.exists(os.path.dirname(dest_pathname)):
                os.makedirs(os.path.dirname(dest_pathname))
        for k in keys:
            dest_pathname = os.path.join(local, k)
            if not os.path.exists(os.path.dirname(dest_pathname)):
                os.makedirs(os.path.dirname(dest_pathname))
            client.download_file(bucket, k, dest_pathname)
          

    @staticmethod
    def application(inputfile):
        try:
            Main.download_from_s3_bucket(inputfile)
            #Main.download_dir('/',file_path,SRC_BUCKET)
        except Exception as e:
            logger.error(e)

    @staticmethod
    def main(argv):
        filename = ''
        try:
            opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
        except getopt.GetoptError:
            print ('test.py -i <filename>')
            sys.exit(2)
        for opt, arg in opts:
            if opt == '-h':
                print ('test.py -i <filename>')
                sys.exit()
            elif opt in ("-i", "--ifile"):
                filename = arg

        Main.log_level(LOG_LEVEL)
        Main.application(filename)

if __name__ == "__main__":
    Main.main(sys.argv[1:])