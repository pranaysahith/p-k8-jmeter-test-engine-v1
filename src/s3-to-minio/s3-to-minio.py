import os
import logging
import sys, getopt
import boto3
import requests
import time
from botocore.client import Config
from botocore.exceptions import ClientError

logger = logging.getLogger('s3-to-minio')
s3_client = boto3.client('s3')
folder = '/home/harut/input/'
S3_BUCKET = 'k8-jmeter-test-engine-data'

LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()

class Main():

    @staticmethod
    def log_level(level):
        logging.basicConfig(level=getattr(logging, level))

    @staticmethod
    def download_from_s3_bucket(bucket_name, folder_path):

        try:
            s3 = boto3.resource('s3')
            #logger.debug('Check if the Bucket {} exists'.format(SRC_BUCKET))
            if (s3.Bucket(bucket_name) in s3.buckets.all()) == False:
                logger.info('Bucket {} not found.'.format(SRC_BUCKET))
                return
            logger.info('Bucket {} found.'.format(bucket_name))    
            bucket = s3.Bucket(bucket_name)

            for objs in bucket.objects.all():
                logger.info(objs.key)
                path=folder_path+os.sep.join(objs.key.split(os.sep)[:-1])
                try:
                    if not os.path.exists(path):
                        os.makedirs(path)
                    bucket.download_file(objs.key, folder_path+objs.key)
                except FileExistsError as fe:                          
                    logger.error(objs.key+' exists')

        except Exception as e:
            logger.error(e)
          

    @staticmethod
    def application(inputfile):
        try:
            #Main.download_from_s3_bucket(S3_BUCKET,'/tmp/')
            Main.download_from_s3_bucket(S3_BUCKET,folder)
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