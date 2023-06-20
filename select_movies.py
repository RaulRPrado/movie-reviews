import logging
import pandas as pd
import requests
from bs4 import BeautifulSoup


def getTitles(url, headers):
    soup = BeautifulSoup(requests.get(url, headers=headers).content, "html.parser")
    titles = soup.find_all('a', href=True)

    logging.info("Found {} movie titles".format(len(titles)))

    output = list()
    for tt in titles:

        if '/title/tt' in tt['href']:
            title = tt.get_text().strip()
            if len(title) > 0:
                output.append(title)
    return output

def getYears(url, headers):
    soup = BeautifulSoup(requests.get(url, headers=headers).content, "html.parser")
    titles = soup.find_all('span', {"class": "lister-item-year text-muted unbold"})

    logging.info("Found {} movie years".format(len(titles)))

    output = list()
    for tt in titles:

        year = ''.join(c for c in tt.get_text() if c.isdigit())
        output.append(year)

    return output

def getMovies(url, headers):
    titles = getTitles(url, headers)
    years = getYears(url, headers)
    return [t + " " + y for (t, y) in zip(titles, years)]




if __name__=="__main__":

    headers = {"Accept-Language": "en-US,en;q=0.5"}


    urls = [
        "https://www.imdb.com/search/title/?title_type=feature&release_date=2012-01-01,2022-12-31&num_votes=50000,&countries=us&view=simple&count=250",
        "https://www.imdb.com/search/title/?title_type=feature&release_date=2012-01-01,2022-12-31&num_votes=50000,&countries=us&view=simple&count=250&start=251&ref_=adv_nxt",
        "https://www.imdb.com/search/title/?title_type=feature&release_date=2012-01-01,2022-12-31&num_votes=50000,&countries=us&view=simple&count=250&start=501&ref_=adv_nxt",
        "https://www.imdb.com/search/title/?title_type=feature&release_date=2012-01-01,2022-12-31&num_votes=50000,&countries=us&view=simple&count=250&start=751&ref_=adv_nxt",
        "https://www.imdb.com/search/title/?title_type=feature&release_date=2012-01-01,2022-12-31&num_votes=50000,&countries=us&view=simple&count=250&start=1001&ref_=adv_nxt",
    ]

    movies = list()

    for url in urls:
        movies += getMovies(url, headers)

    with open('movies.dat', 'w') as out:
        for mm in movies:
            out.write(mm + '\n')
