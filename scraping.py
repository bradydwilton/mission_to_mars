# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as soup

# Create executable path for chromedriver
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)


# Scrape Mars News Titles & Summaries

# Visit mars.nasa.gov
news_url = 'https://mars.nasa.gov/news/'
browser.visit(news_url)

# Delay to allow page to fully load (optional)
browser.is_element_present_by_css('ul.item_list li.slide', wait_time=10)

# Create parent element for most recent news story
slide_elem = soup(browser.html, 'html.parser').select_one(
    'ul.item_list li.slide')

# Get title & summary from parent element
news_title = slide_elem.find('div', class_='content_title').get_text()
news_p = slide_elem.find('div', class_='article_teaser_body').text


# Scrape featured image

# Visit featured image website
images_url = 'http://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
browser.visit(images_url)

# Click 'Full Image' button on homepage of site
browser.click_link_by_partial_text('FULL IMAGE')

# Save image url
img_link_rel = soup(browser.html, 'html.parser').find(
    'img', class_='fancybox-image').get('src')
img_url = f'http://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_link_rel}'

# Scrape Mars facts

# Visit space-facts.com
facts_url = 'https://space-facts.com/mars/'
# browser.visit(facts_url)

# Store Mars facts table into DataFrame
df = pd.read_html('https://space-facts.com/mars/')[0]
df.columns = ['description', 'value']
df.set_index('description', inplace=True)
df

# Convert dataframe to html
df.to_html()

# exit browser
browser.quit()

# print(news_title)
# print(news_p)
# print(img_url)
# print(df)
