# Justin Caringal
# 
# Scripts and functions to organize interfacing with the
# Spotify API

### CONSTANTS ###

CONFIG_NAME = 'config.json'
FLASK_KEY = None
CLIENT_ID = None
CLIENT_SECRET = None

### LIBRARIES / PACKAGES ###

import os
import sys
import json
from time import time
from datetime import datetime, timezone
import spotipy
from spotipy.oauth2 import SpotifyOAuth # authenticates permissions
from dotenv import load_dotenv, find_dotenv
from flask import Flask, request, url_for, session, redirect # accesses HTTP requests

### .ENV SECRETS BOILERPLATE ###
load_dotenv(find_dotenv())
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
FLASK_KEY = os.getenv('FLASK_KEY')

### FLASK SETUP BOILERPLATE ###
app = Flask(__name__) # initializes Flask app
app.config['SESSION_COOKIE_NAME'] = 'Spotify Cookie' # set name of session cookie
app.secret_key = FLASK_KEY # sets random key to sign cookie
TOKEN_INFO = 'token_info' # sets key for token info in session dict


### FUNCTIONS ###

def create_spotify_oauth():
    """Authenticates Spotify API

    Args:
        None
    
    Returns:
        SpotifyOAuth: A successful OAuth.
        
    """
    
    return SpotifyOAuth(
        client_id = CLIENT_ID,
        client_secret = CLIENT_SECRET,
        redirect_uri = url_for('redirect_page', _external=True),
        scope='user-library-read playlist-modify-public playlist-modify-private'
    )


def get_token():
    """Getter for token info.
    
    A function which gets the token info from the session.

    Args:
        None
    
    Returns:
        The token info to connect Flask and the Spotify API
    
    """
    
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        # if the token info is not found, redirect the user to the login route
        redirect(url_for('login', _external=False))
    
    # check if the token is expired and refresh it if necessary
    now = int(time())

    is_expired = token_info['expires_at'] - now < 60
    if is_expired:
        spotify_oauth = create_spotify_oauth()
        token_info = spotify_oauth.refresh_access_token(token_info['refresh_token'])

    return token_info


### FLASK ROUTES ###

@app.route('/')
def login():
    # create a SpotifyOAuth instance and get the authorization URL
    auth_url = create_spotify_oauth().get_authorize_url()
    # redirect the user to the authorization URL
    return redirect(auth_url)


# route to handle the redirect URI after authorization
@app.route('/redirect')
def redirect_page():
    # clear the session
    session.clear()
    # get the authorization code from the request parameters
    code = request.args.get('code')
    # exchange the authorization code for an access token and refresh token
    token_info = create_spotify_oauth().get_access_token(code)
    # save the token info in the session
    session[TOKEN_INFO] = token_info
    # redirect the user to the create_playlist route
    return redirect(url_for('create_playlist',_external=True))


# route to convert a Youtube playlist into a Spotify playlist
@app.route('/TruifyDiscographyDatabase')
def create_playlist():

    ### AUTH BOILERPLATE
    try: 
        # get the token info from the session
        token_info = get_token()
    except:
        # if the token info is not found, redirect the user to the login route
        print('User not logged in')
        return redirect("/")

    # create a Spotipy instance with the access token
    sp = spotipy.Spotify(auth=token_info['access_token'])
    SPOTIFY_USER_ID = sp.current_user()['id']

    iso_suffix = datetime.now().astimezone().strftime('%Y%m%d-%H%M%S')
    playlist_title = f'Truify\'s Playlist {iso_suffix}'
    

    # checks to see if playlist already exists in current users playlists,
    # exits program to prevent override and unwanted appends
    current_playlists =  sp.current_user_playlists()['items']
    for playlist in current_playlists:
        if(playlist['name'] == playlist_title):
            print(f'Playlist \"{playlist_title}\" already exists.')
            return f'Playlist \"{playlist_title}\" already exists.'
        
    print('Initiating Spotify API track queries.')

    songs_info = [
        {
            'title' : 'No Longer You',
            'author' : 'Jorge Rivera-Herrans',
        }
    ]
    # QUERYING
    # iterates through video info to creacte search queries to Spotify API
    # URI - resource identifiers for objects in Spotify
    MAX_REPEAT_QUERIES = 3
    track_uris = []
    successful_queries = [] # not currently interacted with
    queries_not_found = []
    for song in songs_info:
        # creates query and executes API call
        search_query = f"{song['title']} {song['author']}"
        print(f'Querying: {search_query}', end=' - Status - ')
        for attempt in range(1, MAX_REPEAT_QUERIES + 1):
            search_result = sp.search(search_query,
                                    limit=1,
                                    offset=0,
                                    type='track')
            
            print(f'Attempt {attempt}: ', end='')

            # examines search result, Exception created when bad result received
            # i.e. a query failed to return a even a single track
            try: # query successful
                track_uri = search_result['tracks']['items'][0]['uri']
                track_uris.append(track_uri)
                successful_queries.append(search_query)
                print('Success.', end='')
                break
            except: # query not successful (list index out of range)
                queries_not_found.append(search_query)
                print('Failed.', end='')
        print('') # prints newline

    not_found = len(songs_info) - len(track_uris)
    print(f'Track queries complete. {len(track_uris)} successes, {not_found} failures.')
    
    # removes duplicates while preserving order using list comprehension
    print('Removing duplicates.')
    trimmed_uris = []
    [trimmed_uris.append(uri) for uri in track_uris if uri not in trimmed_uris]
    tracks_removed = len(track_uris) - len(trimmed_uris)
    print(f'{tracks_removed} tracks removed. New length: {len(trimmed_uris)}')

    # creates playlist and extracts ID
    print(f'Creating playlist {playlist_title}')
    sp.user_playlist_create(user=SPOTIFY_USER_ID,
                            name=playlist_title,
                            public=True,
                            collaborative=False,
                            description='This playlist was created by Jaq\'s YtS bot.')
    # finds new playlist created and extracts playlist ID
    current_playlists =  sp.current_user_playlists()['items']
    new_playlist_id = None
    for playlist in current_playlists:
        if(playlist['name'] == playlist_title):
            new_playlist_id = playlist['id']
            print(f'Successfully created and identified playlist.')
            break
    
    # breaks up playlist appends to API to prevent overwhelming API
    size_of_sublist = 25
    for index in range(size_of_sublist,
                       len(trimmed_uris) + size_of_sublist,
                       size_of_sublist):
        start = index - size_of_sublist
        sublist_of_uris = trimmed_uris[start : index]
        sp.user_playlist_add_tracks(SPOTIFY_USER_ID,
                                    new_playlist_id,
                                    sublist_of_uris,
                                    None)
    
    end_str = f'Playlist {playlist_title} successfully created and populated!'
    print(end_str)
    return end_str


@app.route('/shutdown', methods=['POST'])
def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return 'Server shutting down...'


from multiprocessing import Process
import webbrowser as wb
if __name__ == '__main__':
    wb.open('http://127.0.0.1:5000/')
    server = Process(target=app.run)
    server.start()
    server.join()
       

    # server.terminate()
    print('test')