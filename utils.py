def getMovieYear(movie):
    return movie[-4:]


def getReviewFileName(source, movie):
    dirName = 'reviews/' + source + '/'
    return dirName + movie + '.txt'


def getReviewFileNameError(source, movie):
    dirName = 'reviews/' + source + '/'
    return dirName + movie + '_ERROR.txt'

def getMovieName(row):
    return row.rstrip('\n').replace('/', '')

