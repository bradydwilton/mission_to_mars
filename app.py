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
