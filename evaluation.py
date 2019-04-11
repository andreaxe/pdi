import os
import requests
import xml.etree.ElementTree as ET
from urllib.parse import urlparse, ParseResult


def evaluate_websites(file='crawler_results.txt'):
    """
    :return:
    """
    api_id = 'd306f1a5fd30841c0f78325ef85993367f97da39'

    # with open('sites_list.txt', 'r') as f:
    with open(file, 'r') as f:
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
