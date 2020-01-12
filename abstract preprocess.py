from pathlib import Path
import glob
import os
import re
from langdetect import detect

# make one file from raw .txt files in a folder
pathlist = Path(
    "/home/kseniia/Projects/ALGE/papers-abstracts/").glob("**/*.txt")
with open("result.txt", "wb") as outfile:
    for path in pathlist:
        with open(path, "rb") as infile:
            outfile.write(infile.read())


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


# cleaning
filepath = "/home/kseniia/Projects/ALGE/result.txt"
out = "result_cleaned.txt"
breaker = ["_______NEW__PAPER________"]
delete_list = [
    "Abstract",
    " ,",
    "Conclusion",
    "METHOD",
    "RATIONALE",
    "Objectives",
    "Paper",
    "PAPER",
    "PURPOSE",
    "MATERIALS",
    "PERSPECTIVE",
    "UNLABELLED",
    "BACKGROUND",
    "Results",
    "Methods",
    "Background",
    "OBJECTIVE",
    "CONCLUSION",
    "METHODS",
    "RESULTS",
    "BACKGROUND/AIMS",
    "Context",
    "Introduction",
    "GENERALIZABILITY",
    "QUESTION",
    "ANSWER",
    "AND",
    "SETTING",
    "DESIGN",
    "STUDY",
    "AVAILABILITY",
    "MOTIVATION",
    "DISCUSSION",
    "PARTICIPANTS",
    "MEASUREMENTS",
]
filein = open(filepath)
fileout = open(out, "w+")
counter = 0
# writing a file abstract by abstract with one linebreaker
abstract_lines = []
for line in nonblank_lines(filein):
    if counter > 10000:
        break
    if line in breaker:
        abstract = " ".join(abstract_lines)
        try:
            language = detect(abstract)
            if language == "en":
                for word in delete_list:
                    abstract = abstract.replace(word, "")
                abstract = " ".join(abstract.split())
                fileout.write(abstract + "\n")
                counter += 1
                abstract_lines = []
            else:
                abstract_lines = []
        except:
            abstract_lines = []
    else:
        abstract_lines.append(line)

filein.close()
fileout.close()

