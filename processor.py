import json
from string import printable
import pandas as pd
import os

import spacy as spacy
from bs4 import BeautifulSoup as bs
import bs4
import dateparser

bios_html_path = 'html/solidarity/biogramy/'
orgs_html_path = 'html/solidarity/orgs'
# unused test file (first file)
test_file_name = '14879,Abgarowicz-Lukasz.html'

# initialize json data
json_data = []
invalid_tags = ['strong']

nlp = spacy.load("pl_core_news_sm")


def extract_stuff_from_desc(text):
    stuff = nlp(text)
    dates = dict()
    orgs = dict()
    places = dict()
    grad_phrases = {'ukończył', 'ukończyła', 'absolwent', 'absolwentka'}

    for ent in stuff.ents:
        if ent.label_ == 'date':
            dates[ent.start_char] = dateparser.parse(ent.text)
            if not dates[ent.start_char]:
                tmp = ent.text.split(' ')
                dates[ent.start_char] = dateparser.parse(' '.join(tmp[:3]))
        elif ent.label_ == 'orgName':
            orgs[ent.start_char] = ent.text
        elif ent.label_ == 'placeName':
            places[ent.start_char] = ent.text

    bornFlag = False
    college = None
    collegeFlag = False
    bday = None
    birthPlace = None
    birthPlaceFlag = False
    for i, token in enumerate(stuff):
        if token.text == 'ur':
            bornFlag = True
        elif token.text == 'w':
            birthPlaceFlag = True
        elif birthPlaceFlag and token.idx in places:
            birthPlace = places[token.idx]
            birthPlaceFlag = False
        elif token.text.lower() in grad_phrases:
            collegeFlag = True
        elif collegeFlag and token.idx in orgs:
            college = orgs[token.idx]
            collegeFlag = False
        elif bornFlag and token.idx in dates:
            bday = dates[token.idx]
            bornFlag = False
    if bday:
        bday = str(bday.date())
    else:
        bday = 'none'
    if not college:
        college = 'none'
    if not birthPlace:
        birthPlace = 'none'
    return bday, college, birthPlace


def get_abvs():
    selector = 'strong:has(strong)'
    # save original directory
    orig = os.getcwd()
    # print(os.getcwd())
    # change directories for convenience
    os.chdir(bios_html_path)
    # iterate through all the html files and parse them, collecting useful data
    for filename in os.listdir('.'):
        with open(filename, 'r', encoding='utf8') as f:
            print(filename)
            # get the html files only
            if filename.endswith('.html'):
                souped = bs(f, 'html.parser')
                # get name metadata
                name = souped.find('meta', property='og:title')['content']
                # get description metadata
                description = souped.find('meta', property='og:description')['content']

                bday, college, birthPlace = extract_stuff_from_desc(description)
                # get Birth Year, University,
                # get id from metadata
                id = filename.split(',')[0]
                # parse main article
                article = souped.find('article').find_all('p')

                # do some funny replacement of inner html tags (like <bold>)
                for tag in invalid_tags:
                    for elem in article:
                        for match in elem.findAll(tag):
                            match.replaceWithChildren()
                # bio is a list of paragraphs
                bio = [elem.text for elem in article if elem.text]
                new_info = dict()
                new_info['name'] = name
                new_info['description'] = description
                new_info['bio'] = bio
                new_info['bday'] = bday
                new_info['college'] = college
                new_info['birth_place'] = birthPlace
                # add new info to json dump
                json_data.append(new_info)
    os.chdir(orig)
    # write info to a json dump
    with open('biogramy_info_new.json', 'w', encoding='utf8') as outfile:
        json.dump(json_data, outfile, indent=4, ensure_ascii=False)
    return 0


def get_orgs():
    orgs_data = dict()
    # save original directory
    orig = os.getcwd()
    # print(os.getcwd())
    # change directories for convenience
    os.chdir(orgs_html_path)
    # iterate through all the html files and parse them, collecting useful data
    for filename in os.listdir('.'):
        with open(filename, 'r', encoding='utf8') as f:
            print(filename)
            # get the html files only
            if filename.endswith('.html'):
                souped = bs(f, 'html.parser')
                title = souped.find('meta', property='og:title')['content']
                # get description metadata
                description = souped.find('meta', property='og:description')['content']
                # get id from metadata
                id = filename.split(',')[0]
                # get keywords from metadata
                keywords = souped.find('meta', attrs={'name': 'keywords'})['content'].split(',')
                # parse main article
                article = souped.find('article').find_all('p')

                # do some funny replacement of inner html tags (like <bold>)
                for tag in invalid_tags:
                    for elem in article:
                        for match in elem.findAll(tag):
                            match.replaceWithChildren()
                # info is a list of paragraphs
                info = [elem.text for elem in article if elem.text]
                new_info = dict()
                new_info['title'] = title
                new_info['description'] = description
                new_info['org_info'] = info
                new_info['keywords'] = keywords
                # add new info to json dump
                orgs_data[id] = new_info
    os.chdir(orig)
    # write info to a json dump
    with open('orgs_info.json', 'w', encoding='utf8') as outfile:
        json.dump(orgs_data, outfile, indent=4, ensure_ascii=False)
    return 0


def get_orgs_metadata():
    # this function is broken disregard for now
    info = {'names': set(), 'orgs': set()}
    orig = os.getcwd()
    os.chdir(orgs_html_path)
    print(os.listdir('.'))
    with open('index_bios.html', 'r', encoding='utf8') as f:
        souped = bs(f, 'html.parser')
        name_tags = souped.find_all('li', property='_3r')
        for tag in name_tags:
            name_tag = tag.find('a')
            info['names'].add(name_tag.text)
    with open('index_orgs.html', 'r', encoding='utf8') as f:
        souped = bs(f, 'html.parser')
        org_tags = souped.find_all('li', property='_3r')
        for tag in org_tags:
            org = tag.find('a')
            info['names'].add(org.text)
    os.chdir(orig)
    with open('orgs_and_bios.json', 'w', encoding='utf8') as outfile:
        json.dump(info, outfile, indent=4, ensure_ascii=False)

# read the bio inifo from json
def read_bio_info():
    df = pd.read_json('biogramy_info_new.json')
    print('done')



def main():
    # get_orgs()
    abvs  = get_abvs()
    print(abvs)


if __name__ == '__main__':
    main()
