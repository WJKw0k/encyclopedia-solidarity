from string import printable
import pandas as pd
import json

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

def orgs_to_csv(json_file):
    

def json_to_csv(json_file):
    abvs  = get_abvs()
    # create a dataframe
    sents = []
    # read json as dict
    with open(json_file, 'r') as f:
        data = json.load(f)
    for key in data:
        # add data[key] to df
        bio = data[key]['bio']
        # erase last sent
        bio = bio[:-1]
        bio = [sent for sent in bio if sent]
        for sent in bio:
            sent = sent.strip()
            # if not empty
            if len(sent) > 0:
                print(len(sent), sent)
                if len(sent) == 0:
                    print(len(sent))
                for abv in abvs:
                    sent = sent.replace(abv, abvs[abv])
                sents.append(sent)
    # convert sents to csv
    df = pd.DataFrame(sents)
    # rename col
    df.columns = ['sentence']
    df.to_csv('biogramy_info.csv', index=False)
def main():
    
    json_to_csv('biogramy_info.json')


if __name__ == '__main__':
    main()