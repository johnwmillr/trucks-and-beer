from urllib.request import Request, urlopen, quote # Python 3
# from urllib2 import Request, urlopen, quote # Python 2    
from bs4 import BeautifulSoup
from difflib import SequenceMatcher as sm # For comparing similarity of lyrics
import requests
import json
import time
import genius as genius_api
genius = genius_api.Genius()


artist_lyrics = {'artists': []}

def downloadLyrics(artist_names, max_songs=None, artists_gender=None, filename="artist_lyrics"):
    # Use the Genius API to get each artist's lyrics
    found_artists = {}
    
    start = time.time()
    for n, name in enumerate(artist_names):
        print("\n--------")
        # try:        
        if name not in found_artists:
            artist = genius.search_artist(name, max_songs=max_songs)
            artist_lyrics['artists'].append({})
            artist_lyrics['artists'][-1]['artist'] = artist.name                            
            artist_lyrics['artists'][-1]['songs'] = []            
            artist_lyrics['artists'][-1]['gender'] = artists_gender # If you know all genders in list are same
            for song in artist.songs:
                if not songInArtist(song): # This takes way too long! It's basically O(n^2), can I do better?
                    artist_lyrics['artists'][-1]['songs'].append({})
                    artist_lyrics['artists'][-1]['songs'][-1]['title'] = song.title
                    artist_lyrics['artists'][-1]['songs'][-1]['album'] = song.album
                    artist_lyrics['artists'][-1]['songs'][-1]['year'] = song.year
                    artist_lyrics['artists'][-1]['songs'][-1]['lyrics'] = song.lyrics                
                    artist_lyrics['artists'][-1]['songs'][-1]['image'] = song.song_art_image_url
                    artist_lyrics['artists'][-1]['songs'][-1]['artist'] = name
                    artist_lyrics['artists'][-1]['songs'][-1]['json'] = song._body
                else:
                    print("SKIPPING \"{}\", already found in artist collection.".format(song.title))
            found_artists[name] = (name, len(artist_lyrics['artists'])-1)
        else:
            # Store reference to artist location in dict, if artist previously found
            artist_lyrics['artists'][-1] = found_artists[name]
        # except Exception as e:
            # print(e)
            # print('Skipping "{}" due to error.'.format(name))

        # Every other artist write the JSON object to disk as a backup
        if n % 2 == 0:
            with open(filename + '_temp' '.json', 'w') as outfile:
                json.dump(artist_lyrics, outfile)
            
    # Final write of the JSON object
    with open(filename + '.json', 'w') as outfile:
        json.dump(artist_lyrics, outfile)
        
    end = time.time()
    print("Time elapsed: {} hours".format((end-start)/60.0/60.0))

def getArtistsFromList(URL):    
    # URL is a Billboard top list,
    # e.g. https://www.billboard.com/charts/year-end/2006/top-country-artists
    page = requests.get(URL)
    html = BeautifulSoup(page.text, "html.parser")    
    chart_items = html.find_all("div", class_="ye-chart-item__title")
    return [item.get_text().strip() for item in chart_items]            

# Here's a list from Ranker.com of the top 50 female country singers
def getListFromRanker(URL):
    page = requests.get(URL)
    html = BeautifulSoup(page.text, "html.parser")
    h = html.find_all("div", class_="listItem__data")
    names = []
    for href in h:
        try:
            name = href.find('a').contents[0]
            if len(name.split()) == 2:
                names.append(name)
        except:
            pass
    return names

# We want to reject songs that have already been added to artist collection
def songsAreSame(s1, s2):    
    # Idea credit: https://bigishdata.com/2016/10/25/talkin-bout-trucks-beer-and-love-in-country-songs-analyzing-genius-lyrics/
    # Compare lyric content using SequenceMatcher
    seqA = sm(None, s1.lyrics, s2['lyrics'])
    seqB = sm(None, s2['lyrics'], s1.lyrics)
    return seqA.ratio() > 0.5 or seqB.ratio() > 0.5

def songInArtist(new_song):    
    # artist_lyrics is global (works in Jupyter notebook)
    for song in artist_lyrics['artists'][-1]['songs']:
        if songsAreSame(new_song, song):
            return True
    return False


def main():

    # Get the Billboard Top 50 country artists each year since 2006
    if 0:
        top_artists_by_year = {}
        for year in range(2006,2018):    
            url = "https://www.billboard.com/charts/year-end/{}/top-country-artists".format(year)
            top_artists_by_year[year] = getArtistsFromList(url)

    artist_names = ['Johnny Cash','Hank Williams']

    downloadLyrics(artist_names, max_songs=3)


if __name__ == '__main__':
    main()
    



