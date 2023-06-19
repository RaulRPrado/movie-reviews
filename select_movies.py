import logging
import pandas as pd

if __name__=="__main__":

    print("Reading file")
    akas = pd.read_csv('../data/akas.tsv', sep='\t')

    # printing data
    print(akas)
