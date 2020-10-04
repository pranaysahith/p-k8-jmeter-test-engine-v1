"""
create and manage buckets
"""
from minio import Minio
import logging


class BucketHandler():

    def __init__(self, minio: Minio):
        super().__init__()
        self.minio = minio

    def create_bucket(self, bucket_name, ignore_if_exists=True):
        """
        creates a bucket with given name
        :param bucket_name: Bucket name
        :param ignore_if_exists: ignores if bucket already exists
        :return: bucket_name
        """
        try:
            bucket_exists = self.minio.bucket_exists(bucket_name)
            if bucket_exists and ignore_if_exists:
                return bucket_name
            elif bucket_exists:
                raise Exception("Bucket already exists")
            self.minio.make_bucket(bucket_name)
            return bucket_name
        except Exception as e:
            logging.error(e)
            raise

    def delete_bucket(self, bucket_name, ignore_if_not_exists=True):
        """
        deletes the bucket with given name
        :param bucket_name: Bucket name
        :param ignore_if_not_exists: ignores delete if bucket is not present
        :return: returns True if successful
        """
        try:
            bucket_exists = self.minio.bucket_exists(bucket_name)
            if not bucket_exists and ignore_if_not_exists:
                return True
            elif not bucket_exists:
                raise Exception("Bucket does not exists")
            self.minio.remove_bucket(bucket_name)
            return True
        except Exception as e:
            logging.error(e)
            raise

    def list_buckets(self):
        """
        lists the buckets
        :return: list of bucket names
        """
        try:
            return self.minio.list_buckets()
        except Exception as e:
            logging.error(e)
            raise 
