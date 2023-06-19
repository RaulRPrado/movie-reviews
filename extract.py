import logging
import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.DEBUG)

movies = [
    'Everything Everywhere All at Once 2022',
    'Top Gun: Maverick 2022',
    'The Batman 2022'
]

def GoogleRogerEbertSearchUrl(text):
    words = (text + ' roger ebert movie review').split(' ')
    search_words = "+".join(words)
    return 'https://google.com/search?q=' + search_words

def RogerEbertReviewUrl(movie):
    searchUrl = GoogleRogerEbertSearchUrl(movie)
    logging.debug('Google Search - ' + searchUrl)

    content = requests.get(searchUrl).text
    url_start_index = content.find('https://www.rogerebert.com/reviews/')
    start_content = content[url_start_index:]

    url_end_index = start_content.find('&')
    url = start_content[:url_end_index]

    logging.debug('Roger Ebert Url - ' + searchUrl)

    return url

def ExtractRogerEbertReview(url):
    page = requests.get(url).content
    soup = BeautifulSoup(page, "html.parser")
    blocks = soup.find_all('section', {'class': 'page-content--block_editor-content js--reframe'})

    review = ''
    for block in blocks:
        review += ' ' + block.get_text()

    return review


if __name__=="__main__":

    for movie in movies:
        url = RogerEbertReviewUrl(movie)
        print(url)

        review = ExtractRogerEbertReview(url)
        print(review)
