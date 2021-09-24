from flask import Flask, request, url_for
from flask import render_template

import os

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="65e7e4db3b3442499c2d758ef486f581", client_secret="89c5ef1dbd8640b9ab9a87c59c0c1deb"))

app = Flask(__name__)


@app.route("/", methods=['get'])
def spotify_get():
    return render_template('index.html')

@app.route("/", methods=['post'])
def spotify_post():
    search = request.form.get('name')
    nums = request.form.get('number')
    # type = request.form.get('type')

    musics = {}

    if (search != '' and nums != ''):
        if (int(nums) >= 51):
            return render_template('index.html', attention='※表示件数の最大は50件までです。', name=search)
        elif (int(nums) != 0 and nums != ''):
            results = sp.search(q=search, limit=nums)
            for idx, track in enumerate(results['tracks']['items']):
                musics[track['name']] = idx
            return render_template('index.html', musics=musics, result='検索結果')
    elif (search != '' and nums == ''):
        return render_template('index.html', attention='※表示件数の入力をしてください。', name=search)
    elif (search == '' and nums != ''):
        return render_template('index.html', attention='※アーティスト名を入力してください。', num=nums)
    elif (search == '' and nums >= 51):
        return render_template('index.html', attention='※表示件数の最大は50件までです。', name=search)
    else:
        return render_template('index.html', attention='※アーティスト名と表示件数の入力してください。', name=search, num=nums)

if __name__ == "__main__":
    app.run(debug=True)