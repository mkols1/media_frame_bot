# X_frame_bot
 bot for uploading frames of a series in a row. requires some manual work

# Extracting frames
Used ffmpeg to extract 12 frames of each second and then manually pruned them to pick out the key moments

##Example
without subs:

```
ffmpeg -i "Revue Starlight - S01E01 - Stage Girls.mkv" -qscale:v 3 -r 12/1 "01 - Stage Girls - %05d.jpg"
```

with subs:

```
ffmpeg -i "Revue Starlight - S01E01 - Stage Girls.mkv" -qscale:v 3 -vf subtitles="Revue Starlight - S01E01 - Stage Girls.mkv" -r 12/1 "01 - Stage Girls - %05d.jpg"
```

##oauth2.txt
Replace each line with your corresponding access token

# Issues
Could usually get it to upload between 12-24 hours before the twitter/X/whatever API would stop accepting the posts. My understanding was that it shouldn't have been anywhere close to exceeding the limits but I'm aware that there were some changes to the API recently that led to issues with other similar projects.
