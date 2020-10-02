from minio import Minio
from minio.error import ResponseError
import random

minioClient = Minio(
    '127.0.0.1:9000',
    access_key='minioadmin',
    secret_key='minioadmin',
    secure=False
)

# List all object paths in bucket that begin with my-prefixname.
objects = minioClient.list_objects('pdf', recursive=True)

# try:
#     data = minioClient.get_object('input', 'JS_Siemens.pdf')
#     with open('JS_Siemens.pdf', 'wb') as file_data:
#         for d in data.stream(32*1024):
#             file_data.write(d)
# except ResponseError as err:
#     print(err)
names = []
for name in objects:
    names.append(name.object_name)

d1 = random.choice(names)
print(d1)
data = minioClient.get_object('pdf', d1)
with open(d1, 'wb') as file_data:
    for d in data.stream(32*1024):
        file_data.write(d)

