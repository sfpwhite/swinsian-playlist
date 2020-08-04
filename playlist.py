import sqlite3  
import sys 
import datetime

#TODO: use click or argparse
playlist =  sys.argv[1]


#TODO perhaps make this into a class
db = sqlite3.connect('/Users/swhite/Library/Application Support/Swinsian/Library.sqlite')
cursor = db.cursor()

#TODO make this into a function
playlist_num = cursor.execute("SELECT playlist_id FROM playlist WHERE name IS ?", (playlist,)).fetchall()

#TODO make this a function
if not playlist_num:
    print("playlist doesn't exist")
    exit()
#TODO check length of playlist_num and if > 1, enter a for loop to ask user which playlist to convert

#TODO make this into a function
playlist_to_convert = cursor.execute("SELECT track.artist,track.title,track.length,playlisttrack.tindex FROM \
                        track INNER JOIN playlisttrack on track.track_id = playlisttrack.track_id WHERE \
                        playlisttrack.playlist_id IS ? ORDER BY playlisttrack.tindex", (playlist_num[0][0],)).fetchall()

#TODO print to cue sheet in a function
with open(f'{playlist}.cue', "w") as cue:
    for track_info in playlist_to_convert:
        artist = track_info[0]
        title = track_info[1]
        track_length = int(track_info[2])
        tindex = track_info[3]

        # In CUE Format, the first track is at timestamp 00:00:00(MM:SS:FF where F is frames and don't matter to me). 
        # Subsequent tracks have a timestamp equal to the accumulated lengths of all previous tracks
        if tindex == 0:
            timestamp_seconds = 0
            playlist_length = track_length
        else:
            timestamp_seconds = playlist_length
            playlist_length += track_length
        
        timestamp_formatted = str(datetime.timedelta(seconds=timestamp_seconds)).split(':', maxsplit=1)[1]

        cue.write(f'TRACK {str(tindex).zfill(2)} AUDIO\n')
        cue.write(f'  PERFORMER "{artist}"\n')
        cue.write(f'  TITLE "{title}"\n')
        cue.write(f'  INDEX 01 {timestamp_formatted}:00\n')

db.close()