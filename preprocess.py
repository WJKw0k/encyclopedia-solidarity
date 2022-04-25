from string import printable
import pandas as pd
import json
import googletrans
from googletrans import Translator

def translate_sent(sent, translator, name=None):
    try:
        english = translator.translate(sent, src='pl', dest='en')
    except:
        print(sent)
        return ''
    english = english.text
    english = name + ' ' + english if name else english
    return english

def dict_to_csv(dict, name):
    df = pd.DataFrame(dict)
    df.to_csv(name, index=False)

def get_abvs():
    # open a txt
    abvs = {}
    with open('solidarity.abbreviations.txt', 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                line = line.split(' * ')
                abvs[line[0].strip()] = line[1].strip()
    return abvs

def dict_to_df(dict):
    df = pd.DataFrame(dict)
    # find row with max length


def strip_polish_punct(sent):
    for char in sent:
        if char not in printable:
            sent = sent.replace(char, '')
    return sent

def json_to_csv(json_file, json_file2):
    translator = Translator()

    abvs  = get_abvs()
    # create a dataframe
    sents = []
    # read json as dict
    with open(json_file, 'r') as f:
        data = json.load(f)
    for key in data:
        # add data[key] to df
        bio = data[key]['bio']
        name = data[key]['name']
        # erase last sent
        bio = bio[:-1]
        bio = [sent for sent in bio if sent]
        for sent in bio:
            sent = sent.strip()
            # if not empty
            if len(sent) > 0:
                for abv in abvs:
                    sent = sent.replace(abv, abvs[abv])
                sent = translate_sent(sent, translator, name)
                sents.append(sent)
    with open(json_file2, 'r') as f:
        data = json.load(f)
    for key in data:
        # add data[key] to df
        bio = data[key]['org_info']
        # erase last sent
        bio = bio[:-1]
        bio = [sent for sent in bio if sent]
        for sent in bio:
            sent = sent.strip()
            # if not empty
            if len(sent) > 0:
                for abv in abvs:
                    sent = sent.replace(abv, abvs[abv])
                    sent = translate_sent(sent, translator)
                sents.append(sent)
    # convert sents to csv
    df = pd.DataFrame(sents)
    # rename col
    df.columns = ['sentence']
    df.to_csv('sents_en.csv', index=False)

def translate():
    translator = Translator()
    #read sents.csv as df
    df = pd.read_csv('biogramy_info.csv')
    #apply translator.translate(sent, src='pl', dest='en') to column
    df['sentence'] = df['sentence'].apply(lambda sent: translate_sent(sent, translator))
    #save df to csv
    df.to_csv('sents_en2.csv', index=False)

def get_insights():
    df = pd.read_csv('graph2.csv')
    print(df.head())
    # get most frequent source
    sources = df['source'].value_counts()
    # sort by count
    sources = sources.sort_values(ascending=False)
    # save to csv
    sources.to_csv('sources.csv', index=True)
    # get most frequent edge
    edges = df['edge'].value_counts()
    # sort by count
    edges = edges.sort_values(ascending=False)
    # save to csv
    edges.to_csv('edges.csv', index=True)
    # get most frequent target
    targets = df['target'].value_counts()
    # sort by count
    targets = targets.sort_values(ascending=False)
    # save to csv
    targets.to_csv('targets.csv', index=True)
    # count where edge is "graduate of"
    graduate = df[df['edge'] == 'graduated from']
    graduate = graduate['target'].value_counts()
    # sort by count
    graduate = graduate.sort_values(ascending=False)
    # save to csv
    graduate.to_csv('graduate.csv', index=True)


def main():
    # json_to_csv('biogramy_info.json', 'orgs_info.json')
    # translate()
    get_insights()


if __name__ == '__main__':
    main()