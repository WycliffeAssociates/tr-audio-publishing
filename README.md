# tr-audio-publishing
Lambda functions that automates publishing process for audio translation projects

In order to use this process, tR should upload a zipped project as well as create a repository and commit a manifest on gogs.

Audio should be packaged in a folder named:
\<target language slug\>_\<book slug\>\_audio__\<version slug\>

and then zipped with the commit number prepended to that name.

folder ex: cmn_eph_audio_ulb
zip ex: 6534103f53cmn_eph_audio_ulb.zip

files should be uploaded to the s3 bucket under: \<bucket name\>/inbound/\<gogs username\>

this will then unzip the project to wav-staging/\<gogs username>/\<project name\>/\<commit number\>.
Extracted wav files will be converted to mp3 and placed in the cdn bucket.
