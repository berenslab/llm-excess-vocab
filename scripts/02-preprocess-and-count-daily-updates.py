# Run on the server with enough RAM
# nohup python preprocess-and-count.py > foo.out 2> foo.err &

import pandas as pd
import numpy as np
import pickle
from preprocess_and_count_utils import *


# RESULTS_FOLDER = '../results/'
RESULTS_FOLDER = ""

INPUT_FOLDER = "/gpfs01/berens/data/data/pubmed_processed/"

df = load_data(start_year=2010, end_year=2025)

cleanup_abstracts_inplace(df)

X, words, years, counts, totals = vectorize_abstracts(df)

# X = pickle.load(open("counts.pkl", "rb"))

# df = pd.read_csv(RESULTS_FOLDER + "yearly-counts.csv.gz")
# words = df.word.values[:-1].astype(str)
# years = df.columns[1:].astype(int)
# counts = df.values[:-1, 1:].astype(int)
# totals = df.values[-1, 1:].astype(int)

compute_excess_gaps()

compute_excess_gaps_subgroups(0.02, "yearly-counts-subgroups.csv")


## Below is a stand-along script to analyze the Covid frequency gap

# import pandas as pd
# import numpy as np
# import pickle

# df = pd.read_csv("yearly-counts.csv.gz")
# words = df.word.values[:-1].astype(str)
# years = df.columns[1:].astype(int)
# counts = df.values[:-1, 1:].astype(int)
# totals = df.values[-1, 1:].astype(int)

# X = pickle.load(open("counts.pkl", "rb"))

# df = pd.read_csv("/gpfs01/berens/data/data/pubmed_processed/pubmed_baseline_2025.zip")
# df = df[(df.Year >= 2010) & (df.Year <= 2024)]

covid_words = ["covid", "pandemic", "coronavirus", "sars"]
ind_covid_words = np.isin(words, covid_words)
group_counts = np.zeros((2, years.size), dtype=int)
for i, year in enumerate(years):
    ind = df.Year == year
    group_counts[0, i] = np.sum(np.sum(X[ind, :][:, ind_covid_words], axis=1) > 0)
    group_counts[1, i] = np.sum(ind)
print(group_counts)
f = (group_counts[0].astype(float) + 1) / (group_counts[1] + 1)
print(f * 100)
