from urllib.request import Request, urlopen, quote # Python 3
from bs4 import BeautifulSoup
import requests

def scrapeBillboardList(self, URL):
    page = requests.get(URL)
    html = BeautifulSoup(page.text, "html.parser")



def main():
    url = "https://www.billboard.com/charts/year-end/2017/top-country-artists"

    scraper = Scraper()
    country_artists = scraper.getBillboardList(url)


if __name__ == '__main__':
    main()
