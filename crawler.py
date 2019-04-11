# -*- coding: utf-8 -*-
import re
import requests
from tld import get_tld
from bs4 import BeautifulSoup
from tldextract import extract
from urllib.parse import urlparse

links = []
checked_links = []
global_links = []


def crawl_web(webpage, limit):
    """
    Method to start crawling website links
    :param webpage:
    :param limit:
    :return:
    """
    # Start of the crawling
    limit = int(limit)
    parse_page(webpage, limit=limit)

    while [len(links) > 0]:
        if links[0] not in checked_links:
            parse_page(links[0], limit)
            checked_links.append(links[0])
        links.remove(links[0])

    # webpage = "http://cite.gov.pt"


def parse_page(site, limit):
    """
    Funcão para descobrir sites relacionados com o Governo Português
    :param site:
    :param limit:
    :return:
    """
    try:

        # ==== Parse page for links
        html_page = requests.get(site, verify=False, timeout=4)
        soup = BeautifulSoup(html_page.content)
        for link in soup.findAll('a', attrs={'href': re.compile("^http://")}):
            verified_link = link.get('href')
            if verified_link not in links  and get_tld(verified_link) == 'pt' or get_tld(verified_link) == 'gov.pt':
                print(verified_link)
                links.append(verified_link)

        # ==== Parse all links for other government links
        for l in links:
            data = urlparse(l)
            if data.netloc and data.netloc not in global_links:
                tsd, td, tsu = extract(data.netloc)  # prints abc, hostname, com
                if tsu == 'pt' or tsu == 'gov.pt':
                    print(data.netloc)
                    global_links.append(data.netloc)

    except Exception as e:
        print(e)

    print("Foram encontrados {} sites ".format(len(global_links)))
    print("Restam {} sites para investigar".format(len(links)))
    if len(links) > 0 and len(global_links) < limit:
        return
    else:
        with open('crawler_results.txt', 'w') as f:
            for item in global_links:
                f.write("%s\n" % item)
        print(global_links)
        from main import menu
        menu()
