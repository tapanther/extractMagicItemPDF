#! /usr/bin/env python3

import PyPDF2
import argparse
import re
import csv

#---------------------
# functions
#---------------------

def toInt(string):
    string = string.strip().replace(',','')
    return int(string) if string else ''


#---------------------
# Parse Arguments
#---------------------

parser = argparse.ArgumentParser()

parser.add_argument(
    'infile',
    help = 'PDF to read.'
)

parser.add_argument(
    'outfile',
    nargs='?',
    default='out.csv',
    help = 'Output CSV file.'
)

args = parser.parse_args()

items = list()
pages = list()

with open(args.infile, 'rb') as pdfFileObj:
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    for i in range(2, pdfReader.getNumPages()):
        text = pdfReader.getPage(i).extractText()
        search = r'([\w() ]+)\n'
        search = r'([\w() ]+)\n(Yes|No)?\n?'
        search = r'([\w() ]+)\n(Yes|No)?\n?(\w+)\n'
        search = r'(.*?)\n(Yes|No)?\n?(\w+)\n'
        search = r'(.*?)\n(Yes|No)?\n?(\w+)\n([0-9gp, ]+)\n'
        search = r'(.*?)\n(Yes|No)?\n?(\w+)\n([0-9gp, ]+)\n(.*?)\n'
        search = r'(.*?)\n(.*?)\n?(\w+)\n([0-9gp, ]+)\n(.*?)\n'
        search = r'(.*?)\n(((Yes|No).*?)\n)?(\w+)\n([0-9gp, ]+)\n(.*?)\n'
        search = r'(.*?)\n(((Yes|No).*?)\n)?(([0-9—]+)\n)?(([+0-9—]+)\n)?(\w+)\n([0-9gp, ]+)\n(.*?)\n'
        #          name   AttnNL Attn AttnYN #Rar # dc   ab             Rare        GP             SRC
        search = r'(.*?)\n(((Yes|No).*?)\n)?((([0-9—]+)\+([+0-9—]+))?\n?.*?([A-Z][\w ]+))?\n([0-9, ]+)gp\n(.*?)\n'
        #search = r'([\w() ]+)\n((Yes|No)\n)?(\w+)\n([0-9gp, ]+)\n(\w+)\n'
        #search = r'([\w() ]+)\n((Yes|No)\n)?(\w+)\n([0-9gp, ]+)\n(\w+)\n'
        items.extend(re.findall(search, text, flags=re.MULTILINE))


with open(args.outfile, 'w', newline='') as outfile:
    outfile_writer = csv.writer(outfile, dialect='excel')
    outfile_writer.writerow(['Name','Attunement','DC','Attack Bonus','Rarity','Cost','Source'])

    for item in items:
        name, _, attunement, _, _, _, dc, ab, rarity, cost, source = item
        dc = toInt(dc)
        ab = toInt(ab)
        cost = toInt(cost)
        outfile_writer.writerow([name,attunement,dc,ab,rarity,cost,source])
        print(f'name: {name}\nattunement: {attunement}\nDC = {dc}\nAB = {ab}\nrarity: {rarity}\ncost = {cost}\nsource = {source}\n')
    
        
#print(items)
    
