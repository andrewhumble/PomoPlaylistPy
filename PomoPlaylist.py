import spotipy
import random
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyPKCE


def pomorize(uris, time_per_session):
    random.shuffle(uris)
    songs_output = []
    songs_remaining = uris[:]
    time_sum = 0
    time_minimum = time_per_session - (time_per_session * 0.04)
    time_maximum = time_per_session + (time_per_session * 0.04)
    for j in range(0, len(uris), 1):
        time_per_session = uris[j][1]
        name = uris[j][0]
        if (time_sum + time_per_session) <= time_maximum:
            songs_output.append(name)
            index = find(name, songs_remaining)
            songs_remaining.pop(index)
            time_sum += time_per_session
            if time_sum >= time_minimum:
                return songs_output, songs_remaining, time_sum
    return songs_output, songs_remaining, time_sum


def find(element, array):
    for k in range(0, len(array), 1):
        if array[k][0] == element:
            return k


def store_tracks(track_list):
    stored_tracks = []
    for m, item in enumerate(track_list['items']):
        track = item['track']
        track_info = []
        track_uri = track['uri']
        track_info.append(track_uri)
        track_length_long = sp.track(track['uri'])
        track_length = track_length_long['duration_ms']
        track_info.append(track_length)
        stored_tracks.append(track_info)
    return stored_tracks


cid = 'dd2836540fa3469592394918a4789025'
secret = '5ba66d87f2aa4f8386701c1eaec9bfb0'
r_uri = 'https://humbletutors.com/pomodoro-playlist/'
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=cid, client_secret=secret))
scope = "playlist-modify-public"
# user = "sbg1eumhnz8r137t43an7py9o"
user = "sbg1eumhnz8r137t43an7py9o"
sp_OAuth = spotipy.Spotify(auth_manager=SpotifyPKCE(client_id=cid, redirect_uri=r_uri, username=user, scope=scope))

# Gets playlists from the user
playlists = sp.user_playlists(user)
print("Your playlists: ")

# Stores the playlists into a list of uris and prints the playlist names
playlist_ids = []
while playlists:
    for i, playlist in enumerate(playlists['items']):
        uri = playlist['uri']
        playlist_ids.append(uri)
        print("%4d %s" % (i + 1, playlist['name']))
    if playlists['next']:
        playlists = sp.next(playlists)
    else:
        playlists = None

# Gets playlist choice from the user
playlist_num = int(input("\nWhich playlist number would you like to use? ")) - 1

# Forms list consisting of song name, song uri, and song length in milliseconds
results = sp.playlist(playlist_ids[playlist_num])
tracks = results['tracks']
songs = store_tracks(tracks)

# user_id = "sbg1eumhnz8r137t43an7py9o"
user_id = "sbg1eumhnz8r137t43an7py9o"
playlist_name = input("\nWhat should the playlist be called? ")
created_playlist = sp_OAuth.user_playlist_create(user_id, playlist_name)

time = 1500000
total_time = 0
uri_list, uri_remaining, time_length = pomorize(songs, 1500000)
total_time += time_length
time_min = time - (time * 0.04)
time_max = time + (time * 0.04)
one_minute_silence = "spotify:track:5ztFa7D99J95hLjLt2NMXg"
break_silence = []
for i in range(0, 5, 1):
    break_silence.append(one_minute_silence)
new_playlist_id = created_playlist['id']
sp_OAuth.playlist_add_items(new_playlist_id, uri_list, position=0)
sp_OAuth.playlist_add_items(new_playlist_id, break_silence, position=len(uri_list))

long_break_counter = 0
while len(uri_remaining) > 0:
    songs = uri_remaining[:]
    uri_list, uri_remaining, time_length = pomorize(songs, 1500000)
    total_time += time_length
    sp_OAuth.playlist_add_items(new_playlist_id, uri_list, position=len(uri_list) - 1)
    if long_break_counter == 3:
        sp_OAuth.playlist_add_items(new_playlist_id, break_silence, position=len(uri_list))
        sp_OAuth.playlist_add_items(new_playlist_id, break_silence, position=len(uri_list)+len(break_silence))
        long_break_counter = 0
    else:
        sp_OAuth.playlist_add_items(new_playlist_id, break_silence, position=len(uri_list))
    long_break_counter += 1
