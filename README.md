# tr-audio-publishing

*In testing/prototype phase*

Lambda functions that kick off the publishing process for audio projects uploaded by translationRecorder app or by some other means. The end result is a web page in door43 that enables playback of the uploaded video.

In order to use this process, tR should upload a zipped project as well as create a repository and push a manifest to gogs.

## tR config

Each audio project should be packaged in a folder named:

`\<target_language_slug\>_\<book_slug\>\_audio_\<version_slug\>`

and then zipped with the commit number prepended to that name.

So ULB Ephesians in Chinese Mandarin would look like this:

*folder*: cmn_eph_audio_ulb
*zip*: 6534103f53cmn_eph_audio_ulb.zip

The zipped project should be uploaded to the s3 bucket under: `\<bucket name\>/inbound/\<username\>`

## AWS config

*region*: us-west-2
*bucket name*: test-tr-sassy

We use [APEX](http://apex.run/) for deployment. Make sure to properly set your AWS credentials for deploying.

# Important Note

This project is nowhere near finish. The automation only covers the unzipping of a project, converting wav to mp3, and uploading the converted files to door43's test-cdn bucket.

Functions that are still manual:
- Uploading project to S3 bucket (/inbound/\<username\>/\<commit\>\<project\>.zip)
- Generation of html files for each audio files in door43's test-cdn bucket
- Integration with tx-manager to generate `build_log.json` in door43's test-cdn bucket
