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

LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()


class Main():

    minio_URL = ''
    minio_access_key = ''
    minio_secret_key = ''
    minio_bucket = ''

    @staticmethod
    def log_level(level):
        logging.basicConfig(level=getattr(logging, level))

    @staticmethod
    def upload_to_minio(file_path, filename):

        try:
            logger.info('Uploading file {}.'.format(filename))

            s3 = boto3.resource('s3', endpoint_url=Main.minio_URL, aws_access_key_id=Main.minio_access_key,
                                aws_secret_access_key=Main.minio_secret_key, config=Config(signature_version='s3v4'))
            logger.debug('Checking if the Bucket to upload files exists or not.')
            if (s3.Bucket(Main.minio_bucket) in s3.buckets.all()) == False:
                logger.info('Bucket not Found. Creating Bucket.')
                s3.create_bucket(Bucket=Main.minio_bucket)
            logger.debug('Uploading file to bucket {} minio {}'.format(Main.minio_bucket, Main.minio_URL))
            file_to_upload = file_path + filename
            s3.Bucket(Main.minio_bucket).upload_file(file_to_upload, filename)
        except ClientError as e:
            logger.error("Cannot connect to the minio {}. Please vefify the Credentials.".format(Main.minio_URL))
        except Exception as e:
            logger.info(e)


    @staticmethod
    def download_from_s3_bucket(bucket_name, folder_path):

        try:
            s3 = boto3.resource('s3')
            #logger.debug('Check if the Bucket {} exists'.format(bucket_name))
            if (s3.Bucket(bucket_name) in s3.buckets.all()) == False:
                logger.info('Bucket {} not found.'.format(bucket_name))
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
                    Main.upload_to_minio(folder_path, objs.key)
                except FileExistsError as fe:                          
                    logger.error(objs.key+' exists')

        except Exception as e:
            logger.error(e)

    @staticmethod
    def application(s3_bucket, folder):
        try:
            Main.download_from_s3_bucket(s3_bucket,folder)
        except Exception as e:
            logger.error(e)

    @staticmethod
    def main(argv):
        help_string = 's3-to-minio.py -b <s3 bucket> -f <download folder> -m <minio URL> -i <minio bucket> -a <minio access ket> -s <minio secret key>'
        s3_bucket = ''
        download_folder = ''
        try:
            opts, args = getopt.getopt(argv,"hb:f:m:i:a:s:",["s3bucket=","folder=","minio=","mibucket=","access=","secret="])
        except getopt.GetoptError:
            print (help_string)
            sys.exit(2)
        for opt, arg in opts:
            if opt == '-h':
                print (help_string)
                sys.exit()
            elif opt in ("-b", "--s3bucket"):
                s3_bucket = arg
            elif opt in ("-f", "--folder"):
                download_folder = arg
            elif opt in ("-m", "--minio"):
                Main.minio_URL = arg
            elif opt in ("-i", "--mibucket"):
                Main.minio_bucket = arg
            elif opt in ("-a", "--access"):
                Main.minio_access_key = arg
            elif opt in ("-s", "--secret"):
                Main.minio_secret_key = arg

        Main.log_level(LOG_LEVEL)
        logger.info(Main.minio_URL)
        logger.info(Main.minio_bucket)
        logger.info(Main.minio_access_key)
        logger.info(Main.minio_secret_key)

        Main.application(s3_bucket, download_folder)

if __name__ == "__main__":
    Main.main(sys.argv[1:])