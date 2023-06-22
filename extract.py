import logging
import argparse
from os import path

from extract_lib import ExtractReview, ReviewUrl

logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser()

parser.add_argument(
    "--src",
    default=None,
    type=str,
    choices=['RogerEbert', 'HollywoodReporter', 'EW', 'EmpireOnline', 'RollingStone']
)
parser.add_argument(
    "--max",
    default=1500,
    type=int
)


if __name__=="__main__":

    args = parser.parse_args()

    url_file = open('url_log.csv', 'a')

    with open('movies.dat', 'r') as file:

        count = 0
        for row in file:
            movie = row.rstrip('\n').replace('/', '')
            if count >= args.max:
                break

            logging.info(movie)

            dirName = 'reviews/' + args.src + '/'
            fileName = dirName + movie + '.txt'
            fileNameError = dirName + movie + '_ERROR.txt'
            if path.exists(fileName):
                logging.info('Review already exists')
                continue

            if path.exists(fileNameError):
                logging.info('Error file already exists')
                continue

            url = ReviewUrl(args.src, movie)
            if len(url) < 10:
                msg = 'Url is invalid - error {}'.format(movie)
                logging.error(msg)
                with open(fileNameError, 'w') as f:
                    f.write(msg)
                count += 1
                continue

            url_file.write(movie + ',' + url + '\n')

            review = ExtractReview(args.src, url)

            #print(review)
            #count += 1
            #continue

            if len(review) < 200:
                msg = 'Review is too short - error {}'.format(movie)
                logging.error(msg)
                with open(fileNameError, 'w') as f:
                    f.write(msg)
                count += 1
                continue

            with open(fileName, 'w') as reviewFile:
                reviewFile.write(review)
                count += 1

    url_file.close()
