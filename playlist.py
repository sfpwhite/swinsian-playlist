import sqlite3
import sys
import datetime
import csv

# TODO: use click or argparse
playlist = sys.argv[1]

# TODO perhaps make this into a class
db = sqlite3.connect(
    '/Users/swhite/Library/Application Support/Swinsian/Library.sqlite')
cursor = db.cursor()

# TODO make this into a function
playlist_num = cursor.execute(
    "SELECT playlist_id FROM playlist WHERE name IS ?", (playlist,)).fetchall()

# TODO make this a function
if not playlist_num:
    print("playlist doesn't exist")
    exit()
# TODO check length of playlist_num and if > 1, enter a for loop to ask user which playlist to convert

#TODO make this into a function
playlist_to_convert = cursor.execute(
    "SELECT track.artist,track.title,track.length,playlisttrack.tindex FROM "
    "track INNER JOIN playlisttrack on track.track_id = playlisttrack.track_id WHERE "
    "playlisttrack.playlist_id IS ? ORDER BY playlisttrack.tindex", 
    (playlist_num[0][0],)).fetchall()

# TODO print to cue sheet in a function
with open(f'{playlist}.cue', "w") as cue, open(f'{playlist}.csv', "w", newline='') as csvfile:
    now = datetime.datetime.now()
    show_date = playlist[0:2] + "-" + playlist[2:4] + "-" + str(now.year)[2:4]

    cue.write('PERFORMER "DJ Huge Problem"\n')
    cue.write(f'TITLE \"Lullabies For Cthulhu {show_date}\"\n')
    cue.write(f'FILE \"lullabies-for-cthulhu-{show_date}.mp3\"\n')

    fieldnames = ["start time", "end time", "duration", "title", "artist",
                  "album"]
    csvwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)

    csvwriter.writeheader()

    for track_info in playlist_to_convert:
        artist = track_info[0]
        title = track_info[1]
        album = track_info[2]
        track_length = int(track_info[3])
        tindex = track_info[4]

        # In CUE Format, the first track is at timestamp 00:00:00(MM:SS:FF
        # where F is frames and don't matter to me). Subsequent tracks have
        # a timestamp equal to the accumulated lengths of all previous tracks
        if tindex == 0:
            begin_seconds = 0
            playlist_length = track_length
        else:
            begin_seconds = playlist_length
            playlist_length += track_length

        length_formatted = str(datetime.timedelta(
            seconds=track_length)).split(':', maxsplit=1)[1]
        timestamp_begin = str(datetime.timedelta(
            seconds=begin_seconds)).split(':', maxsplit=1)[1]
        timestamp_end = str(datetime.timedelta(
            seconds=playlist_length)).split(':', maxsplit=1)[1]

        csvwriter.writerow(
            {f'start time': f'{show_date} 00:{timestamp_begin}', 'end time': f'{show_date} 00:{timestamp_end}',
             'duration': f'{length_formatted}', 'title': f'{title}', 'artist': f'{artist}', 'album': f'{album}'})

        cue.write(
            f'TRACK {str(tindex).zfill(2)} AUDIO\n'
            f'  PERFORMER "{artist}"\n')
            f'  TITLE "{title}"\n')
            f'  INDEX 01 {timestamp_formatted}:00\n')
db.close()
