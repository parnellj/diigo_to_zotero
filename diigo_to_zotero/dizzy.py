import urllib2
import pdfkit
import csv
import os
from bs4 import BeautifulSoup


# The path of the CSV. Must have columns 'URL' and 'Custom 3' (PDF name)
INPATH = os.path.join('.', 'inputs')
OUTPATH = os.path.join('.', 'outputs')
DOCPATH = os.path.join(INPATH, 'doc')
# Some pages block bots so impersonate a browser
opener = urllib2.build_opener()
opener.addheaders = [('User-Agent', 'Mozilla/5.0')]

# Workaround because the pdfkit wrapper doesn't work correctly
path_wkhtmltopdf = b'C:\Program Files\wkhtmltopdf\\bin\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

opener_errors = []
webContent_errors = []
wkhtmltopdf_errors = []

ris_lines = []

for d in [INPATH, OUTPATH, DOCPATH]:
    if not os.path.exists(d):
        os.mkdir(d)

with open(os.path.join(INPATH, 'diigo_dump_20161231_r1.csv'), 'rb') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
    rows = [r for r in reader]
    for i, r in enumerate(rows):
        if os.path.isfile(os.path.join(DOCPATH, r['Custom 3'] + '.pdf')) and \
                os.path.isfile(os.path.join(DOCPATH, r['Custom 3'] + '.html')):
            print 'already generated, continuing on'
            continue

        try:
            response = opener.open(r['UR'])
        except:
            print 'error with opener'
            opener_errors.append(r['L1'])
        try:
            webContent = response.read()
        except:
            'error reading web content'
            webContent_errors.append(r['L1'])
            continue
        with open(os.path.join(DOCPATH, r['Custom 3'] + '.html'), 'w') as html_file:
            soup = BeautifulSoup(webContent, 'lxml')
            [s.extract() for s in soup(['script', 'canvas', 'img', 'link'])]
            html = soup.prettify('utf-8')
            html_file.write(html)
            try:
                print 'PDFing: ' + r['Custom 3']
                pdfkit.from_string(html.decode('utf-8'),
                                   OUTPATH + 'doc/' + r['Custom 3'] + '.pdf',
                                   configuration=config)
            except IOError:
                'error creating PDF'
                wkhtmltopdf_errors.append(r['L1'])

            del soup

with open(os.path.join(INPATH, 'diigo_dump_20161231_r1.csv'), 'r') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
    rows = [r for r in reader]
    for i, r in enumerate(rows):
        ris_lines.append('TY  - ' + r['TY'])
        ris_lines.append('KW  - ' + r['KW'])
        ris_lines.append('L1  - ' + os.path.join(DOCPATH, r['Custom 3'] + '.html'))
        ris_lines.append('L1  - ' + os.path.join(DOCPATH, r['Custom 3'] + '.pdf'))
        ris_lines.append('M1  - ' + r['M1'])
        [ris_lines.append('N1  - ' + n) for n in r['N1'].split('Highlight:')[1:]]
        ris_lines.append('ST  - ' + r['TI'])
        ris_lines.append('TI  - ' + r['TI'])
        ris_lines.append('UR  - ' + r['UR'])
        ris_lines.append('ID  - ' + str(i))
        ris_lines.append('ER  - ')

with open(os.path.join(OUTPATH, 'ris_db.txt'), 'w') as outfile:
    outfile.write('\n'.join(ris_lines))
