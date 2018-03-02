from urllib.request import Request, urlopen, quote # Python 3
from bs4 import BeautifulSoup
from difflib import SequenceMatcher as sm # For comparing similarity of lyrics
import requests
import json
import os

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Import client access token from environment variable
import lyricsgenius.lyricsgenius as genius
client_access_token = os.environ.get("GENIUS_CLIENT_ACCESS_TOKEN", None)
assert client_access_token is not None, "Must declare environment variable: GENIUS_CLIENT_ACCESS_TOKEN"
api = genius.Genius(client_access_token)

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

def getListFromRanker_Selenium(url):
    # https://stackoverflow.com/questions/21006940/how-to-load-all-entries-in-an-infinite-scroll-at-once-to-parse-the-html-in-pytho    
    browser = webdriver.Chrome()

    browser.get("https://www.ranker.com/crowdranked-list/the-greatest-rappers-of-all-time")
    time.sleep(1)

    elem = browser.find_element_by_tag_name("body")

    no_of_pagedowns = 20

    while no_of_pagedowns:
        elem.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.2)
        no_of_pagedowns-=1

    post_elems = browser.find_elements_by_class_name("listItem__data")
    artist_names = [p.find_element_by_class_name("listItem__title").text for p in post_elems[:-1]]
    browser.quit()
    return artist_names

def downloadLyrics(artist_names, max_songs=None):
    artist_objects = [api.search_artist(name, max_songs=max_songs, take_first_result=True) for name in artist_names]
    api.save_artists(artist_objects, overwrite=True)

def main():

    url = "https://www.ranker.com/crowdranked-list/the-greatest-rappers-of-all-time"
    # artist_names = getListFromRanker(url)
    artist_names = getListFromRanker_Selenium(url)
    print(artist_names)
    downloadLyrics(artist_names[:2], max_songs=1)

if __name__ == '__main__':
    main()
    

