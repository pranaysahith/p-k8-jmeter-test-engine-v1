"""
class to handler operations on minio server
"""
import os
import logging
from uuid import uuid4
from minio import Minio
from bucket_handler import BucketHandler

log = logging.getLogger()


class MinioService(BucketHandler):

    def __init__(self, url, access_key, secret_key):
        self.minio = Minio(url, access_key=access_key, secret_key=secret_key, secure=False)
        super().__init__(self.minio)
        
    def create_bucket(self, bucket_name, ignore_if_exists=True):
        """
        creates a bucket with given name
        :param bucket_name: Bucket name
        :param ignore_if_exists: ignores if bucket already exists
        :return: bucket_name
        """
        return super().create_bucket(bucket_name, ignore_if_exists)

    def delete_bucket(self, bucket_name, ignore_if_not_exists=True):
        """
        deletes the bucket with given name
        :param bucket_name: Bucket name
        :param ignore_if_not_exists: ignores delete if bucket is not present
        :return: returns True if successful
        """
        return super().delete_bucket(bucket_name, ignore_if_not_exists)

    def list_buckets(self):
        """
        lists the buckets
        :return: list of bucket names
        """
        return super().list_buckets()

    def upload_file(self, bucket_name, local_file_name, remote_file_name=None):
        """
        uploads a local file to given bucket
        :param bucket_name: bucket name to which file should be uploaded
        :param local_file_name: local file name with absolute path to be uploaded
        :param remote_file_name: file name to be used in bucket
        :return:
        """
        try:
            if not self.minio.bucket_exists(bucket_name):
                raise Exception(f"bucket {bucket_name} does not exists")
            if remote_file_name is None:
                remote_file_name = local_file_name.split("/")[-1]
            self.minio.fput_object(bucket_name, object_name=remote_file_name, file_path=local_file_name)
        except Exception as e:
            log.error(e)

    def download_file(self, bucket_name, file_name, output_dir):
        """
        download a file from the bucket
        :param bucket_name: Bucket name from which file should be downloaded
        :param file_name: file to be downloaded
        :return: returns downloaded file name
        """
        try:
            if not self.minio.bucket_exists(bucket_name):
                raise Exception(f"bucket {bucket_name} does not exists")
            local_file_name = file_name.split("/")[-1]
            self.minio.fget_object(bucket_name, local_file_name, os.path.join(output_dir, local_file_name))
            # with open(os.path.join(output_dir, local_file_name), "wb") as f:
                # f.write(data)
            return local_file_name
        except Exception as e:
            log.error(e)

    def delete_files(self, bucket_name, file_names):
        """
        deletes given list of file names
        :param bucket_name: bucket name
        :param file_names: file names to be deleted
        :return: return True if successful
        """
        try:
            if not self.minio.bucket_exists(bucket_name):
                raise Exception(f"bucket {bucket_name} does not exists")
            for file_name in file_names:
                self.delete_file(bucket_name, file_name)
            return True
        except Exception as e:
            log.error(e)

    def delete_file(self, bucket_name, file_name):
        """
        deletes given list of file names
        :param bucket_name: bucket name
        :param file_name: file name to be deleted
        :return: return True if successful
        """
        try:
            if not self.minio.bucket_exists(bucket_name):
                raise Exception(f"bucket {bucket_name} does not exists")
            self.minio.remove_object(bucket_name, file_name)
            return True
        except Exception as e:
            log.error(e)

    def list_files(self, bucket_name, prefix=None, recursive: bool = None):
        """
        returns list of files in the bucket
        :param bucket_name: Bucket name
        :param prefix: To get files that start with prefix
        :param recursive: To get the files recursively from folders
        :return: Iterator with file names
        """
        try:
            self.is_valid_bucket(bucket_name)
            return self.minio.list_objects(bucket_name, prefix, recursive)
        except Exception as e:
            log.error(e)
            raise

    def is_valid_bucket(self, bucket_name):
        """
        checks if the bucket exists and throws exception if not exists
        :param bucket_name: Bucket name
        :return: True if bucket exists
        """
        try:
            if self.minio.bucket_exists(bucket_name):
                return True
            else:
                raise Exception(f"bucket {bucket_name} does not exists")
        except Exception as e:
            log.error(e)
            raise

    def download_files(self, bucket_name, num_files):
        """
        Download files of a given file type
        :param bucket_name: Bucket name
        :param num_files: Number of files to be downloaded
        :return:
        """
        try:
            file_path = "./"
            log.info("Check if the Bucket {} exists".format(bucket_name))
            files_list = []
            saved_files = 0
            for files in self.list_files(bucket_name):
                path, filename = os.path.split(files.key)
                obj_file = file_path + filename
                log.info("Downloading file {}.".format(filename))
                self.download_file(bucket_name, obj_file)
                files_list.append(obj_file)
                saved_files += 1
                if saved_files == num_files:
                    break
            return files_list
        except Exception as e:
            log.error(e)
