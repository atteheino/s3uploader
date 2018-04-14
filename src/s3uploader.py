import boto3
from os import listdir, rename, makedirs
from os.path import isfile, join, realpath, exists
 
def upload(PROFILE, BUCKET, KEY_PREFIX, FOLDER):
    list_of_files = get_list_of_files(FOLDER)
    session = boto3.Session(profile_name=PROFILE)
    s3 = session.resource('s3')
    for f in list_of_files:
        upload_to_s3(s3, BUCKET, KEY_PREFIX, f, FOLDER)
        archive(f, FOLDER)
 
def get_list_of_files(folder):
    return [f for f in listdir(folder) if isfile(join(folder, f))]
 
def upload_to_s3(s3, bucket, key_prefix, file_name, folder):
    s3.meta.client.upload_file(  join(folder, file_name),
                                        bucket,
                                        key_for_object(file_name, key_prefix))
 
def key_for_object(file_name, prefix):
    return "{}/{}".format(prefix, file_name)
 
def archive(file_name, folder):
    archive_folder = realpath(join(folder, 'archive'))
    print("Archived: {} to {}".format(file_name, archive_folder))
    if not exists(archive_folder): makedirs(archive_folder)
    rename( realpath(join(folder, file_name)),
            realpath(join(archive_folder, file_name)))