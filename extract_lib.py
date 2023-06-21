import logging
import requests
from bs4 import BeautifulSoup

# Generic

def ReviewUrl(source, movie):
    if source == 'RogerEbert':
        return RogerEbertReviewUrl(movie)
    elif source == 'HollywoodReporter':
        return HollywoodReporterReviewUrl(movie)
    else:
        return ''

def ExtractReview(source, url):
    if source == 'RogerEbert':
        return ExtractRogerEbertReview(url)
    elif source == 'HollywoodReporter':
        return ExtractHollywoodReporterReview(url)
    else:
        return ''

def GoogleSearchUrl(source, text):
    if source == 'RogerEbert':
        words = (text + ' roger ebert movie review').split(' ')
    elif source == 'HollywoodReporter':
        words = (text + ' hollywood reporter movie review').split(' ')
    else:
        return ''
    search_words = "+".join(words)
    return 'https://google.com/search?q=' + search_words


# HollywoodReporter
def HollywoodReporterReviewUrl(movie):
    searchUrl = GoogleSearchUrl('HollywoodReporter', movie)
    logging.info('Google Search - ' + searchUrl)

    content = requests.get(searchUrl).text
    url_start_index = content.find('https://www.hollywoodreporter.com/movies/movie-reviews')
    start_content = content[url_start_index:]

    url_end_index = start_content.find('&')
    url = start_content[:url_end_index]

    logging.info('Hollywood Reporter Url - ' + url)

    return url

def ExtractHollywoodReporterReview(url):
    page = requests.get(url).content
    soup = BeautifulSoup(page, "html.parser")
    # blocks = soup.find_all('p', {'class': 'paragraph larva //  a-font-body-m'})
    blocks = soup.find_all('p')

    review = ''
    for block in blocks:

        if block.has_attr('class'):
            if 'paragraph' not in block['class'] and 'larva' not in block['class']:
                continue

        this_review = ' '.join(block.get_text().split())
        review += ' ' + this_review

    return review

# RogerEbert
def RogerEbertReviewUrl(movie):
    searchUrl = GoogleSearchUrl('RogerEbert', movie)
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
