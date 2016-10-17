# =============================================================================
# This function should be triggered when a wav file is dropped into the
# following location on S3 by unzip_project():
#
#    <bucket>/wav-staging/<username>/<project>/<commit>/<file>.wav
# =============================================================================

import os

# AWS-specific imports
import boto3


def handle(event, ctx):
    # We know this path because we saw the event printout
    object_key = event["Records"][0]["s3"]["object"]["key"]

    # Pipeline is set to dump the output in test-cdn.door43.org
    pipeline_id = "1476382143749-1ok4vi"

    # Audio file should be in...
    # <bucket_name>/wav-staging/<username>/<project>/<commit>/<file>.wav
    #               [0]         [1]        [2]       [3]
    names = object_key.split("/")
    username = names[1]
    project = names[2]
    commit = names[3]

    # ElasticTranscoder configuration. For more info, visit
    # http://docs.aws.amazon.com/elastictranscoder/latest/developerguide/create-job.html
    input_dict = {
        "Key": object_key,
        "FrameRate": "auto",
        "Resolution": "auto",
        "AspectRatio": "auto",
        "Interlaced": "auto",
        "Container": "wav"
    }
    output_key_name = os.path.splitext(os.path.basename(object_key))[0]
    job = {
        "PipelineId": pipeline_id,
        "Input": input_dict,
        "Outputs": [{
            "Key": os.path.join(
                "u",
                username,
                project,
                commit,
                output_key_name + ".mp3"
            ),
            "PresetId": "1351620000001-300040"
        }],
    }

    # Create ElasticTranscoder's job
    transcoder_client = boto3.client("elastictranscoder")
    result = transcoder_client.create_job(**job)

    return result
