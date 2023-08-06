## Main function: header_analysis(text)
## input file: readme files text data
## output file: json files with categories extracted using header analysis; other text data cannot be extracted
import string

import numpy as np
import pandas as pd
import re
from textblob import Word
import json

# Define wordnet groups
group = dict()

#Word("citation").synsets[2] -> Includes ack, which is not the right sense
citation = [Word("citation").synsets[3],Word("reference").synsets[1], Word("cite").synsets[3]]
group.update({"citation": citation})

ack = [Word("acknowledgement").synsets[0]]
group.update({"acknowledgement": ack})

run = [Word("run").synsets[9], Word("run").synsets[34], Word("execute").synsets[4]]
group.update({"run": run})

install = [Word("installation").synsets[0], Word("install").synsets[0], Word("setup").synsets[1],
           Word("prepare").synsets[0], Word("preparation").synsets[0], Word("manual").synsets[0],
           Word("guide").synsets[2], Word("guide").synsets[9]]
group.update({"installation": install})

download = [Word("download").synsets[0]]
group.update({"download": download})

requirement = [Word("requirement").synsets[2], Word("prerequisite").synsets[0], Word("prerequisite").synsets[1],
               Word("dependency").synsets[0], Word("dependent").synsets[0]]
group.update({"requirement": requirement})

contact = [Word("contact").synsets[9]]
group.update({"contact": contact})

description = [Word("description").synsets[0], Word("description").synsets[1],
               Word("introduction").synsets[3], Word("introduction").synsets[6],
               Word("basics").synsets[0],
               Word("initiation").synsets[1],
#               Word("overview").synsets[0],
               Word("summary").synsets[0], Word("summary").synsets[2]]
group.update({"description": description})

contributor = [Word("contributor").synsets[0]]
group.update({"contributor": contributor})

documentation = [Word("documentation").synsets[1]]
group.update({"documentation": documentation})

license = [Word("license").synsets[3], Word("license").synsets[0]]
group.update({"license": license})

usage = [Word("usage").synsets[0], Word("example").synsets[0], Word("example").synsets[5],
         #Word("implement").synsets[1],Word("implementation").synsets[1],
         Word("demo").synsets[1], Word("tutorial").synsets[0],
         Word("tutorial").synsets[1],
         Word("start").synsets[0], Word("start").synsets[4], Word("started").synsets[0],
         Word("started").synsets[1], Word("started").synsets[7], Word("started").synsets[8]]
group.update({"usage": usage})

#update = [Word("updating").synsets[0], Word("updating").synsets[3]]
#group.update({"update": update})

# Needs to be revisited
#Word("issues").synsets[0],
faq = [Word("errors").synsets[5], Word("problems").synsets[0],
          Word("problems").synsets[2], Word("faq").synsets[0]]
group.update({"faq": faq})

support = [Word("support").synsets[7], Word("help").synsets[0], Word("help").synsets[9], Word("report").synsets[0],
           Word("report").synsets[6]]
group.update({"support": support})

def extract_bash_code(text):
    splitted = text.split("```")
    output = []
    if (len(splitted)>=3):
        for index, value in enumerate(splitted):
            if index%2 == 1:
                output.append(splitted[index])
    return output

