# tr-audio-publishing

*In testing/prototype phase*

Lambda functions that kick off the publishing process for audio projects uploaded by translationRecorder app or by some other means. The end result is a web page in door43 that enables playback of the uploaded video.

## Config stuff

*region*: us-west-2
*bucket name*: test-tr-sassy

We use [APEX](http://apex.run/) for deployment. Make sure to properly set your AWS credentials for deploying.

# Important Note

This project is nowhere near finish. The automation only covers the unzipping of a project, converting wav to mp3, and uploading the converted files to door43's test-cdn bucket.

Functions that are still manual:
- Uploading project to S3 bucket (/inbound/<username>/<commit><project>.zip)
- Generation of html files for each audio files in door43's test-cdn bucket
- Integration with tx-manager to generate `build_log.json` in door43's test-cdn bucket