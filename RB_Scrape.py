from bs4 import BeautifulSoup
import requests
import pandas as pd
import pymongo

def scrape_title(query):
    # URL of page to be scraped 
    base_url = 'https://reelgood.com'
    url = f'{base_url}/search?q={query}'

    # GET RESULTS (SHOWS). PARSE HTML.
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    dict_result = {}
    # DO WE HAVE A RESULT (A SHOW) ?
    results_exist = len(soup.select('.e1qyeclq5 a')) > 0 
    if not results_exist:
        dict_result = {'title': 'Title not found' }
        return dict_result
    
    link = soup.select('.e1qyeclq5 a')[0]['href']
    show_url = base_url + link
    print(show_url)

    show_response = requests.get(show_url)
    show_soup = BeautifulSoup(show_response.text, 'html.parser')

   
    try:  # TRY PARSING ALL THE FIELDS
        title = ''
        if len(show_soup.select('h1.e14injhv7')) > 0:
            title = show_soup.select('h1.e14injhv7')[0].text

        desc = ''
        if len(show_soup.select('p[itemprop=description]')) > 0:
            desc = show_soup.select('p[itemprop=description]')[0].text

        feature_img = ''
        if len(show_soup.select('.e1x40mdt0 picture.e1181ybh0 img.e1181ybh1')) > 0:
            feature_img = show_soup.select(
                '.e1x40mdt0 picture.e1181ybh0 img.e1181ybh1')[0]['src']

        services = []
        if len(show_soup.select('.e126mwsw1 span[class*=hou113]')) > 0:
            services = show_soup.select('.e126mwsw1 span[class*=hou113]')

        recommended = []
        if len(show_soup.select('.e1yfir8f4 .e1qyeclq4')) > 0:
            elements = show_soup.select('.e1yfir8f4 .e1qyeclq4')
            recommended = [r.text for r in elements]

        country = ''
        if len(show_soup.select('.css-10wrqt0[href*=origin]')) > 0:
            country = show_soup.select('.css-10wrqt0[href*=origin]')[0].text

        maturity = ''
        if len(show_soup.select('span[title*=rating]')) > 0:
            maturity = show_soup.select('span[title*=rating]')[0].text

        genre = show_soup.find('a', class_='css-10wrqt0').text
        rating = show_soup.find('span', class_='ey4ir3j3').text

        dict_result['title'] = title
        dict_result['services'] = [s.text for s in set(services)]
        dict_result['description'] = desc
        dict_result['feature_img'] = feature_img
        dict_result['genre'] = genre
        dict_result['rating'] = rating
        dict_result['maturity'] = maturity
        dict_result['country'] = country
        dict_result['recommended'] = recommended
        dict_result['query'] = query
    except:
        dict_result = {'title': 'Title not found'}
        print(f'err: dict_result parse error {query}')
        raise

    print(f"scraped {dict_result['title']}  {query}")

    return dict_result
