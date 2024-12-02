# Justin Caringal
# 
# A stand-alone function to help clean up song
# information queried from MongoDB in app.py
# and send it over to access_spotify.py

def _extract_one_song(song : dict):
    """Clean up one song.
    
    A function which takes one song information
    dictionary and extracts only the title and artist
    from the song, returning it.
    
    Args:
        song (dict): The information of a single song.
    
    Returns:
        dict: Returns a cleaned and streamlined dictionary
    """
    cleaned_dict = {}

    # handles title insertion
    if 'song' in song:
        cleaned_dict['song'] = song['song']
    else:
        cleaned_dict['song'] = ''

    # handles author insertion
    if 'artist' in song:
        cleaned_dict['artist'] = song['artist']
    else:
        cleaned_dict['artist'] = ''

    return cleaned_dict


def extract_songs(songs : list):
    """Extracts the needed song information.

    A function which takes a list of songs and extracts
    the title and artist information for each song. Exported
    to an external python script.

    Args:
        songs (list): A list of song information dictionaries
            to be iterated through.

    Returns:
        list: Returned a cleaned and streamlined list of song
            information dictionaries
    """
    return [_extract_one_song(song) for song in songs]

__all__ = ['extract_songs']
