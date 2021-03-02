# Mission to Mars

## Description
Web scraping with Python, Splinter, and BeautifulSoup to create a Flask application displaying recent news, images, and statistics about Mars from various sources across the internet. Data is stored with MongoDB and integrated via PyMongo.

## Current Version (1.1)
<img src='https://github.com/bradydwilton/mission_to_mars/blob/main/Images/MissionToMars_1.2.png' width=800>

## Tools Used:
* [Python](https://docs.python.org/3/): scripting
* [Splinter](https://splinter.readthedocs.io/en/latest/): web browser automation
* [BeautifulSoup](https://pypi.org/project/beautifulsoup4/): HTML parsing/scraping
* [Flask](https://flask.palletsprojects.com/en/1.1.x/): create web app to display information
* [JSONify](https://flask.palletsprojects.com/en/1.1.x/api/#module-flask.json): convert data to JSON format
* [Pandas](https://pandas.pydata.org/docs/): data manipulation
* [MongoDB](https://docs.mongodb.com/): data storage and retieval
* [Jupyter Notebook](https://jupyter-notebook.readthedocs.io/en/stable/): testing and development

## Pseudocode

### Scrape the data in the `scraping.py` file

1. Import dependencies
2. Create `scrape_all()` function to scrape all data and store in a dictionary

``` python
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
```

3. Create functions to scrape the following data (linked to source):
    * [Recent News (Title and Summary)](https://mars.nasa.gov/news/)
    * [Featured Image](http://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html)
    * [Mars Facts Table, Mars vs Eath Comparison Table & Image](https://space-facts.com/mars/)
    * [High resolution jpeg files of each of Mars's 4 hemispheres](https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars)

##### Example Function: Mars news title and summary:

``` python
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
 ```  

### Create Flask app & routes to scrape and display data to localhost:5000 in `app.py`

``` python
      from flask import Flask, render_template, redirect
      from flask_pymongo import PyMongo
      import scraping

      app = Flask(__name__)

      # Use flask_pymongo to set up mongo connection
      app.config['MONGO_URI'] = 'mongodb://localhost:27017/mars_app'
      mongo = PyMongo(app)

      # Create Flask Routes

      # Home route


      @app.route('/')
      def index():
          mars = mongo.db.mars.find_one()
          return render_template('index.html', mars=mars)


      @app.route('/scrape')
      def scrape():
          # assign new variable that points to database
          mars = mongo.db.mars
          # create new variable to hold newly scraped data
          mars_data = scraping.scrape_all()
          # update the database
          mars.update({}, mars_data, upsert=True)
          # redirect to home page following successful scrape
          return redirect('/', code=302)


      if __name__ == '__main__':
          app.run()
```
    
## Create index.html template to for Flask app
* Utilized [Bootstrap](https://getbootstrap.com/docs/4.1/getting-started/introduction/) elements such as the [jumbotron container](https://getbootstrap.com/docs/4.1/components/jumbotron/) to design the webpage
``` HTML
      <div class="jumbotron text-center">
```    
* Called data from the MongoDB database (indicated by `{}` or `{{}}`)
``` HTML
      {% for hemisphere in mars.hemispheres %}
      <div class="mx-auto d-block col-xs-6 col-md-3">
          <a class="img-thumbnail" href={{hemisphere.img_link}} target="_blank">
              <img src="{{hemisphere.img_link}}" class="mx-auto d-block img-responsive" alt="...">
              <div class="text-center text-danger caption">
                  <h3>{{hemisphere.title}}</h3>
              </div>
          </a>
```

## Run the App!
With all elements complete, the final step is to set the environment variable `FLASK_APP` equal to `app.py` (within the working dir). Once done, run `app.py` from a terminal and view the page in your browser at port 5000 of localhost (`127.0.0.1:5000` or `localhost:5000`)
