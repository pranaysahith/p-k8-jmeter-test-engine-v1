import os
import logging
import logging.config
from pythonjsonlogger import jsonlogger
from datetime import datetime;
import requests
import time
from os import listdir
from os.path import isfile, join
from minio_service import MinioService


class ElkJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(ElkJsonFormatter, self).add_fields(log_record, record, message_dict)
        log_record['level'] = record.levelname
        log_record['logger'] = record.name

logging.config.fileConfig('logging.conf')
logger = logging.getLogger('file processor')

TGT_URL = os.getenv('TARGET_MINIO_URL', 'http://127.0.0.1:9000')
TGT_ACCESS_KEY = os.getenv('TARGET_MINIO_ACCESS_KEY', 'test')
TGT_SECRET_KEY = os.getenv('TARGET_MINIO_SECRET_KEY', 'test@123')
TGT_BUCKET = os.getenv('TARGET_MINIO_BUCKET', 'output')

OUTPUT_PATH = os.getenv('OUTPUT_PATH', '/usr/share/Test/output/')
REPORT_PATH = os.getenv('OUTPUT_PATH', '/usr/share/Test/report/')
REPORT_BUCKET = os.getenv('REPORTS_MINIO_BUCKET', 'reports')

POD_NAME = os.getenv('POD_NAME', 'file-processor-pod')

LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()

SHELL_ACCESS = True


class Main():


    def __init__(self):
        self.minio = MinioService(TGT_URL, TGT_ACCESS_KEY, TGT_SECRET_KEY)
    
    @staticmethod
    def log_level(level):
        logging.basicConfig(level=getattr(logging, level))
    
    def upload_to_minio(self, bucket, file_path, filename):
        try:
            self.minio.create_bucket(bucket)
            file_to_upload = file_path + filename
            self.minio.upload_file(bucket, file_to_upload, filename)
        except Exception as e:
            logger.info(e)
    
    def download_from_minio(self):
        name = os.getenv("INPUT_FILE_PATH", "Macros.xls")
        bucket = name.split(".")[-1]
        input_dir = "/usr/share/Test/input"
        self.minio.download_file(bucket, name, input_dir)
    
    def upload_results(self):
        try:
            for f in listdir(OUTPUT_PATH):
                if isfile(join(OUTPUT_PATH, f)):
                    logger.info(f)
                    main.upload_to_minio(TGT_BUCKET, OUTPUT_PATH, f)
            report_file = POD_NAME + '.tar.gz'
            os.system('tar -zcvf ' + report_file + ' /usr/share/Test/report/')
            Main.upload_to_minio(REPORT_BUCKET, '/', report_file)
            exit(0)
        except Exception as e:
            logger.error(e)
    
    def main(self):
        Main.log_level(LOG_LEVEL)
        self.download_from_minio()
        os.system('/usr/share/Test/launch.sh')
        self.upload_results()

if __name__ == "__main__":
    main = Main()
    main.main()
