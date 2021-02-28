import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as soup
from datetime import datetime as dt


def scrape_all():

    # Create executable path for chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=True)

    # store news variables
    news_title, news_p = mars_news(browser)

    # store data in dictionary
    data = {
        'news_title': news_title,
        'news_paragraph': news_p,
        'featured_image': featured_image(browser),
        'facts': mars_facts(browser),
        'comp': mars_earth_comp(browser),
        'mars_size_img': mars_earth_image(browser),
        'hemispheres': hemi_photos(browser),
        'last_modified': dt.now()
    }

    # stop webdriver & return data
    browser.quit()
    return data


def mars_news(browser):

    # Scrape Mars News Titles & Summaries

    # Visit mars.nasa.gov
    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)

    # Delay to allow page to fully load (optional)
    browser.is_element_present_by_css('ul.item_list li.slide', wait_time=1)

    try:
        # Create parent element for most recent news story
        slide_elem = soup(browser.html, 'html.parser').select_one(
            'ul.item_list li.slide')

        # Get title & summary from parent element
        news_title = slide_elem.find('div', class_='content_title').get_text()
        news_p = slide_elem.find('div', class_='article_teaser_body').text

    # add exception for error caused by webpage changing format
    except AttributeError:
        return None, None

    return news_title, news_p


def featured_image(browser):

    # Scrape featured image

    # Visit featured image website
    images_url = 'http://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(images_url)

    # Click 'Full Image' button on homepage of site
    browser.click_link_by_partial_text('FULL IMAGE')

    try:
        # Save image url
        img_link_rel = soup(browser.html, 'html.parser').find(
            'img', class_='fancybox-image').get('src')
        img_url = f'http://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_link_rel}'

    except AttributeError:
        return None

    return img_url


def mars_facts(browser):

    # Scrape Mars facts

    # Visit space-facts.com
    facts_url = 'https://space-facts.com/mars/'
    # browser.visit(facts_url)

    try:
        # Store Mars facts table into DataFrame
        df = pd.read_html(facts_url)[0]
        df.columns = ['', 'Mars', 'Earth']
        df.set_index('', inplace=True)
        df
    except BaseException:
        return None

    # Convert dataframe to html
    return df.to_html()


def mars_earth_comp(browser):

    # Scrape Mars facts

    # Visit space-facts.com
    facts_url = 'https://space-facts.com/mars/'
    # browser.visit(facts_url)

    try:
        # Store Mars facts table into DataFrame
        df = pd.read_html(facts_url)[1]
        df.columns = ['', 'Mars', 'Earth']
        df.set_index('', inplace=True)
        df
    except BaseException:
        return None

    # Convert dataframe to html
    return df.to_html()


def mars_earth_image(browser):

    facts_url = 'https://space-facts.com/mars/'
    browser.visit(facts_url)

    try:
        img_link = soup(browser.html, 'html.parser').find(
            'img', class_='wp-image-6263').get('src')

    except AttributeError:
        return None

    return f'{img_link}'


def hemi_photos(browser):

    # Visit webpage
    base_url = 'https://astrogeology.usgs.gov'
    hemisphere_url = f'{base_url}/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemisphere_url)

    # Get list of links to each hemisphere page
    item_links = soup(browser.html, 'html.parser').find_all(
        'a', class_='itemLink product-item')
    links = []
    for item in item_links:
        rel_link = item.get('href')
        new_link = f'{base_url}{rel_link}'
        if new_link in links:
            continue
        else:
            links.append(new_link)
    links

    # create list to hold dictionaries of each hemisphere's image link and title
    hemispheres = []

    # Populate dictionary
    for link in links:

        # Visit page for hemisphere
        browser.visit(link)

        hemi_dict = {}

        # Get link to full resolution photo
        img_rel_link = soup(browser.html, 'html.parser').find_all(
            'img', class_='wide-image')
        img_rel_link = img_rel_link[0].get('src')
        hemi_link = f'{base_url}{img_rel_link}'
        hemi_dict['img_link'] = hemi_link

        # Get Hemisphere name from link
        hemi_words = link.split('/')
        hemisphere = hemi_words[-1].split('_')[0:-1]
        hemi_name = ''
        for word in hemisphere:
            hemi_name = hemi_name + ' ' + \
                word[0].upper() + word[1:]
        hemi_name = hemi_name[1:] + ' Hemisphere'
        hemi_dict['title'] = hemi_name

        hemispheres.append(hemi_dict)

    return hemispheres


if __name__ == '__main__':
    # If running as script, print scraped data
    print(scrape_all())
