import boto3
import logging
from os import remove, listdir, walk
from os.path import isfile, join, realpath, exists, split

def upload_files_from_directory(PROFILE, BUCKET, BASE_FOLDER):
    list_of_files = get_list_of_files(BASE_FOLDER)
    for f in list_of_files:
       upload(PROFILE, BUCKET, f, BASE_FOLDER)


def upload(PROFILE, BUCKET, FILE, BASE_FOLDER):
    logger = logging.getLogger(__name__)
    logger.info("Going to try to upload {} to bucket {} with profile {}".format(FILE, BUCKET, PROFILE))
    session = boto3.Session(profile_name=PROFILE)
    s3 = session.resource('s3')
    folder, file_name = split(FILE)
    key_prefix = extract_key(folder, BASE_FOLDER)
    logger.info(folder + ' ' + file_name + ' ' + key_prefix)
    upload_to_s3(s3, BUCKET, file_name, key_prefix, folder)
    remove(FILE)
 
def upload_to_s3(s3, bucket, file_name, key_prefix, folder):
    s3.meta.client.upload_file(join(folder, file_name), bucket, key_for_object(file_name, key_prefix))

def get_list_of_files(folder):
    return [val for sublist in [[join(path, j) for j in folders] for path, subdirs, folders in walk(folder)] for val in sublist]

def key_for_object(file_name, prefix):
    return "{}/{}".format(prefix, file_name)

def extract_key(folder, base_folder):
    return folder.replace(base_folder + '/', '')
 
