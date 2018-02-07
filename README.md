# song-lyrics-analysis

Inspired by a post on the [Big-ish Data Blog](https://bigishdata.com/2016/10/25/talkin-bout-trucks-beer-and-love-in-country-songs-analyzing-genius-lyrics/), I've started working on some textual analysis of contemporary country songs.

More specifically, I scraped [Billboard.com](https://www.billboard.com/charts/year-end/2017/top-country-artists) for a list of the top 50 country artists from 2017 and used my Genius API [python wrapper](https://github.com/johnwmillr/GeniusLyrics) to download the lyrics to each song by every artist on the list. After my script ran for about five hours, I was left with 5,089 songs across 50 artists stored in a 7 MB JSON file.

Some pertinent questions:
  - Which artist mentions trucks in their songs most often?
  - Does an artist's affinity for trucks predict any other features? Their gender for example? Or their fondness for dirt roads?
  - How does the mention of trucks vary with time? Each song item contains its publishing date.
  - Of the fifty artists, whose language is most unique? Whose is most generic?

Should be a fun project!
