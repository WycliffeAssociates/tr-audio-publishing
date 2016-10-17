# =============================================================================
# This function should be triggered when a zip file is uploaded into the
# following location on S3 by translationRecorder:
#
#    <bucket>/inbound/<username>/<commit><project>.zip
# =============================================================================

import os
import tempfile
import zipfile
import json

# AWS-specific imports
import boto3


def handle(event, ctx):
    # For testing purposes only. The printout will be available on cloudwatch
    # logging and it can be used as a test config for the lambda function.
    print json.dumps(event)

    # We know this path because we saw the event printout
    bucket_name = event["Records"][0]["s3"]["bucket"]["name"]
    object_key = event["Records"][0]["s3"]["object"]["key"]

    print "object_key: " + object_key

    # Object key should be...
    # <bucket_name>/inbound/<username>/<commit_hash><project_name>.zip
    #               [0]     [1]        [2]
    username = object_key.split("/")[1]
    commit = object_key.split("/")[2][:10]
    project_name = os.path.splitext(os.path.basename(object_key))[0]

    print "project_name: " + project_name

    # Configuration for unzipping and uploadding
    s3 = boto3.resource("s3")
    zip_file_path = os.path.join(
        tempfile.gettempdir(),
        os.path.basename(object_key)
    )
    extract_target_dir = tempfile.mkdtemp(prefix=project_name)

    # Download file (object_key) from bucket (bucket_name) to a temporary dir
    # (zip_file_path). Temporary dir is virtual (running on AWS), not local.
    s3.meta.client.download_file(bucket_name, object_key, zip_file_path)

    with zipfile.ZipFile(zip_file_path, 'r') as myzip:
        for name in myzip.namelist():
            # "name" is the full path to the file. For example, for this file
            # structure...
            #
            #    6534103f53cmn_eph_audio_ulb.zip
            #       |
            #       --- cmn_eph_audio_ulb
            #        |
            #        --- cmn_ulb_b50_eph_c01_v01_t01.wav
            #        --- cmn_ulb_b50_eph_c01_v02_t01.wav
            #
            # the names would be:
            #    "cmn_eph_audio_ulb/cmn_ulb_b50_eph_c01_v01_t01.wav"
            #    "cmn_eph_audio_ulb/cmn_ulb_b50_eph_c01_v01_t01.wav"
            #
            # Note that splitting the name by the forward slash will give us
            # the project name and the file name separately
            if name.endswith('.wav'):
                # Extract individual "wav" file into a temporary dir
                myzip.extract(name, extract_target_dir)
                # Upload it one by one to the same bucket but under this naming
                # convention...
                # <bucket_name>/wav-staging/<username>/<project_name>/<commit_hash>/<file_name>.wav
                names = name.split("/")
                project = names[0]
                file = names[1]
                s3.meta.client.upload_file(
                    os.path.join(extract_target_dir, name),
                    bucket_name,
                    os.path.join("wav-staging", username, project, commit, file)
                )
