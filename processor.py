import json
from string import printable
import pandas as pd
import os
from bs4 import BeautifulSoup as bs
import bs4

bios_html_path = 'html/solidarity/biogramy/'
# unused test file (first file)
test_file_name = '14879,Abgarowicz-Lukasz.html'

# initialize json data
json_data = dict()
invalid_tags = ['strong']

def get_abvs():
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
                # add new info to json dump
                json_data[id] = new_info
    os.chdir(orig)
    # write info to a json dump
    with open('biogramy_info.json', 'w', encoding='utf8') as outfile:
        json.dump(json_data, outfile, indent=4, ensure_ascii=False)
    return 0
def main():
    abvs  = get_abvs()
    print(abvs)

if __name__ == '__main__':
    main()