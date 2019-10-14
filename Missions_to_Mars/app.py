from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")


# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    latest_mars_data = mongo.db.collection.find_one()

    if latest_mars_data is None:
        latest_mars_data = {
            "nasa_mars":{"title":"news_title", "paragraph":"news_paragraph"},
            "jpl_image":"featured_image_url",
            "mars_latest_tweet": "mars_weather_tweet",
            "mars_facts":{},
            "mars_hemisphere":{}
            }

    # Return template and data
    return render_template("index.html", data=latest_mars_data)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars_data = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
