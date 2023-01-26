import sys
import json
import lxml.html
from .utils import make_request, make_link_absolute 


def scrape_park_page(url):
    """
    This function takes a URL to a park page and returns a
    dictionary with the title, address, description,
    and history of the park.
    Parameters:
        * url:  a URL to a park page
    Returns:
        A dictionary with the following keys:
            * url:          the URL of the park page
            * name:         the name of the park
            * address:      the address of the park
            * description:  the description of the park
            * history:      the history of the park
    """

    answer = {}

    resp = make_request(url)
    root = lxml.html.fromstring(resp.text)

    #name
    names = root.cssselect('.page-title .section')
    answer['name'] = names[0].text_content()
    #address
    addresses = root.cssselect('.address')
    answer['address'] = addresses[0].text_content()
    #description
    descrips = root.cssselect('.block-title')
    for d in descrips:
        if d.text_content() == ' Description ':
            answer['description'] = d.getnext().text_content()
    #history
    historys = root.cssselect('.block-title')
    for h in historys:
        answer['history'] = ''
        if h.text_content() == ' History ':
            answer['history'] = h.getnext().text_content()
    #url
    answer['url'] = url

    return answer


def get_park_urls(url):
    """
    This function takes a URL to a page of parks and returns a
    list of URLs to each park on that page.
    Parameters:
        * url:  a URL to a page of parks
    Returns:
        A list of URLs to each park on the page.
    """
    urls = []

    resp = make_request(url) 
    root = lxml.html.fromstring(resp.text)

    #url
    links = list(root.iterlinks())
    for l in links:
        _, _, link, _ = l
        if link[:7] == '/parks/':
            urls.append(make_link_absolute(link,url))

    return urls


def get_next_page_url(url):
    """
    This function takes a URL to a page of parks and returns a
    URL to the next page of parks if one exists.
    If no next page exists, this function returns None.
    """
    answer = None

    resp = make_request(url) 
    root = lxml.html.fromstring(resp.text)

    links = list(root.iterlinks())
    for l in links:
        e, _, link, _ = l
        if link[:5] == '?page' and e.text_content() == 'Next »':
            answer = make_link_absolute(link, url)

    return answer


def crawl(max_parks_to_crawl):
    """
    This function starts at the base URL for the parks site and
    crawls through each page of parks, scraping each park page
    and saving output to a file named "parks.json".
    Parameters:
        * max_parks_to_crawl:  the maximum number of pages to crawl
    """
    list_page_url = "https://scrapple.fly.dev/parks"
    parks = []
    urls_visited = 0

    while urls_visited < max_parks_to_crawl:
        details= get_park_urls(list_page_url)
        for i in details:
            parks.append(scrape_park_page(i))
        list_page_url = get_next_page_url(list_page_url)
        if list_page_url == None:
            break
        urls_visited = urls_visited + 1

    print("Writing parks.json")
    with open("parks.json", "w") as f:
        json.dump(parks, f, indent=1)


if __name__ == "__main__":
    """
    Tip: It can be convenient to add small entrypoints to submodules
         for ease of testing.
    In this file, we call scrape_park_page with a given URL and pretty-print
    the output.
    This allows testing that function from the command line with:
    $ python -m parks.crawler https://scrapple.fly.dev/parks/4
    Feel free to modify/change this if you wish, you won't be graded on this code.
    """
    '''
    from pprint import pprint
    if len(sys.argv) != 2:
        print("Usage: python -m parks.crawler <url>")
        sys.exit(1)
    result = scrape_park_page(sys.argv[1])
    pprint(result)'''

crawl(3)