import time
import urllib
import time
import urllib
import datetime
from collections import Counter, defaultdict
import xml.etree.ElementTree as ET

from bs4 import BeautifulSoup
import matplotlib.pylab as plt
import pandas as pd
import numpy as np
import bibtexparser

'''
Following https://nbviewer.jupyter.org/url/betatim.github.io//downloads/notebooks/arXiv.ipynb by TimHead

'''

pd.set_option('mode.chained_assignment', 'warn')


def harvest(arxiv="math", start="2009-01-01", end="2018-12-31"):
    #df = pd.DataFrame(columns=("title", "abstract", "categories", "created", "id", "doi"))
    print("start:")
    OAI = "{http://www.openarchives.org/OAI/2.0/}"
    ARXIV = "{http://arxiv.org/OAI/arXiv/}"
    base_url = "http://export.arxiv.org/oai2?verb=ListRecords&"
    url = (base_url +
           "from=" + start + "&until=" + end + "&" +
           "metadataPrefix=arXiv&set=%s" % arxiv)

    big_contents = []
    while True:
        print("fetching", url)
        try:
            response = urllib.request.urlopen(url)

        except urllib.request.HTTPError as e:
            if e.code == 503:
                to = int(e.hdrs.get("retry-after", 30))
                print("Got 503. Retrying after {0:d} seconds.".format(to))

                time.sleep(to)
                continue

            else:
                raise

        xml = response.read()

        root = ET.fromstring(xml)

        for record in root.find(OAI + 'ListRecords').findall(OAI + "record"):
            arxiv_id = record.find(OAI + 'header').find(OAI + 'identifier')
            meta = record.find(OAI + 'metadata')
            if meta == None:
                continue
            info = meta.find(ARXIV + "arXiv")
            created = info.find(ARXIV + "created").text
            created = datetime.datetime.strptime(created, "%Y-%m-%d")
            if info.find(ARXIV + "updated") == None:
                updated = created
            else:
                updated = info.find(ARXIV + "updated").text
                updated = datetime.datetime.strptime(updated, "%Y-%m-%d")

            categories = info.find(ARXIV + "categories").text

            # if there is more than one DOI use the first one
            # often the second one (if it exists at all) refers
            # to an eratum or similar
            #doi = info.find(ARXIV + "doi")
            # if doi is not None:
            #    doi = doi.text.split()[0]

            names = []
            for author in info.find(ARXIV + "authors").findall(ARXIV + "author"):
                last = " ".join(list(map(lambda x: x.text, author.findall(ARXIV + "keyname"))))
                first = " ".join(list(map(lambda x: x.text, author.findall(ARXIV + "forenames"))))
                names += [first + " " + last]

            contents = {'title': info.find(ARXIV + "title").text,
                        'id': info.find(ARXIV + "id").text,  # arxiv_id.text[4:],
                        'abstract': info.find(ARXIV + "abstract").text.strip(),
                        'created': created,
                        'updated': updated,
                        'categories': categories.split(),
                        #'doi': doi,
                        'authors': names,

                        }
            big_contents += [contents]
            #df = df.append(contents, ignore_index=True)

        # The list of articles returned by the API comes in chunks of
        # 1000 articles. The presence of a resumptionToken tells us that
        # there is more to be fetched.
        token = root.find(OAI + 'ListRecords').find(OAI + "resumptionToken")
        if token is None or token.text is None:
            break

        else:
            url = base_url + "resumptionToken=%s" % (token.text)
    df = pd.DataFrame(big_contents)
    df = df.sort_values(by=["created"])
    df = df.reset_index().drop(columns=["index"])
    return df
