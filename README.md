# song-lyrics-analysis

Inspired by a post on the [Big-ish Data Blog](https://bigishdata.com/2016/10/25/talkin-bout-trucks-beer-and-love-in-country-songs-analyzing-genius-lyrics/), I've started working on some textual analysis of contemporary country songs.

I'm writing about this project [on my blog](http://www.johnwmillr.com/trucks-and-beer/).

---
### Visualizations
![beer_and_trucks](./figures/FreqPlot_beer_and_truck.png)

Each point on the word-frequency plots represents a single artist. The values for each point were calculated as a simple percentage of times the given artist mentions a particular term. For example, Cole Swindell had 46 total songs and mentioned beer in 24 of them, arriving at a mention percentage of 52%.

I've also added the artist's gender to the plot. Further analysis is needed, but there does appear to be an interaction between gender and one's likelihood to sing about trucks and beer. I haven't found a good way to display this yet, 50% of the female artists are actually stacked on top of each other at the origin, meaning they didn't mention beer or trucks in any of their songs.


