import logging
import requests
from os import path
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)

def GoogleRogerEbertSearchUrl(text):
    words = (text + ' roger ebert movie review').split(' ')
    search_words = "+".join(words)
    return 'https://google.com/search?q=' + search_words

def RogerEbertReviewUrl(movie):
    searchUrl = GoogleRogerEbertSearchUrl(movie)
    logging.info('Google Search - ' + searchUrl)

    content = requests.get(searchUrl).text
    url_start_index = content.find('https://www.rogerebert.com/reviews/')
    start_content = content[url_start_index:]

    url_end_index = start_content.find('&')
    url = start_content[:url_end_index]

    logging.info('Roger Ebert Url - ' + url)

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

    maxMovies = 100

    with open('movies.dat', 'r') as file:

        count = 0
        for row in file:
            movie = row.rstrip('\n')
            if count >= maxMovies:
                break

            logging.info(movie)

            # RogerEbert
            fileName = 'reviews/RogerEbert/' + movie + '.txt'
            fileNameError = 'reviews/RogerEbert/' + movie + '_ERROR.txt'
            if path.exists(fileName):
                logging.info('Review already exists')
                continue

            if path.exists(fileNameError):
                logging.info('Error file already exists')
                continue

            url = RogerEbertReviewUrl(movie)
            if len(url) < 10:
                msg = 'Url is invalid - error {}'.format(movie)
                logging.error(msg)
                with open(fileNameError, 'w') as f:
                    f.write(msg)
                continue

            review = ExtractRogerEbertReview(url)

            if len(review) < 200:
                msg = 'Review is too short - error {}'.format(movie)
                logging.error(msg)
                with open(fileNameError, 'w') as f:
                    f.write(msg)
                continue

            with open(fileName, 'w') as reviewFile:
                reviewFile.write(review)
                count += 1
