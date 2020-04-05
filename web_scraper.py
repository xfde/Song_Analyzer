import requests
from bs4 import BeautifulSoup
import pandas as pd
import sys


def GetSongsFromArtist(artist, songName, position):
    print(artist)
    base = 'https://www.lyrics.com/'
    url = base + 'artist/' + artist.split(' ')[0].lower()
    for i in range(1, len(artist.split())):
        url = url + '%2D' + artist.split(' ')[i].lower()
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    print(url)
    duration = []
    lyrc = []
    song = []
    songs = soup.find_all('td', {'class': 'tal qx'})
    songs_duration = soup.find_all('td', {'class': 'tar qx'})
    seen = set()
    cnt = 0
    for i in songs:
        if (i.text.lower() not in seen) and (i.text.lower() == songName.lower()):
            print("Song No." + str(position), end=" ")
            seen.add(i.text.lower())
            song.append(i.text)
            duration.append(songs_duration[cnt].text)
            if songs[cnt].a is None:
                pass
            else:
                print("Lyrics Found")
                lyrics_url = base + songs[cnt].a.attrs['href']
                req = requests.get(lyrics_url)
                soup = BeautifulSoup(req.text, 'html.parser')
                lyrc.append(soup.find('pre', {'id': 'lyric-body-text'}).text.encode('UTF-8'))
        cnt = cnt + 1
    dataf = pd.DataFrame({'song': song, 'duration': duration, 'lyrics': lyrc})
    # Set output file
    # !!! DO NOT RUN IF CSV IS OPEN
    dataf.to_csv('songs_data.csv', mode='a', header=False)


def GetTop100Songs():
    url = 'https://www.billboard.com/charts/decade-end/hot-100'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    song_names = soup.find_all('div', {'class': 'ye-chart-item__title'})
    song_artists = soup.find_all('div', {'class': 'ye-chart-item__artist'})
    cnt = 0
    for i, j in zip(song_names, song_artists):
        string = ''
        for conto in range(0, len(j.text.split())):
            if j.text.split(' ')[conto] == 'Featuring' or j.text.split(' ')[conto] == '&':
                break
            else:
                string = string + ' ' + j.text.split(' ')[conto].lower()
        GetSongsFromArtist(string, i.text.lower(), cnt)
        cnt += 1


GetTop100Songs()
