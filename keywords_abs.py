from pathlib import Path
import glob
import os
import re
from langdetect import detect
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
import pandas as pd

# function ignoring blank lines
def nonblank_lines(f):
    for l in f:
        line = l.rstrip()
        if line:
            yield line


# function for text pre-processing
def pre_process(text):

    # lowercase
    text = text.lower()

    # tags out
    text = re.sub("</?.*?>", " <> ", text)

    # special characters and digits out
    text = re.sub("(\\d|\\W)+", " ", text)

    return text

# function for loading stopwords
def get_stop_words(stop_file_path):
    """load stop words """

    with open(stop_file_path, "r", encoding="utf-8") as f:
        stopwords = f.readlines()
        stop_set = set(m.strip() for m in stopwords)
        return frozenset(stop_set)

# ***COMPUTING IDF***

# list of abstract preprocessed for idf analysis
# here is my homepath to the file, change it to your own
with open("/home/kseniia/Projects/ALGE/abstracts_001_cleaned_1.txt") as myfile:
    idf = []
    for abstract in myfile:
        idf.append(pre_process(abstract))

# load a set of stop words
stopwords = get_stop_words("stopwords.txt")

# create a vocabulary of words,
# ignore words appearing in 10% of documents,
# exclude stop words
cv = CountVectorizer(max_df=0.90, stop_words=stopwords)
word_count_vector = cv.fit_transform(idf)

# magic
word_count_vector = cv.fit_transform(idf)
tfidf_transformer = TfidfTransformer(smooth_idf=True, use_idf=True)
tfidf_transformer.fit(word_count_vector)
tfidf_transformer.idf_

# ***COMPUTING TF-IDF***

# loading abstract test data
df_test = pd.read_csv("abstract.csv", sep='\t', engine='python')
test = [pre_process(df_test.iloc[0, 0])]


def sort_coo(coo_matrix):
    tuples = zip(coo_matrix.col, coo_matrix.data)
    return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)


def extract_topn_from_vector(feature_names, sorted_items, topn=10):
    """get the feature names and tf-idf score of top n items"""

    # use only topn items from vector
    sorted_items = sorted_items[:topn]

    score_vals = []
    feature_vals = []

    for idx, score in sorted_items:
        fname = feature_names[idx]

        # keep track of feature name and its corresponding score
        score_vals.append(round(score, 3))
        feature_vals.append(feature_names[idx])

    # create a tuples of feature,score
    #results = zip(feature_vals,score_vals)
    results = {}
    for idx in range(len(feature_vals)):
        results[feature_vals[idx]] = score_vals[idx]

    return results


# do once
feature_names = cv.get_feature_names()

# generate tf-idf for the given document
tf_idf_vector = tfidf_transformer.transform(cv.transform(test))

# sort the tf-idf vectors by descending order of scores
sorted_items = sort_coo(tf_idf_vector.tocoo())

# extract only the top n; n here is 20
keywords = extract_topn_from_vector(feature_names, sorted_items, 20)

# now print the results
print("\n===Keywords===")
for k in keywords:
    print(k, keywords[k])
