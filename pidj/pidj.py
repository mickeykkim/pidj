"""Main module."""
import random
import string
from typing import Dict, Tuple

import flask
import spotify.sync as spotify  # type: ignore

from pidj.configs import CLIENT_ID, CLIENT_SECRET, SESSIONS_SECRET

SPOTIFY_CLIENT = spotify.Client(CLIENT_ID, CLIENT_SECRET)

APP = flask.Flask(__name__)
APP.secret_key = SESSIONS_SECRET
APP.config.from_mapping({'spotify_client': SPOTIFY_CLIENT})

FLASK_HOST = 'localhost'
FLASK_PORT = '8888'
FLASK_DEBUG = True

# See: https://community.spotify.com/t5/Spotify-for-Developers/
#        INVALID-CLIENT-Invalid-redirect-URI/m-p/5229058#M2802
REDIRECT_URI: str = f'http://{FLASK_HOST}:{FLASK_PORT}/spotify/callback'

OAUTH2_SCOPES: Tuple[str, str, str] = ('user-modify-playback-state',
                                       'user-read-currently-playing',
                                       'user-read-playback-state')
OAUTH2: spotify.OAuth2 = spotify.OAuth2(SPOTIFY_CLIENT.id,
                                        REDIRECT_URI,
                                        scopes=OAUTH2_SCOPES)

SPOTIFY_USERS: Dict[str, spotify.User] = {}


@APP.route('/spotify/callback')
def spotify_callback():
    """Spotify callback after login"""
    try:
        code = flask.request.args['code']
    except KeyError:
        return flask.redirect('/spotify/failed')
    else:
        key = ''.join(random.choice(string.ascii_uppercase) for _ in range(16))
        SPOTIFY_USERS[key] = spotify.User.from_code(SPOTIFY_CLIENT,
                                                    code,
                                                    redirect_uri=REDIRECT_URI)

        flask.session['spotify_user_id'] = key

    return flask.redirect('/')


@APP.route('/spotify/failed')
def spotify_failed():
    """Login failed page"""
    flask.session.pop('spotify_user_id', None)
    return 'Failed to authenticate with Spotify.'


@APP.route('/')
@APP.route('/index')
def index():
    """Index page"""
    try:
        return repr(SPOTIFY_USERS[flask.session['spotify_user_id']])
    except KeyError:
        return flask.redirect(OAUTH2.url)


def main():
    """Main method"""
    APP.run(host=FLASK_HOST, port=FLASK_PORT, debug=FLASK_DEBUG)


if __name__ == '__main__':
    main()
