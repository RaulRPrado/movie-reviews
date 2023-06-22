from os import path

from utils import getMovieName, getReviewFileName

if __name__=="__main__":

    sources = ['RogerEbert', 'HollywoodReporter', 'EmpireOnline', 'RollingStone']

    with open('movies.dat', 'r') as file:

        count = 0
        for row in file:
            movie = getMovieName(row)
            if count >= 4:
                break

            reviews = ''
            for src in sources:
                fileName = getReviewFileName(src, movie)
                if not path.exists(fileName):
                    continue

                with open(fileName, 'r') as file:
                    reviews += file.read() + ' '

            print(len(reviews))
            print()
            print(reviews)

            count += 1