import tekore as tk
import random 
# Grab song history, make songs and playlist(later) definitions

def get_recomendation(token) -> dict | None :
    '''
    Get Recomendations (V1): Make a Recomendation Post based on Spotify's get_recomendation endpoint.
    @param: token (str): Any users spotify oauth access token 
    @returns post (dict): Dictionary of assembled recomendation post from socialfy or (None) if recomendation is unable to be gathered

    '''
    spotify = tk.Spotify(token)
    users_songs = spotify.current_user_top_tracks(
            time_range="short_term", limit=10, offset=0).items
    chosen_songs = []
    acc = 0
    recomendation = None 
    post = {}
    if len(users_songs) >= 5:
        for song in users_songs:
            if len(chosen_songs) == 5:
                break

            if len(chosen_songs) >= len(users_songs) - acc:
                chosen_songs.append(song.id)

            elif random.uniform(0, 1) == 1:
                chosen_songs.append(song.id)

            acc += acc + 1
        recomendation = spotify.recommendations(track_ids=chosen_songs,market= 'from_token').tracks[0]
        post ={
            "id" : "null",
            "friend_name" : "Socialfy",
            "song_name" : recomendation.name,
            "song_arist" : recomendation.artists[0].name,
            "song_uri": recomendation.uri,
            "song_album_art":recomendation.album.images[0].url,
            "text_blurb" : "Your Latest Recomendation From Socialfy.",
            "likes" : "null"

            } 
        return post 
    return None