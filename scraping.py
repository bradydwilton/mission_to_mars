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
        df.columns = ['description', 'value']
        df.set_index('description', inplace=True)
        df
    except BaseException:
        return None

    # Convert dataframe to html
    return df.to_html()


if __name__ == '__main__':
    # If running as script, print scraped data
    print(scrape_all())
