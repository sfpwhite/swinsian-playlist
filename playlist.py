import sqlite3 
import argparse 
import sys 

#TODO: use click or argparse
playlist =  sys.argv[1]


#TODO abstract db object into a class
db = sqlite3.connect('/Users/swhite/Library/Application Support/Swinsian/Library.sqlite')
cursor = db.cursor()

#TODO abstract this into a function
playlist_num = cursor.execute("SELECT playlist_id FROM playlist WHERE name IS ?", (playlist,)).fetchall()

#TODO make a function
if not playlist_num:
    print("playlist doesn't exist")
    exit()

#TODO make this work, might be better to just check length of playlist_num and if > 1, enter a for loop
# to ask user which playlist to convert

#if folder:
#    folder_id = cursor.execute("SELECT playlist_id FROM playlist WHERE name IS ?", (folder,)).fetchall()
#    playlist_num = cursor.execute("SELECT playlist_id FROM playlistfolderplaylist WHERE playlistfolder_id \
#                    IS ? AND playlist_id IS ?", (folder_id, playlist_num)).fetchall()

#TODO make this into a function that is reliable for multiple values
for row in playlist_num[0]:
    playlist_num = row

#TODO make this into a function
playlist_to_convert = cursor.execute("SELECT artist,title,length FROM track LEFT OUTER JOIN playlisttrack \
                        ON track.track_id = playlisttrack.track_id WHERE playlisttrack.playlist_id IS ?",
                        (playlist_num,)).fetchall()

#TODO print to cue sheet in a function

for track_info in playlist_to_convert:
    print(track_info)

db.close()