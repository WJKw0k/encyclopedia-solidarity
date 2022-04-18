from string import printable
import pandas as pd

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
def main():
    abvs  = get_abvs()
    print(abvs)

if __name__ == '__main__':
    main()