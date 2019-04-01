# -*- coding: utf-8 -*-
import os
import re
import requests
from tld import get_tld
from bs4 import BeautifulSoup
from tldextract import extract
import xml.etree.ElementTree as ET
from urllib.parse import urlparse, ParseResult

links = []
checked_links = []
global_links = []
api_id = 'd306f1a5fd30841c0f78325ef85993367f97da39'


def evaluate_websites():
    """
    :return:
    """
    with open('sites_list.txt', 'r') as f:
        websites = [line.strip() for line in f]

    for website in websites:

        url = parse_url_string(website)
        print("Checking website: " + url)
        guides = 'WCAG2-A,WCAG2-AA,WCAG2-AAA'
        api_url = 'https://achecker.ca/checkacc.php?uri={}&id={}&guide={}&output=rest'.format(url, api_id, guides)
        print(api_url)
        r = requests.get(api_url)

        from xml.etree.ElementTree import ParseError

        try:
            # save results to a xml file
            path = os.path.join('adchecker_results', url.replace("http://www.", "") + '.xml')
            with open(path, 'wb') as f:
                f.write(r.content)
            root = ET.fromstring(r.content)
        except ParseError as e:
            print("Website: {} has an error: {}" .format(url, repr(e)))
            continue

        # responseXml = ET.fromstring(response_xml_as_string)

        for child in root.iter('*'):
            print(child.tag)

        for child in root.iter('summary'):
            print(child.tag, child.attrib)


def parse_url_string(url):
    """
    :param url: String url unparsed
    :return:
    """

    p = urlparse(url, 'http')
    netloc = p.netloc or p.path
    path = p.path if p.netloc else ''
    if not netloc.startswith('www.'):
        netloc = 'www.' + netloc

    p = ParseResult('http', netloc, path, *p[3:])
    return p.geturl()


def crawl_web():
    """
    Method to start crawling website links
    :return:
    """

    # Start of the crawling
    webpage = 'https://www.eapn.pt/links/governo-da-republica-portuguesa-e-instituicoes-publicas'
    parse_page(webpage)

    while [len(links) > 0]:
        if links[0] not in checked_links:
            parse_page(links[0])
            checked_links.append(links[0])
        links.remove(links[0])

    # webpage = "http://cite.gov.pt"


def parse_page(site):
    """
    Funcão para descobrir sites relacionados com o Governo Português
    :param site:
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
    if len(links) > 0 and len(global_links) < 1500:
        return
    else:
        with open('no_recursion2.txt', 'w') as f:
            for item in global_links:
                f.write("%s\n" % item)
        print(global_links)
        exit()  # end program


def elements(argument):

    elements_required = ['status', 'NumOfErrors', 'NumOfLikelyProblems', 'NumOfPotentialProblems']
    if argument in elements_required:
        return True
    return False


if __name__ == '__main__':

    evaluate_websites()
    exit()
    # file = os.path.join('adchecker_results', 'rccgestao.gov.pt.xml')
    file = os.path.join('adchecker_results', 'gep.msess.gov.pt.xml.xml')

    import xml.etree.ElementTree as ET

    root = ET.parse(file).getroot()
    print([elem.tag for elem in root.iter()])

    e = ET.ElementTree(ET.parse(file))

    country = e.findall('resultset')
    print(len(country))

    for c in range(len(country)):
        print(c)
    for elt in e.iter():
        if element_of_interest(elt.tag):
            print("{}: {}".format(elt.tag, elt.text))

    for summary in root.iter('resultset/summary'):
        print(summary)
