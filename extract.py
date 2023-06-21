import logging
from os import path

from extract_lib import ExtractReview, ReviewUrl

logging.basicConfig(level=logging.INFO)

if __name__=="__main__":

    maxMovies = 10
    source = 'HollywoodReporter'

    if source not in ['RogerEbert', 'HollywoodReporter']:
        logging.error('Source is invalid')
        exit()

    with open('movies.dat', 'r') as file:

        count = 0
        for row in file:
            movie = row.rstrip('\n').replace('/', '')
            if count >= maxMovies:
                break

            logging.info(movie)

            dirName = 'reviews/' + source + '/'
            fileName = dirName + movie + '.txt'
            fileNameError = dirName + movie + '_ERROR.txt'
            if path.exists(fileName):
                logging.info('Review already exists')
                continue

            if path.exists(fileNameError):
                logging.info('Error file already exists')
                continue

            url = ReviewUrl(source, movie)
            if len(url) < 10:
                msg = 'Url is invalid - error {}'.format(movie)
                logging.error(msg)
                with open(fileNameError, 'w') as f:
                    f.write(msg)
                continue

            review = ExtractReview(source, url)

            # print(review)
            # count += 1
            # continue

            if len(review) < 200:
                msg = 'Review is too short - error {}'.format(movie)
                logging.error(msg)
                with open(fileNameError, 'w') as f:
                    f.write(msg)
                continue

            with open(fileName, 'w') as reviewFile:
                reviewFile.write(review)
                count += 1