def extract_header_content(text):  # extract the header and content of text to dataframe
    print('Extracting headers and content.')
    # check the format of header
    underline_header = re.findall('.+[\n]={3,}[\n]', text)
    hash_header = re.findall('#{1,5} .*[\n][\n]', text)

    # header declared with ==== and --- Since creating a single regex for both is complicated,
    # We select the maximum number of headers we can match
    if len(underline_header) != 0 and len(underline_header) > len(hash_header):
        header = re.findall('.+[\n][=-]+[\n]+', text)
        header = [re.sub('[\n][=-]+[\n]', '', i) for i in header]
        content = re.split('.+[\n][=-]+[\n]+', text)
        # Remove the first entry, as it is always empty
        content = content[1:]

    # header declared with ##
    else:
        #a = re.findall(r'\`\`\`[^\`]+\`\`\`', text, flags=re.DOTALL)
        #replace call to re.findall for extract_bash_code to solve GitHub issue 231
        a = extract_bash_code(text)
        a_sub = [re.sub('#', '#notes:', i) for i in a]
        for i, j in zip(a, a_sub):
            text = text.replace(i, j)
        header = re.findall('#{1,5} .*', text)
        header = [re.sub('#', '', i) for i in header]
        content = re.split('#{1,6} .*', text)
        content = [re.sub('#notes', '#', i) for i in content]
        content = [re.sub("[\n]+", '', i, 1) for i in content]
        # Remove the first entry, as it is always empty
        content = content[1:]

    # into dataframe
    df = pd.DataFrame(columns=['Header', 'Content'])
    for i, j in zip(header, content):
        df = df.append({'Header': i, 'Content': j}, ignore_index=True)
    df['Content'].replace('', np.nan, inplace=True)
    df.dropna(subset=['Content'], inplace=True)
    return df


def find_sim(wordlist, wd):
    """
    Function that returns the max probability between a word and subgroup
    Parameters
    ----------
    wordlist
    wd

    Returns
    -------

    """
    sim_value = []
    for sense in wordlist:
        if (wd.path_similarity(sense) != None):
            sim_value.append(wd.path_similarity(sense))
    if (len(sim_value) != 0):
        return max(sim_value)
    else:
        return 0


def match_group(word_syn, group, threshold):  # match a word with a subgroup
    currmax = 0
    maxgroup = ""
    simvalues = dict()
    for sense in word_syn:  # for a given sense of a word
        similarities = []
        for key, value in group.items():  # value has all the similar words
            path_sim = find_sim(value, sense)
            # print("Similarity is:",path_sim)
            if (path_sim > threshold):  # then append to the list
                if (path_sim > currmax):
                    maxgroup = key
                    currmax = path_sim
    return maxgroup


def label_header(header):  # label the header with a subgroup
    # remove punctuation
    header_clean = header.translate(str.maketrans('', '', string.punctuation))
    sentence = header_clean.strip().split(" ")
    label = []
    for s in sentence:
        synn = Word(s).synsets
        if (len(synn) > 0):
            bestgroup = match_group(synn, group, 0.8)
            if (bestgroup != "" and bestgroup not in label):
                label.append(bestgroup)
    return label


def clean_html(text):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', text)
    return cleantext


def extract_categories_using_headers(text):  # main function
    #remove call to clean_html to solve GitHub issues 139 and 89
    #text = clean_html(text)
    data = extract_header_content(text)
    print('Labeling headers.')
    if data.empty:
        print("File to analyze has no headers")
        return {}, [text]
    data['Group'] = data['Header'].apply(lambda row: label_header(row))
    if len(data['Group'].iloc[0]) == 0:
        data['Group'].iloc[0] = ['unknown']
    groups = data.apply(lambda x: pd.Series(x['Group']), axis=1).stack().reset_index(level=1, drop=True)
    groups.name = 'Group'
    data = data.drop('Group', axis=1).join(groups)
    if data['Group'].iloc[0] == 'unknown':
        data['Group'].iloc[0] = np.NaN

    # to json
    group = data.loc[(data['Group'] != 'None') & pd.notna(data['Group'])]
    group = group.reindex(columns=['Content', 'Group'])
    group['confidence'] = [[1]] * len(group)
    group.rename(columns={'Content': 'excerpt'}, inplace=True)
    group['technique'] = 'Header extraction'
    group_json = group.groupby('Group').apply(lambda x: x.to_dict('r')).to_dict()
    for key in group_json.keys():
        for ind in range(len(group_json[key])):
            del group_json[key][ind]['Group']
    print('Converting to json files.')

    # strings without tag (they will be classified)
    str_list = data.loc[data['Group'].isna(), ['Content']].values.squeeze().tolist()
    if type(str_list) != list:
        str_list = [str_list]
    return group_json, str_list
