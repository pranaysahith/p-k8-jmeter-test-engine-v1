import os
import logging
import sys, getopt
import boto3
import requests
import time
from botocore.client import Config
from botocore.exceptions import ClientError

logger = logging.getLogger('file processor')

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
                path, filename = os.path.split(file.key)
                obj_file = file_path + filename
                logger.info('Downloading file {}.'.format(filename))
                bucket.download_file(file.key, obj_file)
                # we only are intrested in processing the first file if it exists
                #break

        except ClientError as e:
            logger.error("Cannot Connect to {}. Please Verify your credentials.".format(SRC_BUCKET))
            logger.error(e)
        except Exception as e:
            logger.error(e)

    @staticmethod
    def application(inputfile):
        try:
            Main.download_from_s3_bucket(inputfile)
        except:
            logger.error('Could not connect to Minio {}'.format(SRC_BUCKET))

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