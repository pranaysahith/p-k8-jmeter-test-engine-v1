import os
import logging
import logging.config
from pythonjsonlogger import jsonlogger
from datetime import datetime;
import boto3
import requests
import time
from botocore.client import Config
from botocore.exceptions import ClientError
from os import listdir
from os.path import isfile, join

class ElkJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(ElkJsonFormatter, self).add_fields(log_record, record, message_dict)
        log_record['level'] = record.levelname
        log_record['logger'] = record.name

logging.config.fileConfig('logging.conf')
logger = logging.getLogger('file processor')

file_path = '/usr/share/Test/output/'

TGT_URL = os.getenv('TARGET_MINIO_URL', 'http://192.168.99.123:30493')
TGT_ACCESS_KEY = os.getenv('TARGET_MINIO_ACCESS_KEY', 'test')
TGT_SECRET_KEY = os.getenv('TARGET_MINIO_SECRET_KEY', 'test@123')
TGT_BUCKET = os.getenv('TARGET_MINIO_BUCKET', 'output')

LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()

jwt_token = os.getenv("API_TOKEN","YOUR_REBUILD_API_TOKEN")
url = os.getenv("API_URL","https://gzlhbtpvk2.execute-api.eu-west-1.amazonaws.com/Prod/api/rebuild/file")

FILE_TO_PROCESS = os.getenv("FILE_TO_PROCESS", "Reports 1.pdf")

SHELL_ACCESS = True

class Main():

    @staticmethod
    def log_level(level):
        logging.basicConfig(level=getattr(logging, level))

    @staticmethod
    def upload_to_minio(file_path, filename):
        try:
            logger.info('Uploading file {}.'.format(filename))

            s3 = boto3.resource('s3', endpoint_url=TGT_URL, aws_access_key_id=TGT_ACCESS_KEY,
                                aws_secret_access_key=TGT_SECRET_KEY, config=Config(signature_version='s3v4'))
            logger.debug('Checking if the Bucket to upload files exists or not.')
            if (s3.Bucket(TGT_BUCKET) in s3.buckets.all()) == False:
                logger.info('Bucket not Found. Creating Bucket.')
                s3.create_bucket(Bucket=TGT_BUCKET)
            logger.debug('Uploading file to bucket {} minio {}'.format(TGT_BUCKET, TGT_URL))
            file_to_upload = file_path + filename
            s3.Bucket(TGT_BUCKET).upload_file(file_to_upload, filename)
        except ClientError as e:
            logger.error("Cannot connect to the minio {}. Please vefify the Credentials.".format(TGT_URL))
        except Exception as e:
            logger.info(e)

    @staticmethod
    def application():
        #if os.name == 'nt':
        #    file_path = 'C:/GW/files/'
        try:
            for f in listdir(file_path):
                if isfile(join(file_path, f)):
                    logger.info(f)
                    Main.upload_to_minio(file_path, f)
        except Exception as e:
            logger.error(e)

    @staticmethod
    def main():
        Main.log_level(LOG_LEVEL)
        #if os.name == 'nt':
        #    file_path = 'C:/GW/files/'
        #else:
        os.system('/usr/share/Test/launch.sh')
        # os.system('service filebeat start')
        Main.application()
        # let filebeat do his job
        time.sleep(2)

        if SHELL_ACCESS:
            while True:
                time.sleep(5)

if __name__ == "__main__":
    Main.main()
