import logging
import requests
from bs4 import BeautifulSoup

from utils import getMovieYear

# Generic

def ReviewUrl(source, movie):
    if source == 'RogerEbert':
        return RogerEbertReviewUrl(movie)
    elif source == 'HollywoodReporter':
        return HollywoodReporterReviewUrl(movie)
    elif source == 'EW':
        return EWReviewUrl(movie)
    elif source == 'EmpireOnline':
        return EmpireOnlineReviewUrl(movie)
    elif source == 'RollingStone':
        return RollingStoneReviewUrl(movie)
    else:
        return ''

def ExtractReview(source, url):
    if source == 'RogerEbert':
        return ExtractRogerEbertReview(url)
    elif source == 'HollywoodReporter':
        return ExtractHollywoodReporterReview(url)
    elif source == 'EW':
        return ExtractEWReview(url)
    elif source == 'EmpireOnline':
        return ExtractEmpireOnlineReview(url)
    elif source == 'RollingStone':
        return ExtractRollingStoneReview(url)
    else:
        return ''

def GoogleSearchUrl(source, text):
    if source == 'RogerEbert':
        words = (text + ' roger ebert movie review').split(' ')
    elif source == 'HollywoodReporter':
        words = (text + ' hollywood reporter movie review').split(' ')
    elif source == 'EW':
        words = (text + ' entertainment weekly movie review').split(' ')
    elif source == 'EmpireOnline':
        words = (text + ' empire online movie review').split(' ')
    elif source == 'RollingStone':
        words = (text + ' rolling stone movie review').split(' ')
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

# EntertainmentWeekly
def EWReviewUrl(movie):
    searchUrl = GoogleSearchUrl('EW', movie)
    logging.info('Google Search - ' + searchUrl)

    content = requests.get(searchUrl).text
    if 'https://ew.com/movies/movie-reviews/' in content:
        url_start_index = content.find('https://ew.com/movies/movie-reviews/')
        start_content = content[url_start_index:]

        url_end_index = start_content.find('&')
        url = start_content[:url_end_index]
        logging.info('Entertainment Weekly Url - ' + url)
        return url
    elif 'https://ew.com/article/' in content:
        url_start_index = content.find('https://ew.com/article/')
        start_content = content[url_start_index:]

        url_end_index = start_content.find('-review/')
        url = start_content[:url_end_index+8]

        if len(url) > 200:
            return ''

        if url == 'https://ew.com/movies/movie-reviews/':
            return ''

        year = getMovieYear(movie)
        if year not in url and str(int(year) + 1) not in url:
            logging.info('Entertainment Weekly Url ERROR - WRONG YEAR - ' + url)
            return ''

        logging.info('Entertainment Weekly Url - ' + url)

    return ''

def ExtractEWReview(url):
    page = requests.get(url).content
    soup = BeautifulSoup(page, "html.parser")
    blocks = soup.find_all('div', {'class': 'paragraph'})

    review = ''
    for block in blocks:
        this_review = ' '.join(block.get_text().split())
        if 'Related content' in this_review:
            break
        review += ' ' + this_review

    return review

# EmpireOnline
def EmpireOnlineReviewUrl(movie):
    searchUrl = GoogleSearchUrl('EmpireOnline', movie)
    logging.info('Google Search - ' + searchUrl)

    content = requests.get(searchUrl).text

    if 'https://www.empireonline.com/movies/reviews/' in content:
        url_start_index = content.find('https://www.empireonline.com/movies/reviews/')
        start_content = content[url_start_index:]

        url_end_index = start_content.find('&')
        url = start_content[:url_end_index]
        logging.info('Empire Online Url - ' + url)

        if len(url) > 200:
            return ''

        return url

    return ''

def ExtractEmpireOnlineReview(url):
    page = requests.get(url).content
    soup = BeautifulSoup(page, "html.parser")
    blocks = soup.find_all('p')

    review = ''
    for block in blocks:
        this_review = ' '.join(block.get_text().split())
        if 'Movies |' in this_review:
           break
        review += ' ' + this_review

    return review

# RollingStone
def RollingStoneReviewUrl(movie):
    searchUrl = GoogleSearchUrl('RollingStone', movie)
    logging.info('Google Search - ' + searchUrl)

    content = requests.get(searchUrl).text

    if 'https://www.rollingstone.com/tv-movies/tv-movie-reviews/' in content:
        url_start_index = content.find('https://www.rollingstone.com/tv-movies/tv-movie-reviews/')
        start_content = content[url_start_index:]

        url_end_index = start_content.find('&')
        url = start_content[:url_end_index]
        logging.info('RollingStone Url - ' + url)

        if len(url) > 200:
            return ''

        return url

    return ''

def ExtractRollingStoneReview(url):
    page = requests.get(url).content
    soup = BeautifulSoup(page, "html.parser")
    blocks = soup.find_all('p')

    review = ''
    for block in blocks:
        this_review = ' '.join(block.get_text().split())
        if 'We want to hear it' in this_review:
            break
        review += ' ' + this_review

    return review
