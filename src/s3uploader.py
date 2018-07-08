import boto3
from os import remove, listdir
from os.path import isfile, join, realpath, exists, split

def upload_files_from_directory(PROFILE, BUCKET, FOLDER):
    list_of_files = get_list_of_files(FOLDER)
    session = boto3.Session(profile_name=PROFILE)
    s3 = session.resource('s3')
    for f in list_of_files:
        print("Uploading {} to S3".format(f))
        upload_to_s3(s3, BUCKET, f, FOLDER)
        remove(join(FOLDER, f))


def upload(PROFILE, BUCKET, FILE):
    print("Going to try to upload {} to bucket {} with profile {}".format(FILE, BUCKET, PROFILE))
    session = boto3.Session(profile_name=PROFILE)
    s3 = session.resource('s3')
    folder, file_name = split(FILE)
    print(folder, file_name)
    upload_to_s3(s3, BUCKET, file_name, folder)
    remove(FILE)
 
def upload_to_s3(s3, bucket, file_name, folder):
    s3.meta.client.upload_file(join(folder, file_name), bucket, file_name)

def get_list_of_files(folder):
    return [f for f in listdir(folder) if isfile(join(folder, f))]

def key_for_object(file_name, prefix):
    return "{}/{}".format(prefix, file_name)
 
