import os
import logging
import sys, getopt
import boto3
import requests
import time
import csv
from botocore.client import Config
from botocore.exceptions import ClientError

logger = logging.getLogger('s3-to-minio')
s3_client = boto3.client('s3')

LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()


class Main():

    cvs_file = ''
    minio_URL = ''
    minio_access_key = ''
    minio_secret_key = ''

    @staticmethod
    def log_level(level):
        logging.basicConfig(level=getattr(logging, level))

    @staticmethod
    def upload_to_minio(bucket_name, s3_file):
        basename = os.path.basename(s3_file)
        logger.info('Uploading file {}.'.format(basename))
        try:
            s3 = boto3.resource('s3', endpoint_url=Main.minio_URL, aws_access_key_id=Main.minio_access_key,
                                aws_secret_access_key=Main.minio_secret_key, config=Config(signature_version='s3v4'))
            logger.debug('Checking if the Bucket to upload files exists or not.')
            if (s3.Bucket(bucket_name) in s3.buckets.all()) == False:
                logger.info('Bucket not Found. Creating Bucket.')
                s3.create_bucket(Bucket=bucket_name)
            logger.debug('Uploading file to bucket {} minio {}'.format(bucket_name, Main.minio_URL))
            s3.Bucket(bucket_name).upload_file(basename, s3_file)
        except ClientError as e:
            logger.error("Cannot connect to the minio {}. Please vefify the Credentials.".format(Main.minio_URL))
        except Exception as e:
            logger.info(e)

    @staticmethod
    def process_the_csv_file(csv_file_path):
        with open(csv_file_path) as csv_file:
            s3 = boto3.resource('s3')
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                bucketname = row[0]
                s3_file = row[1]
                if s3_file.startswith('/'):
                    s3_file = s3_file[1:]
                #dirname = os.path.dirname(s3_file)
                basename = os.path.basename(s3_file)
                try:
                    s3.Bucket(bucketname).download_file(s3_file, basename)
                    Main.upload_to_minio(bucketname, s3_file)
                    os.remove(basename)
                except Exception as e:
                    logger.info(e)

    @staticmethod
    def application(s3_bucket, folder):
        try:
            Main.download_from_s3_bucket(s3_bucket,folder)
        except Exception as e:
            logger.error(e)

    @staticmethod
    def main(argv):
        help_string = 's3-to-minio.py -c <cvs file path> -m <minio URL> -a <minio access ket> -s <minio secret key>'
        try:
            opts, args = getopt.getopt(argv,"hc:m:a:s:",["cvs=","minio=","access=","secret="])
        except getopt.GetoptError:
            print (help_string)
            sys.exit(2)
        for opt, arg in opts:
            if opt == '-h':
                print (help_string)
                sys.exit()
            elif opt in ("-c", "--cvs"):
                Main.cvs_file = arg
            elif opt in ("-m", "--minio"):
                Main.minio_URL = arg
            elif opt in ("-a", "--access"):
                Main.minio_access_key = arg
            elif opt in ("-s", "--secret"):
                Main.minio_secret_key = arg

        Main.log_level(LOG_LEVEL)
        logger.info(Main.cvs_file)
        logger.info(Main.minio_URL)
        logger.info(Main.minio_access_key)
        logger.info(Main.minio_secret_key)

        #Main.application(s3_bucket, download_folder)
        Main.process_the_csv_file(Main.cvs_file)

if __name__ == "__main__":
    Main.main(sys.argv[1:])