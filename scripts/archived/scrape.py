"""
A very simple and basic web scraping script. Feel free to
use this as a source of inspiration, but, make sure to attribute
it if you do so.

This is by no means production code.
"""
# built-in imports
import re
import json

import requests

# user packages
from bs4 import BeautifulSoup
from urllib.request import urlopen

# constants
BASE_URL = "https://www.domain.com.au"
N_PAGES = range(1, 51) # update this to your liking

HEADERS = {"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"}

def get(url):
    response = requests.get(url, headers=HEADERS)
    while response.status_code == 502:
        response = requests.get(url, headers=HEADERS)
    return response

# begin code
url_links = []
data = []

# generate list of urls to visit
for page in N_PAGES:
    print("%s.." % page, end='')
    url = BASE_URL + f"/rent/melbourne-region-vic/?sort=price-desc&page={page}"
    
    bs_object = BeautifulSoup(get(url).text, "html.parser")

    # find the unordered list (ul) elements which are the results, then
    # find all href (a) tags that are from the base_url website.
    index_links = bs_object \
        .find(
            "ul",
            {"data-testid": "results"}
        ) \
        .findAll(
            "a",
            href=re.compile(f"{BASE_URL}/*") # the `*` denotes wildcard any
        )

    for link in index_links:
        # if its a property address, add it to the list
        if 'address' in link['class']:
            url_links.append(link['href'])


# for each url, scrape some basic metadata
for property_url in url_links[1:]:
    property_metadata = dict()
    
    bs_object = BeautifulSoup(get(property_url).text, "html.parser")
    
    property_metadata['url'] = property_url
    
    # looks for the header class to get property name
    property_metadata['name'] = bs_object \
        .find("h1", {"class": "css-164r41r"}) \
        .text

    # looks for the div containing a summary title for cost
    property_metadata['cost_text'] = bs_object \
        .find("div", {"data-testid": "listing-details__summary-title"}) \
        .text

    # extract coordinates from the hyperlink provided
    # i'll let you figure out what this does :P
    property_metadata['coordinates'] = [
        float(coord) for coord in re.findall(
            r'destination=([-\s,\d\.]+)', # use regex101.com here if you need to
            bs_object \
                .find(
                    "a",
                    {"target": "_blank", 'rel': "noopener noreferer"}
                ) \
                .attrs['href']
        )[0].split(',')
    ]

    try:
        property_metadata['rooms'] = [
            re.findall(r'\d\s[A-Za-z]+', feature.text)[0] for feature in bs_object \
                .find("div", {"data-testid": "property-features"}) \
                .findAll("span", {"data-testid": "property-features-text-container"})
        ]
    except IndexError:
        # Not all property listings have a property-features div
        pass

    property_metadata['desc'] = re \
        .sub(r'<br\/>', '\n', str(bs_object.find("p"))) \
        .strip('</p>')
        
    data.append(property_metadata)

# output to example json in data/raw/
with open('../data/raw/example.json', 'w') as f:
    f.write(json.dumps(data, indent=2))
    # print('dumps: %.3f' % timeit.timeit(
    #     lambda: f.write(json.dumps(data,indent=2)), number=1000))
    # print('dump:  %.3f' % timeit.timeit(
    #     lambda: json.dump(data,f,indent=2), number=1000))
    
